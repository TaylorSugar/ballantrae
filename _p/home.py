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
