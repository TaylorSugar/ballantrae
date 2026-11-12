#!/usr/bin/env python3
"""One command rebuilds the whole site:  python3 build.py
Inputs : data/sales.json (from extract_sales.py / the official Excel), data/for_sale.json, content.py
Output : site/*.html   (run ./rebuild.sh to re-read the Excel first)"""
import json,os,html,statistics,datetime,re
from content import *
HERE=os.path.dirname(os.path.abspath(__file__));OUT=os.path.join(HERE,'site')
D=json.load(open(os.path.join(HERE,'data','sales.json')));FS=json.load(open(os.path.join(HERE,'data','for_sale.json')))
SALES=D['sales'];META=D['meta'];HIST=D['model_history'];E=html.escape
YEARS=sorted({s['year'] for s in SALES});LATEST=YEARS[-1]
MBY={m['name']:m for m in MODELS}
usd=lambda v:'${:,.0f}'.format(v);usdm=lambda v:'${:.2f}M'.format(v/1e6)
def fixaddr(a):
    a=re.sub(r'\bHllw$','Hollow',a.strip());a=re.sub(r'\bTr$','Trail',a);return a
def stats(rows):
    if not rows:return None
    sp=[r['sp'] for r in rows];dom=[r['dom'] for r in rows if r['dom'] is not None]
    rat=[r['sp']/r['lp'] for r in rows if r['lp']]
    return dict(n=len(rows),avg=sum(sp)/len(sp),med=statistics.median(sp),hi=max(sp),lo=min(sp),dom=sum(dom)/len(dom) if dom else None,ratio=sum(rat)/len(rat)*100 if rat else None,vol=sum(sp))
BY={y:[s for s in SALES if s['year']==y] for y in YEARS};ST={y:stats(BY[y]) for y in YEARS}
MODEL_NAMES=[m['name'] for m in MODELS]
extra=sorted({s['model'] for s in SALES if s['model'] and s['model'] not in MBY})
def mlabel(m): return m if m else 'Model not listed'
def mkey(m): return MBY[m]['slug'] if m in MBY else ('not-listed' if not m else re.sub(r'\W+','-',m.lower()))
MODEL_ORDER=MODEL_NAMES+extra+(['Model not listed'] if any(not s['model'] for s in SALES) else [])
def srows(model,year=None):
    return [s for s in SALES if (mlabel(s['model'])==model) and (year is None or s['year']==year)]

NAV=[('community.html','Community'),('models.html','Models'),('site-plan.html','Site Plan &amp; Maps'),('market.html','Market Stats'),('for-sale.html','For Sale Now'),('sold.html','Sold'),('about.html','About')]
FULL=SITE['fullname'];TL=SITE['title']
PH_IMG={'Community':'lush','Models &amp; floor plans':'bunkers','Site plan &amp; maps':'lush','Market stats':'bunkers','For sale now':'flag','Sold':'sunset','About':'lush','Contact':'fairway'}
def bg(k,eager=False,cls=''):
    f='fetchpriority="high"' if eager else 'loading="lazy"'
    return f'<img class="bgimg {cls}" src="img/stock/{k}-1280.webp" srcset="img/stock/{k}-640.webp 640w, img/stock/{k}-1280.webp 1280w, img/stock/{k}-1920.webp 1920w" sizes="100vw" alt="" {f} decoding="async">'
STK='<span class="stk">Stock golf photo, not Ballantrae</span>'
def head(title,desc,page):
    nav=''.join(f'<a href="{h}"{" class=on aria-current=page" if h==page else ""}>{t}</a>' for h,t in NAV)
    T=title.split(' | ')[0] if page!='index.html' else FULL
    full=T if page=='index.html' else f'{T} | {FULL}'
    return f'''<!doctype html><html lang="en-CA"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(full)}</title><meta name="description" content="{E(desc)}"><meta name="robots" content="noindex"><meta name="theme-color" content="#0f2e20">
<meta property="og:title" content="{E(full)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:image" content="img/stock/fairway-1280.webp">
<link rel="icon" href="img/sugar-crest.png"><link rel="stylesheet" href="css/style.css"></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap"><a class="brand" href="index.html" aria-label="{E(FULL)}"><img src="img/sugar-crest.png" alt="Sugar Team crest" width="70" height="40"><span class="wm"><b>Ballantrae.ca :</b><small>Real Estate Guide to Ballantrae Golf and Country Club</small></span></a>
<button class="menu" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
<nav class="main" id="nav" aria-label="Main">{nav}<a class="alt" href="{SITE['sugarteam_url']}" rel="noopener">sugarteam.ca ↗</a><a class="cta" href="contact.html">Contact</a></nav></div></header><main id="main">'''
def foot():
    T,L=CONTACT['taylor'],CONTACT['leigh']
    links=''.join(f'<li><a href="{h}">{t}</a></li>' for h,t in NAV)
    cred=' · '.join(f'<a href="{u}" rel="noopener">{E(a)}</a>' for a,u,_ in STOCK.values())
    return f'''</main><footer class="site"><div class="wrap"><div class="cols"><div><div class="fcrest"><img src="img/sugar-crest.png" alt="Sugar Team crest" width="80" height="46"><h4 style="margin:0">Sugar Team</h4></div>
<p>{' · '.join(SITE['brand_lines'])}.<br><em>{SITE['tagline']}</em></p>
<p>Taylor Sugar · <a href="tel:{T['tel']}">{T['phone']}</a> · <a href="mailto:{T['email']}">{T['email']}</a><br>Leigh Sugar · <a href="tel:{L['tel']}">{L['phone']}</a> · <a href="mailto:{L['email']}">{L['email']}</a><br>Toll free <a href="tel:{CONTACT['tollfree_tel']}">{CONTACT['tollfree']}</a></p>
<p>{E(CONTACT['office'])}<br><span class="ph">{E(CONTACT['brokerage_line'])}</span></p>
<p><a href="{SITE['sugarteam_url']}" rel="noopener">← Back to sugarteam.ca</a></p></div>
<div><h4>Explore</h4><ul>{links}<li><a href="contact.html">Contact</a></li></ul></div>
<div><h4>Official sources</h4><ul><li><a href="{SOURCES['club']['url']}" rel="noopener">Ballantrae Golf Club</a></li><li><a href="{SOURCES['golfcanada']['url']}" rel="noopener">Golf Canada listing</a></li><li><a href="{SITE['sugarteam_url']}" rel="noopener">sugarteam.ca</a></li></ul></div></div>
<div class="fine"><p>Sales statistics are compiled by the Sugar Team from the official Ballantrae Golf and Country sales workbook (sales through {LAST_DATE}) and are not guaranteed. Floor plans and elevations are reproduced from the original builder brochure for reference; dimensions and finishes are approximate and may differ from the home as built. Listings on the For Sale page are a dated snapshot of public listing pages, shown with the listing brokerage; they are not a live MLS® feed. This site is not affiliated with Ballantrae Golf Club or the condominium corporations. {SITE['preview_note']}</p>
<p>{E(CONTACT['disclaimer'])}</p>
<p><b>Photo credits.</b> Decorative golf photography is generic stock from Pexels (free under the Pexels License) and does not show Ballantrae: {cred}. Overhead map: Imagery © Google. Floor plans: original builder brochure. Club facts: <a href="{SOURCES['club']['url']}" rel="noopener">ballantraegolfclub.com</a>.</p></div></div></footer>
<nav class="dock" aria-label="Quick contact"><a href="tel:{T['tel']}">Call Taylor</a><a class="p" href="contact.html">Contact us</a></nav>
<script src="js/main.js" defer></script></body></html>'''
LAST_DATE=datetime.date.fromisoformat(max(s['date'] for s in SALES)).strftime('%B %-d, %Y')
def pagehead(h1,p,crumb,img=None):
    k=img or PH_IMG.get(crumb,'lush')
    return f'<section class="phero">{bg(k,True,"kb")}{STK}<div class="wrap rv"><div class="crumb"><a href="index.html">Home</a> / {crumb}</div><h1>{h1}</h1><p>{p}</p></div></section>'
