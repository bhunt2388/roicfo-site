import sys,re
sys.path.insert(0,'.')
from lib import *
from bs4 import BeautifulSoup
L=BeautifulSoup(open('legacy/home.html').read(),'html.parser')
def inner(sel,root=None):
    e=(root or L).select_one(sel); return e.decode_contents().strip() if e else ''
def txt(sel,root=None): return inner(sel,root)
def rv(c,extra=''): return f'<div class="rv {extra}">{c}</div>'

out=head('ROI CFO — Strategic Returns. Responsible Impact.','ROI CFO — Institutional-grade tax and financial strategy delivered exclusively through elite family offices, registered investment advisors, and accounting firms.','/')
links=[('Strategies','#strategies'),('Who We Serve','#serve'),('For Advisors','#network'),('Insights','#insights')]
out+=navbar(links,('Request Introduction','#cta'),'#hero')

# HERO
mc=str(L.select_one('.mathcard'))
mc=mc.replace('class="mathcard"','class="mathcard rv" style="--d:3"',1)
chips=''.join(str(x) for x in L.select('.hero-compliance .comp-item'))
chips=re.sub(r'<span class="comp-mark"></span>','',chips).replace('class="comp-item"','')
out+=f'''<header class="hero" id="hero">{hero_amb()}
<div class="wrap wide"><div class="hero-grid"><div>
<div class="kicker rv">{txt('.hero-kicker')}</div>
{h1(["Your Clients","Owe Less.","<em>Here's the Math.</em>"])}
<p class="lead rv" id="heroSubText" style="--d:2">{txt('#heroSubText')}</p>
<div class="cta rv" style="--d:3">{btn('Get the Advisor Packet','#cta')}{btn('See How It Works','#strategies','ghost')}</div>
<div class="rl rv" style="--d:4">{chips}</div>
</div>
<div>{mc}</div></div></div>
<div class="scrollcue" aria-hidden="true">Scroll</div>
</header>
'''
# STATS
def stat(sid,val,lab,cls=''):
    i=f' id="{sid}"' if sid else ''
    return f'<div class="stat rv"{i}><span class="gl"></span><div class="v">{val}</div><div class="t">{lab}</div></div>'
sb=L.select('#stats .stat-block')
sts=''
for b in sb:
    v=b.select_one('.stat-val').decode_contents()
    v=re.sub(r' style="[^"]*"',' class="sm"',v)
    v=v.replace('class="acc"','class="acc"')
    sts+=stat(b.get('id'),v,b.select_one('.stat-label').decode_contents())
out+=f'<section class="st2" id="stats" style="padding:70px 0 80px"><div class="wrap wide"><div class="stats stg" style="--cols:4">{sts}</div></div></section>\n'
out+=marquee(['Return','Trust','Longevity','Betterment','Strategic Returns','Responsible Impact'])

# PAIN (date gated)
pc=L.select('.pain-card')
pn=''.join(f'<div class="stat rv"><span class="gl"></span><div class="v" style="{ "color:var(--gold)" if "gold" in c.select_one(".pain-num").get("style","") else "color:var(--green)"}">{c.select_one(".pain-num").decode_contents()}</div><div class="t" style="text-transform:none;letter-spacing:0;font-size:14px;line-height:1.65;font-weight:400">{c.select_one(".pain-label").decode_contents()}</div></div>' for c in pc)
out+=f'''<section id="pain" class="lt"><div class="wrap wide">
<div class="head2"><div>{kicker(txt('#pain .sec-kicker'))}<h2 class="rv">Your Clients Are Overpaying the IRS.<br><em>Significantly.</em></h2></div>
<p class="lead rv">{txt('#pain .sec-body')}</p></div>
<div class="stats stg" style="--cols:3;margin-top:70px">{pn}</div>
<div class="bezel rv" style="margin-top:50px"><div class="core2"><span class="gl"></span><h3>{txt('.pain-callout-title')}</h3><p>{txt('.pain-callout-body')}</p></div></div>
</div></section>
'''
# PHILOSOPHY dark
ph=''
spans=['s7','s5','s5','s7']
for i,c in enumerate(L.select('.phil-card')):
    ph+=f'<div class="bezel {spans[i]} rv"><div class="core2"><span class="bgnum" aria-hidden="true">{txt(".phil-num",c)}</span><span class="gl"></span><h3 class="xl">{txt(".phil-title",c)}</h3><p>{txt(".phil-body",c)}</p></div></div>'
