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