def write(name,body): open(os.path.join(OUT,name),'w').write(body);print('wrote',name)
def bars(vals,labels,title,fmt=usdm,color='#16523a',color2=None,vals2=None,h=300):
    W,P=640,48;n=len(vals);mx=max(vals+(vals2 or []))*1.18;bw=(W-P-14)/n
    s=f'<svg viewBox="0 0 {W} {h}" role="img" aria-label="{E(title)}" style="width:100%;height:auto"><line x1="{P}" y1="{h-38}" x2="{W-8}" y2="{h-38}" stroke="#9bb5a2"/>'
    for i,(v,l) in enumerate(zip(vals,labels)):
        x0=P+i*bw+bw*.14;ww=bw*.72/(2 if vals2 else 1)
        hh=(h-80)*v/mx;s+=f'<rect x="{x0:.0f}" y="{h-38-hh:.0f}" width="{ww:.0f}" height="{hh:.0f}" fill="{color}" rx="4"/><text x="{x0+ww/2:.0f}" y="{h-42-hh:.0f}" text-anchor="middle" font-size="{10 if vals2 else 12}" font-weight="700" fill="#14261c">{fmt(v)}</text>'
        if vals2:
            v2=vals2[i];h2=(h-80)*v2/mx;s+=f'<rect x="{x0+ww+2:.0f}" y="{h-38-h2:.0f}" width="{ww:.0f}" height="{h2:.0f}" fill="{color2}" rx="4"/><text x="{x0+ww*1.5+2:.0f}" y="{h-42-h2:.0f}" text-anchor="middle" font-size="10" font-weight="700" fill="#14261c">{fmt(v2)}</text>'
        s+=f'<text x="{P+i*bw+bw/2:.0f}" y="{h-16}" text-anchor="middle" font-size="13" fill="#14261c">{l}</text>'
    return s+'</svg>'
PAL=['#16523a','#5cb85c','#2a7fba','#76c7ec','#AD1F0F','#8c7b4f','#0e8a8a']
CHART_ORDER=['Doral','Castle Pines','Augusta','Grand Cypress','Pinehurst','Innisbrook','Pebble Beach']
def model_pill(m):
    return f'<a href="models.html#{MBY[m]["slug"]}">{E(m)}</a>' if m in MBY else E(mlabel(m))
def kpis(items): return '<div class="kpis">'+''.join(f'<div class="kpi rv"><b>{v}</b><span>{l}</span></div>' for v,l in items)+'</div>'
def cta_band(h='Thinking about Ballantrae?',p='Tell us about your plans. We will compare your home, by model and view, against every recent sale in the community.'):
    return f'<section class="panel" style="min-height:70vh;min-height:70svh;text-align:center;justify-content:center">{bg("sunset")}<div class="wrap rv" style="padding-top:90px;padding-bottom:90px"><p class="eyebrow">Sugar Team</p><h2>{h}</h2><p class="lede" style="margin:0 auto 26px;color:#eaf6ee">{p}</p><div class="btns" style="justify-content:center"><a class="btn" href="contact.html">Talk to Taylor and Leigh</a><a class="btn ghost" href="sold.html">See what has sold</a></div><p class="tag">{SITE["tagline"]}</p></div></section>'
