# ---------- MODELS ----------
def msum_rows(name):
    out=''
    for y in YEARS:
        r=srows(name,y);s=stats(r)
        out+=f'<tr><td>{y}</td><td>{s["n"] if s else 0}</td><td>{usd(s["avg"]) if s else "–"}</td><td>{usd(s["med"]) if s else "–"}</td></tr>'
    return out
def spark(name):
    k=CHART_ORDER.index(name) if name in CHART_ORDER else 0;col=PAL[k]
    a=hist_avg[name];h=hist_hi[name];yrs=HIST['years'];W,H,Pl,Pr=480,130,10,10
    lo=min(a+h)*.9;hi=max(a+h)*1.05;X=lambda i:Pl+i*(W-Pl-Pr)/(len(yrs)-1);Yf=lambda v:H-26-(H-44)*(v-lo)/(hi-lo)
    pa=' '.join(f'{X(i):.1f},{Yf(v):.1f}' for i,v in enumerate(a));ph=' '.join(f'{X(i):.1f},{Yf(v):.1f}' for i,v in enumerate(h))
    s=f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{name}: average and highest sold price {yrs[0]} to {yrs[-1]}"><polyline points="{ph}" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="5 5" opacity=".7"/><polyline points="{pa}" fill="none" stroke="{col}" stroke-width="3.5" stroke-linejoin="round" stroke-linecap="round"/>'
    s+=''.join(f'<circle cx="{X(i):.1f}" cy="{Yf(v):.1f}" r="3.6" fill="#fff" stroke="{col}" stroke-width="2.4"/>' for i,v in enumerate(a))
    s+=f'<text x="{Pl}" y="{H-6}" font-size="12" fill="#566a5e">{yrs[0]}</text><text x="{W-Pr}" y="{H-6}" font-size="12" fill="#566a5e" text-anchor="end">{yrs[-1]}</text>'
    s+=f'<text x="{X(0):.0f}" y="{Yf(a[0])-9:.0f}" font-size="12" font-weight="700" fill="{col}">{usdm(a[0])}</text><text x="{X(len(a)-1):.0f}" y="{Yf(a[-1])-9:.0f}" font-size="12" font-weight="700" fill="{col}" text-anchor="end">{usdm(a[-1])}</text></svg>'
    return f'<div class="spark"><b style="font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:var(--forest)">Price trend {yrs[0]} to {yrs[-1]}</b>{s}<div class="cap"><span>Solid: average sold price</span><span>Dashed: highest sold price</span></div></div>'
mods=head('Home Models & Floor Plans','Floor plans and elevations for all seven Ballantrae Golf and Country Club models, with sales by year.','models.html')+pagehead('Home models &amp; floor plans','The seven bungalow models, with the original builder floor plans, a price trend and what each has sold for.','Models &amp; floor plans')+f'''
<section class="sec"><div class="wrap"><div class="note" style="margin-top:0">Floor plans and elevations are scanned from the original builder brochure. Rooms, sizes and options shown are approximate; builder options and later renovations vary from home to home. Square footage is as printed on each plan. Bedroom counts vary by option and finished basement, so check the listing.</div>
<div class="filters" style="position:static" role="navigation" aria-label="Jump to a model"><div class="row"><span class="lbl">Jump</span>{''.join(f'<a class="chip" style="text-decoration:none;display:inline-flex;align-items:center" href="#{m["slug"]}">{m["name"]}</a>' for m in MODELS)}</div></div>'''
for m in MODELS:
    st=stats(srows(m['name']))
    mods+=f'''<article class="model rv" id="{m['slug']}"><div class="imgs">{''.join(f'<img src="img/models/{e}.webp" alt="The {m["name"]} elevation {i+1}" loading="lazy" width="560" height="373">' for i,e in enumerate(m['elev']))}</div>
<div><h2 style="margin-bottom:.2em">The {m['name']}</h2><ul class="facts"><li>{m['sqft']:,} sq ft (builder)</li><li>{st['n'] if st else 0} sales on record</li>{f'<li>Avg {usd(st["avg"])}</li>' if st else ''}</ul>
{spark(m['name'])}
<a class="fig" href="img/plans/{m['slug']}-plan.webp" target="_blank" rel="noopener"><img src="img/plans/{m['slug']}-plan-thumb.webp" alt="The {m['name']} floor plan" loading="lazy" style="border:1px solid var(--line);border-radius:10px;margin-bottom:10px" width="520" height="347"></a>
<p class="btns"><a class="btn small" href="img/plans/{m['slug']}-plan.webp" target="_blank" rel="noopener">Open full-size floor plan</a> <a class="btn small green" href="sold.html#all/{m['slug']}">See {m['name']} sales</a></p>
<table class="mini"><thead><tr><th>Year</th><th>Sales</th><th>Average</th><th>Median</th></tr></thead><tbody>{msum_rows(m['name'])}</tbody></table>
<p class="src">Sales: official Sugar Team workbook. Plan: original builder brochure. <a href="market.html#charts">Compare models on the charts →</a></p></div></article>'''
mods+='</div></section>'+cta_band()+foot()
write('models.html',mods)