out+=f'''<section id="philosophy" class="dk">{amb()}<div class="wrap wide">
<div class="head2"><div>{kicker(txt('#philosophy .sec-kicker'))}<h2 class="rv">Four Pillars.<br><em>No Exceptions.</em></h2></div>
<p class="lead rv">{txt('#philosophy .sec-body')}</p></div>
<div class="bento stg">{ph}</div></div></section>
'''
# STRATEGIES light
def strat(card):
    m=''.join(f'<div><b>{txt(".sm-lbl",x)}</b><span class="{"pos" if "green" in x.select_one(".sm-val").get("class") else ""}">{txt(".sm-val",x)}</span></div>' for x in card.select('.strat-metric'))
    prot=''.join(f'<li>{x.get_text(" ",strip=True)}</li>' for x in card.select('.strat-prot'))
    link=card.select_one('.strat-link'); tgt=' target="_blank"' if link.get('target') else ''
    return f'''<div class="bezel rv" id="{card.get('id')}"><div class="core2"><div class="strat">
<div><div class="code">{txt('.strat-code',card)}</div><h3>{txt('.strat-name',card)}</h3><div class="key">{txt('.strat-keyline',card)}</div><div class="mini">{m}</div></div>
<div><p class="desc">{txt('.strat-desc',card)}</p><div class="ph2">{txt('.strat-prot-head',card)}</div><ul class="tick">{prot}</ul>
<div class="slink">{btn('Full Strategy Deck',link.get('href'),'',tgt)}</div></div></div></div></div>'''
cards=''.join(strat(c) for c in L.select('.strat-card'))
out+=f'''<section id="strategies">
<div class="wrap wide"><div class="head2"><div>{kicker(txt('#strategies .sec-kicker'))}<h2 class="rv">Institutional Access.<br><em>Delivered Through Your Firm.</em></h2></div>
<p class="lead rv">{txt('#strategies .sec-body')}</p></div>
<div id="stratList" style="display:flex;flex-direction:column;gap:18px;margin-top:64px">{cards}
<div class="bezel rv"><div class="core2"><div class="more"><div><h3>{txt('.strat-more-title')}</h3><p>{txt('.strat-more-body')}</p></div>{btn('Join the Network','#network')}</div></div></div></div>
</div></section>
'''
# SERVE
sv=''; spans=['s7','s5','s5','s7']
for i,c in enumerate(L.select('.serve-card')):
    items=''.join(f'<li{" id=%s"%chr(34)+x.get("id")+chr(34) if x.get("id") else ""}>{x.decode_contents()}</li>' for x in c.select('.serve-item'))
    sv+=f'<div class="bezel {spans[i]} rv"><div class="core2"><div class="sicon">{c.select_one(".serve-icon svg").decode()}</div><h3>{txt(".serve-title",c)}</h3><p>{txt(".serve-body",c)}</p><ul class="tick">{items}</ul></div></div>'
out+=f'''<section id="serve" class="st2"><div class="wrap wide">
<div class="head2"><div>{kicker(txt('#serve .sec-kicker'))}<h2 class="rv">Designed for the Advisors<br><em>Families Already Trust.</em></h2></div>
<p class="statement" style="font-size:clamp(24px,2.6vw,38px);max-width:22ch;margin-bottom:14px">{txt('#serve .sec-body')}</p></div>
<div class="bento stg">{sv}</div></div></section>
'''
# NETWORK dark
nb=''
for b in L.select('.net-benefit'):
    nb+=f'<div class="benefit rv"><div class="bi">{b.select_one("svg").decode()}</div><div><b>{txt(".net-title",b)}</b><span>{txt(".net-body",b)}</span></div></div>'