def src_link(k): return f'<a href="{SOURCES[k]["url"]}" rel="noopener">{E(SOURCES[k]["label"])}</a>'
SRC_NOTE=f'Source: official Ballantrae Golf and Country Sales Data workbook ({E(META["source_file"])}, Sugar Team Dropbox). Sales through {LAST_DATE}.'
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
# ---------- HOME ----------
l=ST[LATEST];tot=sum(ST[y]['n'] for y in YEARS)
recent=sorted(SALES,key=lambda s:s['date'],reverse=True)[:6]
fs_sorted=FS['listings']
hag=[s for s in SALES if 'hagen' in s['addr'].lower()];hagrow=hag[0] if hag else None
tasks=[('for-sale.html','Buy',f'{len(fs_sorted)} homes for sale now','A dated snapshot with price, beds, baths and listing brokerage.'),
('sold.html','Compare','Sold prices by year and model','Every sale on record, filterable, linked to floor plans.'),
('models.html','Choose','Seven models and floor plans','Elevations, plans and a price trend for each model.'),
('market.html','Track','Market stats and charts','Average and highest sold price by model, 2018 to 2025.'),
('site-plan.html','Explore','Site plan and overhead map','Streets, condo corporations and amenities.'),
('contact.html','Sell','What is my home worth?','Priced against sales of the same model and view.')]
home=head(FULL,'Homes for sale, sold prices, floor plans and market stats for Ballantrae Golf and Country Club in Whitchurch-Stouffville, from the Sugar Team.','index.html')+f'''
<section class="panel" id="top">{bg("fairway",True,"kb")}{STK}<div class="wrap hero-in">
<p class="eyebrow rv">Whitchurch-Stouffville, Ontario · Sugar Team</p>
<h1 class="rv d1">{TL}</h1>
<ul class="pills rv d2">{''.join(f'<li>{b}</li>' for b in SITE['brand_lines'])}</ul>
<p class="lead rv d2">Every sale from {YEARS[0]} to {YEARS[-1]} sorted by year and by model, the original floor plans, an overhead map and the homes for sale now.</p>
<div class="btns rv d3"><a class="btn" href="for-sale.html">Homes for sale now</a><a class="btn ghost" href="sold.html">See sold prices</a><a class="btn ghost" href="contact.html">Contact Taylor and Leigh</a></div>
<p class="tag rv d3">{SITE['tagline']}</p></div><a class="cue" href="#glance">Scroll</a></section>
<section class="panel left" id="glance">{bg("lush")}{STK}<div class="wrap" style="padding-top:110px;padding-bottom:80px"><p class="eyebrow rv">{LATEST} at a glance</p><h2 class="rv d1" style="max-width:16ch">The Ballantrae market, from the official sales data</h2>
{kpis([(l['n'],f'homes sold in {LATEST}'),(usd(l['avg']),f'average sold price, {LATEST}'),(usd(l['med']),f'median sold price, {LATEST}'),(tot,f'sales on record, {YEARS[0]} to {YEARS[-1]}')])}
<p class="rv" style="font-size:.84rem;color:#d9ecdf;max-width:70ch">{SRC_NOTE}</p><div class="btns rv"><a class="btn" href="market.html">Explore the charts</a><a class="btn ghost" href="sold.html">All {len(SALES)} sales</a></div></div></section>
<section class="sec sky"><div class="wrap"><p class="eyebrow rv">What do you want to do?</p><h2 class="rv">Start where you are</h2>
<div class="grid g3">{''.join(f'<a class="card top rv d{i%3}" href="{h}" style="text-decoration:none;color:inherit"><span class="eyebrow">{k}</span><h3>{t}</h3><p style="color:var(--mute);margin:0">{d}</p></a>' for i,(h,k,t,d) in enumerate(tasks))}</div></div></section>
<section class="panel" id="map">{'<img class="bgimg" src="img/overhead-map.webp" alt="Overhead view of the Ballantrae community" loading="lazy" decoding="async">'}<div class="wrap" style="padding-top:100px;padding-bottom:70px;display:flex;flex-direction:column;justify-content:flex-end;min-height:100svh"><div style="max-width:560px;background:rgba(15,46,32,.78);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);padding:clamp(20px,4vw,36px);border-radius:var(--r)" class="rv"><p class="eyebrow">The community</p><h2>Homes between the fairways</h2><p>Detached bungalows around an 18-hole golf course, a recreation centre with a pool and fitness room, and ponds, trails and mature trees, on Highway 48 just north of Aurora Road.</p><div class="btns"><a class="btn" href="site-plan.html">Open the overhead map</a><a class="btn ghost" href="community.html">Explore the community</a></div><p style="font-size:.75rem;color:#cfe7d6;margin:14px 0 0">Imagery © Google</p></div></div></section>
<section class="sec sand"><div class="wrap"><div class="two"><div class="rv"><p class="eyebrow">For sale now</p><h2>{len(fs_sorted)} homes listed in the community</h2><p class="lede">A dated snapshot of public listings inside Ballantrae Golf and Country Club as of {FS['as_of_label']}, with the listing brokerage shown on every home.</p>
<ul class="ticks">{''.join(f'<li><b>{E(x["address"])}</b> · {usd(x["price"])} · {x["beds"]} bd / {x["baths"]} ba</li>' for x in fs_sorted[:4])}</ul><a class="btn" href="for-sale.html">See all {len(fs_sorted)} listings</a></div>
<figure class="fig rv d1"><img src="img/hagen.webp" alt="23 Hagen Hollow, sold by the Sugar Team" loading="lazy" width="1000" height="667"><figcaption>Just sold: 23 Hagen Hollow, a Castle Pines model. <a href="sold.html#recent">See the sale →</a></figcaption></figure></div></div></section>
<section class="sec"><div class="wrap"><p class="eyebrow rv">Seven models</p><h2 class="rv">Find your model, see its floor plan, see what it sold for</h2>
<div class="mgrid">{''.join(f'<a class="mcard rv d{i%3}" href="models.html#{m["slug"]}"><img src="img/models/{m["elev"][0]}.webp" alt="The {m["name"]} elevation" loading="lazy" width="560" height="373"><div><b>{m["name"]}</b><span>{m["sqft"]:,} sq ft · {sum(1 for s in SALES if s["model"]==m["name"])} sales on record</span></div></a>' for i,m in enumerate(MODELS))}
<a class="mcard rv" href="site-plan.html" style="display:flex;align-items:center;justify-content:center;background:var(--forest);color:#fff;text-align:center;padding:18px"><div><b style="color:#fff">Site plan and maps</b><span style="color:var(--lime)">Streets, condo corporations, recreation centre</span></div></a></div></div></section>
<section class="sec green"><div class="wrap"><p class="eyebrow rv">Recently sold</p><h2 class="rv">The latest sales on record</h2>
<div class="tablewrap rv"><table class="t cards"><thead><tr><th>Sold</th><th>Address</th><th>Model</th><th class="n">List</th><th class="n">Sold price</th><th class="n">Days</th></tr></thead><tbody>
{''.join(f'<tr><td data-l="Sold">{s["date"]}</td><td data-l="Address">{E(fixaddr(s["addr"]))}</td><td data-l="Model">{model_pill(s["model"])}</td><td class="n" data-l="List">{usd(s["lp"])}</td><td class="n big" data-l="Sold price"><b>{usd(s["sp"])}</b></td><td class="n" data-l="Days">{s["dom"]}</td></tr>' for s in recent)}</tbody></table></div>
<p style="margin-top:18px"><a class="btn" href="sold.html">All {len(SALES)} sales by year and model →</a></p></div></section>
<section class="sec sand"><div class="wrap"><p class="eyebrow rv">Your Ballantrae team</p><h2 class="rv">The Sugar Team</h2>
<figure class="fig rv"><img src="img/team.webp" alt="The Sugar Team: Sarah Lawrence, Martin Wales, Leigh Sugar, Taylor Sugar, David Fletcher and Blair Dunlop" loading="lazy" width="1400" height="394" style="background:#fff"><figcaption>Team photo from <a href="{SITE['sugarteam_url']}" rel="noopener">sugarteam.ca</a>. Left to right: {', '.join(f'{n}, {t}' for n,t in TEAM)}.</figcaption></figure>
<div class="btns" style="margin-top:22px"><a class="btn green" href="about.html">Meet Taylor and Leigh</a><a class="btn ghost" style="color:var(--forest)!important;border-color:var(--forest)" href="{SITE['sugarteam_url']}" rel="noopener">Visit sugarteam.ca ↗</a></div></div></section>
'''+cta_band()+foot()
write('index.html',home)
# ---------- COMMUNITY ----------
rates=f'''<table class="mini"><tbody><tr><td>Green fee, Mon–Thu</td><td>$84.07</td></tr><tr><td>Green fee, Fri, weekends &amp; holidays</td><td>$97.35</td></tr><tr><td>Twilight</td><td>$53.10</td></tr><tr><td>Shared cart, per rider</td><td>$22.12</td></tr></tbody></table>'''
comm=head('The Community & Lifestyle | Ballantrae Golf and Country Club','Golf, recreation centre, trails, location and what it is like to live at Ballantrae Golf and Country Club in Whitchurch-Stouffville.','community.html')+pagehead('The community &amp; lifestyle','What Ballantrae Golf and Country Club offers, who built it, how it is organized, and where the golf course fits in.','Community')+f'''
<section class="sec"><div class="wrap"><div class="grid g3">
<div class="card rv"><h3>Where it is</h3><p>Ballantrae Golf and Country Club is a master-planned adult lifestyle community in the hamlet of Ballantrae, Whitchurch-Stouffville, York Region. The main entrance road from Highway 48 is Ballantrae Common, and the property sits just north of Aurora Road.</p><p class="src">Sources: Maurice Smith, <em>Naming the Streets of Ballantrae G&amp;CC</em> (2013, from Sugar Team files); original builder site plan; {src_link('fairways2')}.</p></div>
<div class="card rv"><h3>How big it is</h3><p>The original builder brochure describes roughly 900 homes. The condominium map in our files shows <b>{sum(c['units'] for c in CONDOS)}</b> units across five condominium corporations, plus a separate corporation for the recreation centre.</p><p class="src">Sources: builder brochure (site plan); condominium map (Sugar Team files). The unit total is the sum of the five counts printed on that map.</p></div>
<div class="card rv"><h3>The homes</h3><p>Detached bungalows in seven models, from the {MODELS[-1]['sqft']:,} sq ft Pebble Beach to the {MODELS[0]['sqft']:,} sq ft Grand Cypress, set in clusters around the course. <a href="models.html">See every model and floor plan →</a></p><p class="src">Source: builder floor-plan brochure (square footage as printed on each plan).</p></div></div></div></section>
<section class="sec sand" id="golf"><div class="wrap"><div class="two"><div><p class="eyebrow rv">The golf course</p><h2>An 18-hole course at the heart of the community</h2>
<ul class="ticks"><li><b>Ballantrae Golf Club</b> is a public 18-hole, par-72 course of 6,545 yards, with rental clubs, a driving range, lessons, a junior membership and a restaurant. ({src_link('golfcanada')})</li>
<li>It was designed by Doug Carrick and opened in 2001. Fairways Golf &amp; Travel describes generous fairways, raised and contoured greens and a walkable routing, with the homes kept on one side of the holes and now screened by mature trees. ({src_link('fairways')})</li>
<li>The club's own site lists a practice area with driving range, chipping and putting greens, plus a monitored pace of play. ({src_link('rates')})</li></ul>
<div class="note rv"><b>Public course, not private.</b> The course is open to the public, so ask us or the club how residents' play, tee times and any member programs work before you buy. <span class="ph">Resident access terms: to confirm with the club</span></div></div>
<div class="card rv"><h3>2026 rates, as posted by the club</h3>{rates}<p>The club also sells a limited 30-game digital package ($77.88 a round, valid two years, tee times bookable 28 days ahead). The club's page showed it as sold out when we checked.</p>
<p><b>Clubhouse restaurant:</b> open daily 11:00 am to 7:30 pm. The kitchen is closed on Mondays; sandwiches, snacks and drinks are still served. ({src_link('dining')})</p>
<p class="src">Ballantrae Golf Club · 1 The Master's South, Stouffville, ON L4A 1M2 · (905) 640-6333 · <a href="{SOURCES['club']['url']}" rel="noopener">ballantraegolfclub.com</a>. Prices exclude taxes and can change; confirm with the club.</p></div></div></div></section>
<section class="sec" id="rec"><div class="wrap"><div class="two"><figure class="fig"><img src="img/rec-centre-layout.webp" alt="Floor plan of the Ballantrae recreation centre" loading="lazy" width="1200" height="620"><figcaption>Recreation centre layout, from the Sugar Team's community files.</figcaption></figure>
<div><p class="eyebrow rv">Recreation centre</p><h2>Pool, fitness, billiards and a place to gather</h2><p>The recreation centre's layout shows a swimming pool and whirlpool with locker rooms and a sauna, an exercise room, a billiards room, a card room, a library, a lounge, and party rooms with a kitchen. The original builder brochure also lists tennis courts and a hot tub among the homeowners' amenities.</p>
<p>The brochure map marks the gatehouse, clubhouse and restaurant, practice area, recreation centre, tennis, ponds and wooded natural trails. <a href="site-plan.html">See the site plan and maps →</a></p>
<p class="src">Sources: recreation centre layout and builder brochure (Sugar Team files). Hours, fees and rules are set by the condominium corporations; <span class="ph">confirm current amenity details with the corporation</span>.</p></div></div></div></section>
<section class="sec sand"><div class="wrap"><p class="eyebrow rv">How Ballantrae is organized</p><h2>Five condominium corporations, named for golf's greats</h2>
<p style="max-width:70ch">Streets are named after champions. Each condominium corporation has its own theme, according to a street-naming article by resident Maurice Smith (Sept. 30, 2013), kept in the Sugar Team files.</p>
<div class="tablewrap"><table class="t" style="min-width:520px"><thead><tr><th>Corporation</th><th>YRCC no.</th><th class="n">Units (per map)</th><th>Street-name theme</th></tr></thead><tbody>{''.join(f'<tr><td>Condo {c["n"]}</td><td>{c["corp"]}</td><td class="n">{c["units"]}</td><td>{c["streets"]}</td></tr>' for c in CONDOS)}</tbody></table></div><p class="hint">Swipe sideways for more columns.</p>
<div class="note rv">Buying here usually means a monthly condominium fee. Currently listed homes show fees from $674.39 to $857.36 a month where the listing publishes one (see <a href="for-sale.html">For Sale Now</a>). Ask us what a given corporation's fee covers, and review the status certificate before you firm up.</div></div></section>
<section class="sec"><div class="wrap"><p class="eyebrow rv">Buying here</p><h2>What drives value in Ballantrae</h2>
<div class="grid g3"><div class="card rv"><h3>Model</h3><p>Seven models sell at different levels. The <a href="sold.html">Sold page</a> shows each model's sales by year, with its floor plan one click away.</p></div>
<div class="card rv"><h3>View and lot</h3><p>The sales data records each home's view, such as golf, trees, pond or house. We compare your home with sales that share its model and view.</p></div>
<div class="card rv"><h3>Condition</h3><p>The data also notes condition, from original to renovated, which is why two homes of the same model can sell far apart.</p></div></div></div></section>
'''+cta_band()+foot()
write('community.html',comm)
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
# ---------- SITE PLAN ----------
sp=head('Site Plan & Maps','Overhead map, original site plan, condominium map, brochure map and street-naming guide for Ballantrae Golf and Country Club.','site-plan.html')+pagehead('Site plan &amp; maps','Find your street, your condominium corporation and the amenities.','Site plan &amp; maps')+f'''
<section class="sec"><div class="wrap"><p class="eyebrow rv">Overhead map</p><h2 class="rv">The community from above</h2>
<figure class="fig rv" style="margin-top:18px"><a href="img/overhead-map.webp" target="_blank" rel="noopener"><img src="img/overhead-map.webp" alt="Overhead aerial map of the Ballantrae community, golf course and surrounding roads" width="1600" height="961" fetchpriority="high"></a><figcaption><b>Imagery © Google.</b> Overhead view of the community and golf course. Highway 48 runs down the left side and Aurora Road crosses the bottom right. Tap to open full size.</figcaption></figure></div></section>
<section class="sec sand"><div class="wrap"><p class="eyebrow rv">Original site plan</p><h2 class="rv">The builder's site plan</h2><figure class="fig rv"><a href="img/site-plan.webp" target="_blank" rel="noopener"><img src="img/site-plan.webp" alt="Ballantrae site plan showing streets, golf holes and ponds" loading="lazy" width="1400" height="875"></a><figcaption>Original builder site plan (artist's concept; E.&amp;O.E.). Highway 48 is on the left; Aurora Road runs along the bottom. Tap to open full size.</figcaption></figure>
<div class="grid g2" style="margin-top:28px"><div class="card rv"><h3>Reading the map</h3><p>Ballantrae Common leads in from Highway 48 to two traffic circles, First Round and Final Round, joined by The Masters South and The Masters North. Clusters of homes sit between the golf holes, with ponds and woodland around the edges.</p><p class="src">Source: Maurice Smith street-naming article (2013) and the site plan above.</p></div>
<div class="card rv d1"><h3>What the brochure map marks</h3><ul class="ticks"><li>Gatehouse</li><li>Clubhouse and restaurant, practice area</li><li>Recreation centre and tennis</li><li>Ponds and wooded natural trails</li><li>A typical community cluster</li></ul><p class="src">Source: legend on the original brochure map (Sugar Team files).</p></div></div></div></section>
<section class="sec"><div class="wrap"><div class="two"><figure class="fig rv"><a href="img/condo-map.webp" target="_blank" rel="noopener"><img src="img/condo-map.webp" alt="Map of the five Ballantrae condominium corporations" loading="lazy" width="1300" height="761"></a><figcaption>Condominium corporations map from the Sugar Team's community files (unit counts as printed on the map).</figcaption></figure>
<div class="rv d1"><p class="eyebrow">Condominium corporations</p><h2>Five corporations, one ring road</h2><div class="tablewrap"><table class="t" style="min-width:340px"><thead><tr><th>Corp.</th><th>YRCC</th><th class="n">Units</th></tr></thead><tbody>{''.join(f'<tr><td>Condo {c["n"]}</td><td>{c["corp"]}</td><td class="n">{c["units"]}</td></tr>' for c in CONDOS)}</tbody><tfoot><tr><td>Total</td><td></td><td class="n">{sum(c['units'] for c in CONDOS)}</td></tr></tfoot></table></div><p style="margin-top:12px">The recreation centre has its own corporation (1202). The ring road is corporation 967.</p></div></div></div></section>
<section class="sec sky"><div class="wrap"><div class="two"><div class="rv"><p class="eyebrow">More maps</p><h2>Brochure map of the grounds</h2><p>This photo of the builder's brochure map numbers the golf holes and marks the amenities. Use it with the maps above.</p><p class="note">Photo of a printed brochure: some edges are cropped. For a clean version, ask us.</p></div>
<figure class="fig rv d1"><a href="img/brochure-map.webp" target="_blank" rel="noopener"><img src="img/brochure-map.webp" alt="Brochure map of Ballantrae with amenity legend" loading="lazy" width="1100" height="825"></a></figure></div></div></section>
'''+cta_band()+foot()
write('site-plan.html',sp)
# ---------- MARKET ----------
yt=''.join(f'<tr><td><b>{y}</b></td><td class="n">{ST[y]["n"]}</td><td class="n">{usd(ST[y]["avg"])}</td><td class="n">{usd(ST[y]["med"])}</td><td class="n">{usd(ST[y]["hi"])}</td><td class="n">{usd(ST[y]["lo"])}</td><td class="n">{ST[y]["dom"]:.0f}</td><td class="n">{ST[y]["ratio"]:.1f}%</td></tr>' for y in YEARS)
def datatab(d,label):
    return f'<details class="dt"><summary>{label}: exact values</summary><div class="tablewrap"><table class="t" style="min-width:640px"><thead><tr><th>Model</th>'+''.join(f'<th class="n">{y}</th>' for y in HIST['years'])+'</tr></thead><tbody>'+''.join(f'<tr><td>{m}</td>'+''.join(f'<td class="n">{usd(v)}</td>' for v in d[m])+'</tr>' for m in order)+'</tbody></table></div><p class="hint">Swipe sideways for more columns.</p></details>'
