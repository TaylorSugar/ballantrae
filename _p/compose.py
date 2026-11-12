import re
old=open('build_v1.py').read().split('\n')
seg=lambda a,b:'\n'.join(old[a-1:b])+'\n'
rd=lambda n:open(f'_p/{n}.py').read()
def T(t):
    t=re.sub(r'<section class="s( alt)?"',lambda m:'<section class="sec sand"' if m.group(1) else '<section class="sec"',t)
    t=t.replace('btn dark','btn green').replace('.jpg','.webp')
    t=re.sub(r'</table></div>(?!</div>)','</table></div><p class="hint">Swipe sideways for more columns.</p>',t)
    t=t.replace('<p class="eyebrow">','<p class="eyebrow rv">').replace('class="card"','class="card rv"').replace('class="note"','class="note rv"')
    t=t.replace('Golf & Country Club','Golf and Country Club').replace('Golf &amp; Country Club','Golf and Country Club').replace('Golf &amp; Country','Golf and Country').replace('Golf & Country','Golf and Country')
    return t
def title_fix(t): return t.replace(' | Ballantrae Golf and Country Club','')
com=T(seg(123,151));fsx=T(seg(215,229));sold=T(seg(231,262))
# sold: card-style rows on phones
sold=sold.replace('<table class="t"><thead><tr><th>Sold</th>','<table class="t cards"><thead><tr><th>Sold</th>')
sold=re.sub(r'<td>\{s\["date"\]\}</td><td>\{E\(fixaddr\(s\["addr"\]\)\)\}</td><td>\{model_pill\(s\["model"\]\)\}</td><td class="n">\{s\["sqft"\]:,\}</td><td>\{E\(s\["view"\] or "Not listed"\)\}</td><td class="n">\{usd\(s\["lp"\]\)\}</td><td class="n"><b>\{usd\(s\["sp"\]\)\}</b></td><td class="n">\{s\["dom"\] if s\["dom"\] is not None else "–"\}</td><td class="n">\{ratio\}</td>',
 '<td data-l="Sold">{s["date"]}</td><td data-l="Address">{E(fixaddr(s["addr"]))}</td><td data-l="Model">{model_pill(s["model"])}</td><td class="n" data-l="Sq ft">{s["sqft"]:,}</td><td data-l="View">{E(s["view"] or "Not listed")}</td><td class="n" data-l="List">{usd(s["lp"])}</td><td class="n big" data-l="Sold price"><b>{usd(s["sp"])}</b></td><td class="n" data-l="Days">{s["dom"] if s["dom"] is not None else "–"}</td><td class="n" data-l="Sold ÷ list">{ratio}</td>',sold)
assert 'data-l="Sq ft"' in sold
# pageheads: sold/for-sale/community use pagehead(...) with crumb key
body=seg(1,28)+rd('top')+rd('hist')+rd('home')+com+rd('models')+rd('siteplan')+rd('market')+fsx+sold+rd('about')
body=body.replace("pagehead('Sold","pagehead('Sold")
open('build.py','w').write(body)