tiers=''.join(f'<div class="tier{" f" if "featured" in t.get("class") else ""}"><div class="tn">{txt(".tier-name",t)}</div><div class="tp">{txt(".tier-pct",t)}</div><div class="tv">{txt(".tier-vol",t)}</div></div>' for t in L.select('.comp-tier'))
out+=f'''<section id="network" class="dk">{amb()}<div class="wrap wide"><div class="split">
<div>{kicker(txt('#network .sec-kicker'))}<h2 class="rv">Join the Firms Delivering<br>Institutional Strategy<br><em>to Their Clients.</em></h2>
<p class="lead rv">{txt('#network .sec-body')}</p><div style="margin-top:36px" class="stg">{nb}</div></div>
<div class="rv"><div class="bezel"><div class="core2"><span class="ph">{txt('.comp-box-title')}</span><div class="tiers">{tiers}</div>
<p class="note2" style="margin-top:26px">{txt('.net-note')}</p><div class="rule"></div>
<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:18px"><div><div style="font-family:var(--serif);font-size:30px;line-height:1.1">Ready to join?</div><div class="lbl" style="margin-top:4px">Applications reviewed within 48 hours.</div></div>{btn('Apply to the Network','#cta')}</div></div></div></div>
</div></div></section>
'''
# PROCESS light with flow diagram
ps=''
for i,s in enumerate(L.select('.proc-step')):
    ps+=f'<div class="step rv"><div class="stepn">{txt(".proc-circle",s).zfill(2)}</div><h4>{txt(".proc-title",s)}</h4><p>{txt(".proc-body",s)}</p></div>'
