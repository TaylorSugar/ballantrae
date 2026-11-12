# ---------- model history (exact Excel values; 2023+ recalculated from sales rows) ----------
def merged_hist(kind):
    out={}
    for n,v in HIST[kind].items():
        if n not in MBY: continue
        row=[]
        for i,y in enumerate(HIST['years']):
            r=srows(n,y) if y in YEARS else []
            row.append(round((sum(s['sp'] for s in r)/len(r)) if kind=='avg' else max(s['sp'] for s in r)) if r else v[i])
        out[n]=row
    return out
hist_avg=merged_hist('avg');hist_hi=merged_hist('hi')
order=[m for m in CHART_ORDER if m in hist_avg];hist_avg={m:hist_avg[m] for m in order};hist_hi={m:hist_hi[m] for m in order}
nlast=[(m,stats(srows(m,LATEST))) for m in MODEL_NAMES]
BDJ=json.dumps(dict(models=order,years=HIST['years'],avg=hist_avg,hi=hist_hi,pal=PAL[:len(order)],
  n={m:[(len(srows(m,y)) if y>=2023 else None) for y in HIST['years']] for m in order}))