mkt=head('Market Stats','Sales by year, average and highest sold prices by model, 2018 to 2025, for Ballantrae Golf and Country Club.','market.html')+pagehead('Market stats','Sales by year, average and highest sold prices, and how each model has moved, from the official sales workbook.','Market stats')+f'''
<section class="sec sky" id="charts"><div class="wrap"><p class="eyebrow rv">Interactive charts</p><h2 class="rv">Sold prices by model, {HIST['years'][0]} to {HIST['years'][-1]}</h2>
<p class="lede rv">Switch between average and highest sold price, and between a year-by-year view and a model-by-model view. All values are exact figures from the official workbook; none are read off images.</p>
<div class="chart rv"><h3 id="ctitle">Average sold price by model</h3><p class="cap" id="ccap"></p>
<div class="ctl"><div class="seg" id="seg-metric" role="group" aria-label="Metric"><button data-v="avg" aria-pressed="true">Average</button><button data-v="hi" aria-pressed="false">Highest</button></div>
<div class="seg" id="seg-view" role="group" aria-label="View"><button data-v="year" aria-pressed="true">By year</button><button data-v="model" aria-pressed="false">By model</button></div></div>
<div class="legend" id="legend"></div><div class="filters" id="yrow" style="display:none;position:static;box-shadow:none;margin:8px 0;padding:8px 0;border:0;background:none;gap:8px;flex-direction:row;overflow-x:auto"></div>
<div class="cv" id="cv" style="min-height:330px"></div><p class="readout" id="readout" aria-live="polite"></p>
<p class="src">{SRC_NOTE} 2018 to 2022 come from the "2018-2022 Data" sheet of the workbook; 2023 onward are recalculated from the individual sales rows so they match the Sold page (the sheet's own 2023 figures differ for Castle Pines and Pinehurst). Models with few sales in a year can swing widely.</p></div>
<div style="margin-top:18px">{datatab(hist_avg,'Average sold price by model')}{datatab(hist_hi,'Highest sold price by model')}</div></div></section>
<section class="sec"><div class="wrap">{kpis([(ST[y]["n"],f"sales in {y}") for y in YEARS][:3]+[(usd(ST[LATEST]["avg"]),f"{LATEST} average price")])}
<div class="grid g2"><div class="chart rv"><h3>Average and median sold price</h3><p class="cap">Green: average. Red: median.</p>{bars([ST[y]['avg'] for y in YEARS],[str(y) for y in YEARS],'Average and median sold price by year',vals2=[ST[y]['med'] for y in YEARS],color2='#AD1F0F')}</div>
<div class="chart rv d1"><h3>Number of sales per year</h3><p class="cap">Sales through {LAST_DATE}.</p>{bars([ST[y]['n'] for y in YEARS],[str(y) for y in YEARS],'Sales per year',fmt=lambda v:str(int(v)),color='#2a7fba')}</div></div></div></section>
<section class="sec sand"><div class="wrap"><h2 class="rv">Year by year</h2><div class="tablewrap rv"><table class="t"><thead><tr><th>Year</th><th class="n">Sales</th><th class="n">Average</th><th class="n">Median</th><th class="n">Highest</th><th class="n">Lowest</th><th class="n">Avg days</th><th class="n">Sold ÷ list</th></tr></thead><tbody>{yt}</tbody></table></div><p class="hint">Swipe sideways for more columns.</p>
<p class="src">{SRC_NOTE} Average and median are calculated from each year's individual sales. "Sold ÷ list" is the average of each sale's sold price divided by its list price. {LATEST} covers sales up to {LAST_DATE}; a {YEARS[-1]+1} sheet can be added to the workbook and the site rebuilt.</p>
<h2 style="margin-top:44px" class="rv">By model, {LATEST}</h2><div class="tablewrap rv"><table class="t" style="min-width:560px"><thead><tr><th>Model</th><th class="n">Sales</th><th class="n">Average</th><th class="n">Median</th><th>Floor plan</th></tr></thead><tbody>{''.join(f'<tr><td>{E(m)}</td><td class="n">{s["n"] if s else 0}</td><td class="n">{usd(s["avg"]) if s else "–"}</td><td class="n">{usd(s["med"]) if s else "–"}</td><td><a href="models.html#{MBY[m]["slug"]}">Floor plan</a> · <a href="sold.html#{LATEST}/{MBY[m]["slug"]}">Sales</a></td></tr>' for m,s in nlast)}</tbody></table></div><p class="hint">Swipe sideways for more columns.</p>
<div class="btns" style="margin-top:26px"><a class="btn" href="sold.html">Browse every sale</a><a class="btn green" href="contact.html">Ask for a home-value report</a></div></div></section>
<script>window.BD={BDJ};</script>
'''+cta_band()+foot()
write('market.html',mkt)
# ---------- FOR SALE ----------
def card(x):
    maint=f' · <b>Maintenance fee:</b> ${x["maintenance_fee_monthly"]:,.2f}/mo' if x['maintenance_fee_monthly'] else ''
    mod=f' · <b>Model (per listing remarks):</b> {model_pill(x["model_per_remarks"])}' if x['model_per_remarks'] else ''
    return f'''<article class="listing"><div><h3>{E(x['address'])}</h3><div class="meta"><span><b>{x['beds']}</b> bed</span><span><b>{x['baths']}</b> bath</span><span>{x['sqft_range']} sq ft</span><span>MLS® {E(x['mls'])}</span></div>
<div class="meta" style="margin-top:4px"><span>{mod[3:] if mod else 'Model not stated in the listing'}{maint}</span></div>
<p class="courtesy">Listing courtesy of {E(x['brokerage'])}. Listed about {x['listed_days_before_snapshot']} days before {FS['as_of_label']}.</p></div>
<div><div class="price">{usd(x['price'])}</div><a class="btn small" href="{x['url']}" target="_blank" rel="noopener">View public listing ↗</a></div></article>'''
fs=head('Homes For Sale Now | Ballantrae Golf and Country Club','Homes currently for sale in Ballantrae Golf and Country Club, as of '+FS['as_of_label']+'.','for-sale.html')+pagehead('For sale now',f'{len(FS["listings"])} homes listed inside Ballantrae Golf and Country Club, as of {FS["as_of_label"]}.','For sale now')+f'''
<section class="sec"><div class="wrap"><div class="note rv" style="margin-top:0"><b>Snapshot as of {FS['as_of_label']}.</b> Compiled from public listing pages ({', '.join(f'<a href="{s["url"]}" rel="noopener">{E(s["name"])}</a>' for s in FS['sources'])}). This is not a live feed, so prices and status may have changed. Each home shows its listing brokerage and links to its public page. <a href="contact.html">Ask us for today's list, or for homes that are not yet on the market.</a></div>
{''.join(card(x) for x in FS['listings'])}
<p class="src" style="font-size:.82rem;color:var(--mute)">Information deemed reliable but not guaranteed. MLS® and the listing data belong to their respective boards and brokerages. {' '.join(E(n) for n in FS['notes'][:1])}</p>
<div class="btns" style="margin-top:18px"><a class="btn" href="contact.html">Book a showing with the Sugar Team</a><a class="btn green" href="sold.html">See recent sold prices</a></div></div></section>
'''+cta_band('Want to see one of these homes?','Tell us which address, and compare it with what similar Ballantrae homes have sold for.')+foot()
write('for-sale.html',fs)
# ---------- SOLD ----------
mtabs=''.join(f'<button class="chip" data-model="{mkey(m)}" aria-pressed="false">{E(m)}</button>' for m in MODEL_ORDER)
ytabs=''.join(f'<button class="chip" data-year="{y}" aria-pressed="false">{y} ({ST[y]["n"]})</button>' for y in sorted(YEARS,reverse=True))
matrix='<div class="tablewrap"><table class="t" style="min-width:760px" id="by-model"><thead><tr><th>Model</th><th>Floor plan</th>'+''.join(f'<th class="n">{y}</th>' for y in YEARS)+'<th class="n">All years</th></tr></thead><tbody>'
for m in MODEL_ORDER:
    cells=''
    for y in YEARS:
        s=stats(srows(m,y));cells+=f'<td class="n">{(f"<b>{s["n"]}</b> · avg {usd(s["avg"])}<br><small>median {usd(s["med"])}</small>") if s else "–"}</td>'
    sa=stats(srows(m));cells+=f'<td class="n">{(f"<b>{sa["n"]}</b> · avg {usd(sa["avg"])}<br><small>median {usd(sa["med"])}</small>") if sa else "–"}</td>'
    fp=f'<a href="models.html#{MBY[m]["slug"]}">Floor plan</a>' if m in MBY else '<small>No floor plan on file</small>'
    matrix+=f'<tr data-mm="{mkey(m)}"><td><a href="#" data-pick="{mkey(m)}"><b>{E(m)}</b></a></td><td>{fp}</td>{cells}</tr>'