flow='''<div class="fd rv"><svg viewBox="0 0 1000 340" role="img" aria-label="Flow from ROI CFO to the advisor to the client, with IRS inquiry support returning after filing">
<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M1 1L9 5L1 9" fill="none" stroke="#B88A22" stroke-width="1.6" stroke-linecap="round"/></marker><marker id="ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M1 1L9 5L1 9" fill="none" stroke="#146B3A" stroke-width="1.6" stroke-linecap="round"/></marker></defs>
<g class="ringy"><circle cx="500" cy="120" r="104" fill="none" stroke="rgba(184,138,34,.5)" stroke-width="1" stroke-dasharray="3 9"/></g>
<g class="ringx"><circle cx="130" cy="120" r="90" fill="none" stroke="rgba(11,37,69,.28)" stroke-width="1" stroke-dasharray="2 8"/></g>
<g class="ringx"><circle cx="870" cy="120" r="90" fill="none" stroke="rgba(11,37,69,.28)" stroke-width="1" stroke-dasharray="2 8"/></g>
<path class="dash" d="M200 120 H424" style="stroke:#B88A22" marker-end="url(#ah)"/><path class="dash" d="M576 120 H800" style="stroke:#146B3A" marker-end="url(#ag)"/>
<path class="dash" d="M870 196 C870 330 130 330 130 204" style="stroke:#B88A22;opacity:.8" marker-end="url(#ah)"/>
<circle cx="130" cy="120" r="64" fill="#0B2545"/><circle cx="500" cy="120" r="64" fill="#146B3A"/><circle cx="870" cy="120" r="64" fill="#B88A22"/>
<g fill="#F7F5F0" text-anchor="middle" font-size="26" style="font-family:'EB Garamond',Georgia,serif"><text x="130" y="129">ROI CFO</text><text x="500" y="129">Advisor</text><text x="870" y="129" fill="#0B2545">Client</text></g>
<g fill="#1E2428" text-anchor="middle" font-size="15" font-weight="500"><text x="312" y="98">Briefing and documentation</text><text x="688" y="98">Qualified by the advisor</text><text x="500" y="318" style="paint-order:stroke;stroke:#F7F5F0;stroke-width:12px">IRS inquiry support after filing</text></g>
<g fill="#334155" text-anchor="middle" font-size="12.5" letter-spacing="1.6" font-weight="600"><text x="130" y="34">STRATEGIST</text><text x="500" y="34">CPA, RIA OR FAMILY OFFICE</text><text x="870" y="34">THE FAMILY</text></g>
</svg>
<svg class="fv" viewBox="0 0 360 560" role="img" aria-label="Flow from ROI CFO to the advisor to the client, with IRS inquiry support after filing">
<defs><marker id="ahv" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#B88A22" stroke-width="1.6" stroke-linecap="round"/></marker><marker id="agv" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#146B3A" stroke-width="1.6" stroke-linecap="round"/></marker></defs>
<path class="dash" d="M110 98 V168" style="stroke:#B88A22" marker-end="url(#ahv)"/><path class="dash" d="M110 268 V338" style="stroke:#146B3A" marker-end="url(#agv)"/>
<path class="dash" d="M172 400 C340 400 340 50 172 50" style="stroke:#B88A22;opacity:.8" marker-end="url(#ahv)"/>
<circle cx="64" cy="50" r="48" fill="#0B2545"/><circle cx="64" cy="218" r="48" fill="#146B3A"/><circle cx="64" cy="386" r="48" fill="#B88A22"/>
<g text-anchor="middle" font-size="20" style="font-family:'EB Garamond',Georgia,serif"><text x="64" y="57" fill="#F7F5F0">ROI CFO</text><text x="64" y="225" fill="#F7F5F0">Advisor</text><text x="64" y="393" fill="#0B2545">Client</text></g>
<g fill="#334155" font-size="11" letter-spacing="1.2" font-weight="600"><text x="124" y="46">STRATEGIST</text><text x="124" y="214">CPA, RIA OR FAMILY</text><text x="124" y="228">OFFICE</text><text x="124" y="382">THE FAMILY</text></g>
<g fill="#1E2428" font-size="13" font-weight="500"><text x="122" y="136">Briefing and documentation</text><text x="122" y="306">Qualified by the advisor</text><text x="270" y="500" text-anchor="end">IRS inquiry support after filing</text></g>
</svg></div>'''
out+=f'''<section id="process" class="lt"><div class="wrap wide">
<div class="head2"><div>{kicker(txt('#process .sec-kicker'))}<h2 class="rv">From Introduction to Execution.<br><em>We Carry the Complexity.</em></h2></div><span></span></div>
{flow}
<div class="steps" style="--n:4">{ps}</div></div></section>
'''
# TRUST dark
tcards=''.join(f'<div class="bezel rv"><div class="core2"><div class="bignum {"gn" if "green" in (c.select_one(".trust-stat-val").get("class")) else "gd"}">{txt(".trust-stat-val",c)}</div><div class="rule"></div><p>{c.select_one(".trust-stat-text").decode_contents()}</p></div></div>' for c in L.select('.trust-stat-card'))
tcards=tcards.replace('<strong>','<strong style="color:var(--fg)">',3)
out+=f'''<section id="trust" class="dk">{amb()}<div class="wrap wide">
{kicker(txt('.trust-kicker'))}
<blockquote class="quote rv" style="margin-top:30px;max-width:30ch">{txt('.trust-quote')}</blockquote>
<div class="attr rv"><div><b>{txt('.trust-name')}</b><span>{txt('.trust-role')}</span></div></div>
<div class="bento stg tri">{tcards.replace('<div class="bezel rv">','<div class="bezel s1 rv">')}</div></div></section>
'''
# INSIGHTS light
ic=''
for i,c in enumerate(L.select('.insight-card')):
    src=re.sub(r'<svg.*?</svg>','',c.select_one('.insight-source').decode_contents(),flags=re.S).strip()
    idp=f' id="{c.get("id")}"' if c.get('id') else ''
    a=c.select_one('.insight-read a')
    ic+=f'<div class="bezel rv"{idp}><div class="core2"><div class="iimg" style="background-image:url(/assets/insight-{i+1}.jpg)"><span>{src}</span></div><div class="ibody"><div class="cat">{txt(".insight-cat",c)}</div><h3>{txt(".insight-title",c)}</h3><p>{txt(".insight-sub",c)}</p><a href="{a.get("href")}">Read the Brief</a></div></div></div>'
out+=f'''<section id="insights"><div class="wrap wide"><div class="head2"><div>{kicker(txt('#insights .sec-kicker'))}<h2 class="rv">Built for Return.<br><em>Structured for Legacy.</em></h2></div><div class="rv">{btn('Subscribe to Insights','#cta')}</div></div>
<div class="insights stg">{ic}</div></div></section>
'''
# OBJECTIONS
ob=''
for o in L.select('.objection-item'):
    ob+=f'<div class="rv"><span class="on2">{txt(".objection-num",o)}</span><div><h4>{o.select_one(".objection-q span:last-child").decode_contents()}</h4><p>{txt(".objection-a",o)}</p></div></div>'
