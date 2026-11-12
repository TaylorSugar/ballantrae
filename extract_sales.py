#!/usr/bin/env python3
"""Reads the official Ballantrae sales workbook and writes data/sales.json.
Drop a newer workbook (same filename) into data/source/ — any sheet named 'YYYY Solds' is picked up (e.g. '2026 Solds').
The workbook lists every sale twice on some sheets (once in a model block, once in the master list); rows are merged on MLS#."""
import openpyxl,datetime,json,re,os,sys
HERE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(HERE,'data','source','Official Ballantrae Golf and Country Sales Data.xlsx')
OUT=os.path.join(HERE,'data','sales.json')
ALIAS={'innisbrooke':'Innisbrook','innisbrook':'Innisbrook','pine hurst':'Pinehurst','pinehurst':'Pinehurst','peble beach':'Pebble Beach','pebble beach':'Pebble Beach',
       'doral':'Doral','augusta':'Augusta','castle pines':'Castle Pines','grand cypress':'Grand Cypress'}
def clean(v): return v.strip() if isinstance(v,str) else v
def model(v):
    v=clean(v)
    if not v: return None
    return ALIAS.get(v.lower(),v)   # unknown spellings kept as written, never guessed
def view(v):
    v=clean(v); return v or None
def main():
    wb=openpyxl.load_workbook(SRC,data_only=True)
    rows=[]
    for sh in wb.sheetnames:
        m=re.match(r'^(\d{4}) Solds',sh)
        if not m: continue
        ws=wb[sh];hdr=None
        for row in ws.iter_rows():
            vals={c.column:c.value for c in row if c.value is not None}
            if not vals: continue
            names=[clean(v) for v in vals.values()]
            if '#' in names and 'Sold Date' in names:
                hdr={}
                for k,v in sorted(vals.items()):
                    v=clean(v)
                    if v not in hdr: hdr[v]=k
                    if v=='MLS': break
                continue
            if not hdr: continue
            dt=vals.get(hdr['Sold Date'])
            if not isinstance(dt,datetime.datetime): continue
            g=lambda n:vals.get(hdr.get(n))
            rows.append(dict(year=dt.year,sheet=sh,date=dt.strftime('%Y-%m-%d'),addr=clean(g('Address')),dom=g('DOM'),lp=g('List Price'),sp=g('Sold Price'),
                view=view(g('View')),model=model(g('Model')),sqft=g('SQFT'),cond=clean(g('Condition')),mls=clean(g('MLS')),mpac=g('MPAC')))
    merged={}
    for r in rows:
        k=r['mls'] or (r['addr'],r['date'])
        if k in merged:
            for f,v in r.items():
                if merged[k].get(f) in (None,'') and v not in (None,''): merged[k][f]=v
        else: merged[k]=dict(r)
    sales=sorted(merged.values(),key=lambda r:(r['date'],r['addr']))
    hist={}
    if '2018-2022 Data' in wb.sheetnames:
        ws=wb['2018-2022 Data'];sec=None;years=None
        for row in ws.iter_rows(values_only=True):
            cells=[c for c in row if c is not None]
            if not cells: continue
            if isinstance(cells[0],str) and ('Highest' in cells[0] or 'Average' in cells[0]) and len(cells)==1:
                sec='hi' if 'Highest' in cells[0] else 'avg';hist.setdefault(sec,{});continue
            if all(isinstance(c,int) and 2000<c<2100 for c in cells): years=cells;hist['years']=years;continue
            if sec and years and isinstance(cells[0],str) and len(cells)==len(years)+1:
                hist[sec][model(cells[0])]=[round(c) for c in cells[1:]]
    st=os.stat(SRC)
    meta=dict(source_file=os.path.basename(SRC),dropbox_path='/2026 Sugar Team/Ballantrae.ca/Official Ballantrae Golf and Country Sales Data.xlsx',
        workbook_last_modified_in_dropbox='2026-07-16 (client modified 2026-05-11)',sheets=[s for s in wb.sheetnames],
        sale_rows_read=len(rows),unique_sales=len(sales),extracted=datetime.date.today().isoformat())
    json.dump(dict(meta=meta,sales=sales,model_history=hist),open(OUT,'w'),indent=1,default=str)
    print('sales',len(sales),'from',len(rows),'rows;', {y:sum(1 for s in sales if s['year']==y) for y in sorted({s['year'] for s in sales})})
main()