tot_cells=''.join(f'<td class="n"><b>{ST[y]["n"]}</b> · avg {usd(ST[y]["avg"])}<br><small>median {usd(ST[y]["med"])}</small></td>' for y in YEARS)
allst=stats(SALES);matrix+=f'<tr><td><b>All models</b></td><td></td>{tot_cells}<td class="n"><b>{allst["n"]}</b> · avg {usd(allst["avg"])}<br><small>median {usd(allst["med"])}</small></td></tr></tbody></table></div><p class="hint">Swipe sideways for more columns.</p>'
def salerow(s):
    mk=mkey(s['model']);ratio=f'{s["sp"]/s["lp"]*100:.1f}%' if s['lp'] else '–'
    return f'<tr data-y="{s["year"]}" data-m="{mk}"><td data-l="Sold">{s["date"]}</td><td data-l="Address">{E(fixaddr(s["addr"]))}</td><td data-l="Model">{model_pill(s["model"])}</td><td class="n" data-l="Sq ft">{s["sqft"]:,}</td><td data-l="View">{E(s["view"] or "Not listed")}</td><td class="n" data-l="List">{usd(s["lp"])}</td><td class="n big" data-l="Sold price"><b>{usd(s["sp"])}</b></td><td class="n" data-l="Days">{s["dom"] if s["dom"] is not None else "–"}</td><td class="n" data-l="Sold ÷ list">{ratio}</td></tr>'