out+=f'''<section id="objections" class="st2"><div class="wrap wide"><div class="split">
<div>{kicker(txt('#objections .sec-kicker'))}<h2 class="rv">The Three Questions<br>Every Advisor<br><em>Gets Right.</em></h2><p class="lead rv">{txt('#objections .sec-body')}</p><div class="docbtn rv">{btn('Get the Full Documentation','#cta')}</div></div>
<div class="obj stg">{ob}</div></div></div></section>
'''
# CTA dark close
fsel=select('Interested In','product_interest',['Select strategy...','Section 45Q Carbon Tax Credits','Leveraged Donation Strategy','Both / Not Sure Yet','Other Strategy'],'cta-pi')
tsel=select('Client Tax Liability Range','tax_liability',['Select range...','Under $500K','$500K – $1M','$1M – $5M','$5M – $30M','$30M+'],'cta-tl')
frm=form(FORMSPREE,'ROI CFO Homepage — Advisor Introduction Request','ROI CFO — General Inquiry','h-',fsel+tsel,'Request Confidential Introduction','Advisor-only. Conversations held in strict confidence. 48-hour response commitment. bryson@roicfo.com')
meta=''.join(f'<div><b>{txt(".cta-meta-val",m)}</b><span>{txt(".cta-meta-lbl",m)}</span></div>' for m in L.select('.cta-meta-item'))
urg=L.select_one('#ctaUrgency45Q span').decode_contents()
out+=f'''<section id="cta" class="dk close">{amb()}<div class="wrap wide"><div class="split">
<div>{kicker(txt('.cta-kicker'))}<h2 class="closeh rv">See the Numbers.<br><em>Decide from There.</em></h2><p class="lead rv">{txt('.cta-sub')}</p>
<p class="urg rv" id="ctaUrgency45Q">{urg}</p></div>
<div class="rv"><div class="formbox"><div class="formin"><div class="ftitle">{txt('.cta-form-title')}</div>{frm}</div></div></div></div>
<p class="fine2 rv">{txt('.cta-legal')}</p><div class="meta4 stg">{meta.replace('<div>','<div class="rv">')}</div></div></section>
'''
# COMPANIES (keep id, co-css)
co=L.select_one('#companies'); cards=''
for a in co.select('a.co-card'):
    cards+=f'<a class="co-card rv" href="{a.get("href")}" rel="noopener"><span class="co-core"><span class="co-n">{txt(".co-n",a)}</span><span class="co-name">{txt(".co-name",a)}</span><span class="co-desc">{txt(".co-desc",a)}</span><span aria-hidden="true" class="co-go">Visit site</span></span></a>'
co_css='''.co{background:#F7F5F0;color:#0B2545;padding:clamp(84px,10vw,140px) 0;position:relative;overflow:hidden}
.co *{box-sizing:border-box}
.co-in{max-width:1360px;margin:0 auto;padding:0 32px}
.co-top{display:grid;grid-template-columns:1.4fr 1fr;gap:0 64px;align-items:end;margin-bottom:60px}
.co-k{display:flex;align-items:center;gap:14px;font-size:12px;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:#334155;margin-bottom:22px;font-family:'Inter',sans-serif}
.co-k::before{content:"";width:34px;height:2px;background:#146B3A}
.co h2{font-family:'EB Garamond',Georgia,serif;font-weight:400;font-size:clamp(38px,5.4vw,82px);line-height:.98;letter-spacing:-.022em;color:#0B2545;text-wrap:balance;margin:0}
.co-top p{margin:0;color:#334155;font-size:clamp(16px,1.3vw,19px);line-height:1.7;max-width:46ch}
.co-grid{display:grid;grid-template-columns:repeat(12,1fr);gap:18px}
.co-card{grid-column:span 4;display:block;padding:7px;border-radius:2rem;background:rgba(11,37,69,.035);border:1px solid rgba(11,37,69,.15);color:#0B2545;text-decoration:none;transition:transform .6s cubic-bezier(.32,.72,0,1),border-color .6s cubic-bezier(.32,.72,0,1)}
.co-card:nth-child(4),.co-card:nth-child(5){grid-column:span 6}
.co-core{display:flex;flex-direction:column;gap:12px;height:100%;min-height:260px;padding:34px;border-radius:calc(2rem - 7px);background:#fff;box-shadow:inset 0 1px 1px rgba(255,255,255,.9);position:relative;overflow:hidden}
.co-core::before{content:"";position:absolute;inset:0;background:radial-gradient(420px circle at var(--mx,50%) var(--my,-30%),rgba(184,138,34,.16),transparent 60%);opacity:0;transition:opacity .6s cubic-bezier(.32,.72,0,1);pointer-events:none}
.co-card:hover .co-core::before{opacity:1}
.co-card:hover,.co-card:focus-visible{transform:translateY(-4px);border-color:rgba(184,138,34,.55);outline:none}
.co-card:focus-visible{box-shadow:0 0 0 2px #B88A22}
.co-n{font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.2em;color:#B88A22;position:relative}
.co-name{font-family:'EB Garamond',Georgia,serif;font-size:clamp(30px,3vw,44px);line-height:1;letter-spacing:-.012em;color:#0B2545;position:relative}
.co-desc{font-size:15px;line-height:1.7;color:#334155;position:relative}
.co-go{margin-top:auto;padding-top:20px;font-size:13.5px;font-weight:600;color:#146B3A;letter-spacing:.04em;display:flex;align-items:center;gap:12px;position:relative}
.co-go::after{content:"";width:28px;height:1px;background:#146B3A;transition:width .6s cubic-bezier(.32,.72,0,1)}
.co-card:hover .co-go::after{width:52px}
@media(max-width:1000px){.co-top{grid-template-columns:1fr;gap:22px}.co-card,.co-card:nth-child(4),.co-card:nth-child(5){grid-column:span 6}.co-card:nth-child(5){grid-column:span 12}}
@media(max-width:700px){.co-in{padding:0 22px}.co-card,.co-card:nth-child(4),.co-card:nth-child(5),.co-card:nth-child(5){grid-column:span 12}.co-core{padding:26px;min-height:0}}
@media(prefers-reduced-motion:reduce){.co-card,.co-go::after{transition:none}.co-card:hover{transform:none}}'''
out+=f'<style id="co-css">{co_css}</style>\n<section aria-labelledby="co-h" class="co" id="companies"><div class="co-in"><div class="co-top"><div><span class="co-k">Our companies</span><h2 id="co-h">{txt("#co-h",co)}</h2></div><p>{txt(".co-top p",co)}</p></div><div class="co-grid stg">{cards}</div></div></section>\n'
# FOOTER
fcols=''
for col in L.select('footer .footer-top > div')[1:]:
    links=''.join(f'<a href="{a.get("href")}"{" id=%s"%chr(34)+a.get("id")+chr(34) if a.get("id") else ""}{" target=%s_blank%s"%(chr(34),chr(34)) if a.get("target") else ""}>{a.decode_contents()}</a>' for a in col.select('a'))
    fcols+=f'<div><h5>{txt(".footer-col-head",col)}</h5>{links}</div>'