blocks=''
for y in sorted(YEARS,reverse=True):
    s=ST[y]
    blocks+=f'<div class="yearblock" id="y{y}"><h3>{y}: {s["n"]} sales</h3><p class="yearsum">Average {usd(s["avg"])} · median {usd(s["med"])} · highest {usd(s["hi"])} · lowest {usd(s["lo"])}</p><div class="tablewrap"><table class="t cards"><thead><tr><th>Sold</th><th>Address</th><th>Model</th><th class="n">Sq ft</th><th>View</th><th class="n">List</th><th class="n">Sold price</th><th class="n">Days</th><th class="n">Sold ÷ list</th></tr></thead><tbody>{"".join(salerow(r) for r in sorted(BY[y],key=lambda r:r["date"],reverse=True))}</tbody></table></div></div>'
hag=[s for s in SALES if 'hagen' in s['addr'].lower()]
hagrow=hag[0] if hag else None
sold=head('Sold Prices by Year & Model | Ballantrae Golf and Country Club','Every Ballantrae Golf and Country Club sale by year and by model, from the official sales workbook.','sold.html')+pagehead('Sold','Every sale on record, by year and by model. Pick a year or a model to filter.','Sold')+f'''
<section class="sec" id="sold-app"><div class="wrap">
<h2 style="font-size:1.5rem">Sales by model and year</h2><p>Counts, average and median sold prices from the official workbook. Click a model name to filter the sales below, or open its floor plan.</p>{matrix}
<p class="src" style="font-size:.82rem;color:var(--mute)">{SRC_NOTE} Model names are as written in the workbook (spelling variants such as "Innisbrooke" are grouped under Innisbrook). A sale with no model in the data would appear as "Model not listed".</p>
<div class="filters" id="sold-list" role="group" aria-label="Filter sales"><div class="row"><span class="lbl">Year</span><button class="chip" data-year="all" aria-pressed="true">All years ({len(SALES)})</button>{ytabs}</div><div class="row"><span class="lbl">Model</span><button class="chip" data-model="all" aria-pressed="true">All models</button>{mtabs}</div><div class="count" id="sold-count" aria-live="polite">{len(SALES)} sales shown</div></div>
{blocks}
{f'<div id="recent" class="card rv" style="margin-top:34px"><div class="two"><img src="img/hagen.webp" alt="23 Hagen Hollow" loading="lazy" style="border-radius:10px" width="1200" height="800"><div><p class="eyebrow rv">Just sold by the Sugar Team</p><h3>23 Hagen Hollow</h3><p>{model_pill(hagrow["model"])} model · sold {hagrow["date"]} for <b>{usd(hagrow["sp"])}</b> (listed {usd(hagrow["lp"])}, {hagrow["dom"]} days). {E(hagrow["view"] or "")} view.</p><p class="src" style="font-size:.8rem;color:var(--mute)">Photo from the Sugar Team files; sale data from the official workbook.</p></div></div></div>' if hagrow else ''}
<noscript><p>Filters need JavaScript; all years and models are listed above.</p></noscript></div></section>
'''+cta_band('Curious what your Ballantrae home would sell for?','Tell us your model and view, and we will price it against the sales above.')+foot()
write('sold.html',sold)
# ---------- ABOUT ----------
T,L=CONTACT['taylor'],CONTACT['leigh']
about=head('About Taylor & Leigh','Meet Taylor Sugar and Leigh Sugar of the Sugar Team, your Ballantrae real estate specialists.','about.html')+pagehead('About Taylor &amp; Leigh','The Sugar Team: Smart Real Estate, Sweet People, Successful Transitions.','About')+f'''
<section class="sec"><div class="wrap"><div class="two"><div class="rv"><p class="eyebrow">Sugar Team</p><h2>Smart Real Estate. Sweet People. Successful Transitions.</h2><p class="lede">We track every Ballantrae Golf and Country Club sale by model, view and condition, so a price is backed by what homes like yours have actually sold for. {SITE['tagline']}</p>
<p>The bios below are condensed from the team's published profiles on <a href="{SITE['sugarteam_url']}" rel="noopener">sugarteam.ca</a>.</p><p class="btns"><a class="btn" href="contact.html">Contact us</a><a class="btn green" href="{SITE['sugarteam_url']}" rel="noopener">Visit sugarteam.ca ↗</a></p></div>
<div class="rv d1 card top"><h3>Why Ballantrae buyers and sellers call us</h3><ul class="ticks"><li><b>{len(SALES)}</b> sales on record, {YEARS[0]} to {YEARS[-1]}, sorted by year and model</li><li>All seven models and floor plans in one place</li><li>Written opinion-of-value reports, backed by the sales data</li></ul></div></div></div></section>
<section class="sec sand"><div class="wrap"><p class="eyebrow rv">The team</p><h2 class="rv">Your Sugar Team</h2>
<figure class="fig rv"><img src="img/team.webp" alt="The Sugar Team, left to right: {', '.join(n for n,_ in TEAM)}" loading="lazy" width="1400" height="394" style="background:#fff"><figcaption>Team photo from sugarteam.ca. Names and titles left to right:</figcaption></figure>
<ul class="teamlist rv">{''.join(f'<li><b>{n}</b>{t}</li>' for n,t in TEAM)}</ul></div></section>
<section class="sec"><div class="wrap"><div class="people">
<div class="person rv"><img src="img/taylor.webp" alt="Taylor Sugar" width="480" height="600" loading="lazy"><div><h3>Taylor Sugar</h3><p><b>Broker · Team Manager</b></p><p>In real estate since 2008 and a broker since 2012. Taylor was raised in Whitchurch-Stouffville and Aurora. He writes detailed written opinion-of-value reports so clients see the market data, and he views every home as an investment.</p><p><a href="tel:{T['tel']}">{T['phone']}</a><br><a href="mailto:{T['email']}">{T['email']}</a></p></div></div>
<div class="person rv d1"><img src="img/leigh.webp" alt="Leigh Sugar" width="480" height="600" loading="lazy"><div><h3>Leigh Sugar</h3><p><b>Broker</b></p><p>A former banking executive with experience in personal and business finance, financial planning, marketing and project management. Homes are her hobby: designing, renovating, decorating and investing in them. Leigh lives and works in York Region.</p><p><a href="tel:{L['tel']}">{L['phone']}</a><br><a href="mailto:{L['email']}">{L['email']}</a></p></div></div></div>
<div class="note"><span class="ph">PLACEHOLDER</span> Client testimonials, awards and a Ballantrae-specific track-record line (homes sold in the community) are not shown because they have not been confirmed for this site. Add them in content.py when ready.</div></div></section>
'''+cta_band()+foot()
write('about.html',about)
# ---------- CONTACT ----------
contact=head('Contact','Contact Taylor Sugar and Leigh Sugar about Ballantrae Golf and Country Club.','contact.html')+pagehead('Contact','Thinking of buying or selling at Ballantrae? Call or email us.','Contact')+f'''
<section class="sec"><div class="wrap"><div class="grid g2"><div class="card top rv"><h3>Taylor Sugar</h3><p style="color:var(--mute)">{T['role']}</p><p><a class="btn small" href="tel:{T['tel']}">Call {T['phone']}</a></p><p><a href="mailto:{T['email']}?subject=Ballantrae%20Golf%20and%20Country%20Club">{T['email']}</a></p></div>
<div class="card top rv d1"><h3>Leigh Sugar</h3><p style="color:var(--mute)">{L['role']}</p><p><a class="btn small" href="tel:{L['tel']}">Call {L['phone']}</a></p><p><a href="mailto:{L['email']}?subject=Ballantrae%20Golf%20and%20Country%20Club">{L['email']}</a></p></div></div>
<div class="grid g2" style="margin-top:24px"><div class="card rv"><h3>Send us a note</h3><p>Email works best for home-value requests. Tell us your address (or model and view) and when you are thinking of moving.</p><a class="btn" href="mailto:{T['email']}?subject=What%20is%20my%20Ballantrae%20home%20worth%3F&amp;body=Name%3A%0AAddress%20or%20model%2Fview%3A%0ATiming%3A">Ask what my home is worth</a><p class="src">This opens your email app. There is no web form or data collection on this preview.</p></div>
<div class="card rv d1"><h3>Office</h3><p>{E(CONTACT['office'])}<br>Toll free <a href="tel:{CONTACT['tollfree_tel']}">{CONTACT['tollfree']}</a></p><p><span class="ph">{E(CONTACT['brokerage_line'])}</span></p><p>{SITE['tagline']}</p><p><a href="{SITE['sugarteam_url']}" rel="noopener">sugarteam.ca ↗</a></p></div></div></div></section>
'''+foot()
write('contact.html',contact)
print('done',len(SALES),'sales;',len(FS['listings']),'listings')