fc=L.select_one('.footer-contact')
out+=f'''<footer>{amb(1)}<div class="wrap wide"><div class="cols"><div>
<a class="logoplate" href="#hero" aria-label="ROI CFO"><img src="/assets/brand/roicfo-logo.png" width="545" height="180" alt="ROI CFO"></a>
<div class="tagline">{txt('.footer-tagline')}</div><p>{txt('.footer-about')}</p>
<div style="margin-top:20px"><div style="margin-bottom:6px;font-size:14px">{txt('.footer-contact div')}</div><a href="mailto:bryson@roicfo.com">bryson@roicfo.com</a><a href="https://roicfo.com">roicfo.com</a></div></div>
{fcols}</div>
<div class="fine">{txt('.footer-legal')}<br><br>{txt('.footer-copy')}</div></div></footer>
'''
# STICKY
sc=L.select_one('#stickyCta')
out+=f'''<div class="sticky-cta" id="stickyCta"><div class="tx">{txt('.sticky-cta-text')}</div><div class="bt">{btn('Schedule a Zoom','https://calendly.com/d/dv9z-zgv-63g/roi-cfo-tax-strategy-explainer','sm','target="_blank"')}{btn('Request Packet','#cta','sm ghost')}<button class="x" id="stickyClose" aria-label="Dismiss">&times;</button></div></div>
</div>
'''
out+='''<script src="/assets/js/fx.js?v=2"></script>
<script>
(function(){
  var seg=document.getElementById('mcSeg');
  if(seg){var btns=seg.querySelectorAll('button'),panels=document.querySelectorAll('.mc-panel');
    function select(p){seg.dataset.on=p;btns.forEach(function(b){var on=b.dataset.p===p;b.classList.toggle('on',on);b.setAttribute('aria-selected',on?'true':'false');});panels.forEach(function(pl){pl.classList.toggle('on',pl.dataset.panel===p);});}
    btns.forEach(function(b){b.addEventListener('click',function(){select(b.dataset.p);});b.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();var n=seg.dataset.on==='a'?'b':'a';select(n);seg.querySelector('button[data-p="'+n+'"]').focus();}});});}
  var bar=document.getElementById('stickyCta'),cb=document.getElementById('stickyClose'),dd=false,sh=false;
  window.addEventListener('scroll',function(){if(dd)return;var p=window.scrollY/(document.documentElement.scrollHeight-window.innerHeight);if(p>0.20&&!sh){bar.classList.add('show');sh=true;}},{passive:true});
  cb.addEventListener('click',function(){bar.classList.remove('show');dd=true;});
  /* companies spotlight */
  document.querySelectorAll('.co-core').forEach(function(c){c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();c.style.setProperty('--mx',(e.clientX-r.left)+'px');c.style.setProperty('--my',(e.clientY-r.top)+'px');});});
})();
</script>
<!-- ══ MINERAL-STRATEGY-ONLY GATE ══
     Deprioritizes §45Q promotion sitewide on the homepage through Dec 31, 2026.
     Auto-reverts (shows 45Q again) starting Jan 1, 2027. No manual follow-up needed. -->
<script>
(function(){
  var CUTOFF=new Date('2027-01-01T00:00:00');
  if(new Date()>=CUTOFF)return;
  function fixCols(parent){var n=0;for(var i=0;i<parent.children.length;i++){if(parent.children[i].style.display!=='none')n++;}if(n>0)parent.style.setProperty('--cols',n);}
  function hideAndRegrid(id){var el=document.getElementById(id);if(!el)return;var p=el.parentElement;el.style.display='none';if(p)fixCols(p);}
  var seg=document.getElementById('mcSeg');
  if(seg){var tA=document.getElementById('mcTabA'),tB=document.getElementById('mcTabB'),pA=document.getElementById('mcPanelA'),pB=document.getElementById('mcPanelB');
    if(tA&&tB&&pA&&pB){seg.dataset.on='b';tA.classList.remove('on');tA.setAttribute('aria-selected','false');tB.classList.add('on');tB.setAttribute('aria-selected','true');pA.classList.remove('on');pB.classList.add('on');}}
  ['flag45QA','flag45QB'].forEach(function(id){var el=document.getElementById(id);if(el)el.style.display='none';});
  hideAndRegrid('stat45QCredits');hideAndRegrid('stat45QDollar');
  var s45=document.getElementById('strat45Q'),sd=document.getElementById('stratDonation');
  if(s45)s45.style.display='none';
  if(sd&&sd.parentNode)sd.parentNode.insertBefore(sd,sd.parentNode.firstChild);
  hideAndRegrid('insight45Q');
  var fl=document.getElementById('footer45QLink');if(fl)fl.style.display='none';
  var pain=document.getElementById('pain');if(pain)pain.style.display='none';
  var cu=document.getElementById('ctaUrgency45Q');if(cu)cu.style.display='none';
  var hl=document.getElementById('hnwi45QLine');if(hl)hl.style.display='none';
})();
</script>
</body>
</html>
'''
open('../index.html','w').write(out)
print(len(out))
