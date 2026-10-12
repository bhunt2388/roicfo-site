import sys,re,os
sys.path.insert(0,'.')
from lib import *
from bs4 import BeautifulSoup
L=BeautifulSoup(open('legacy/carbon.html').read(),'html.parser')
for e in L.find_all(True):
    if e.has_attr('style'): del e['style']
def I(sel,root=None):
    e=(root or L).select_one(sel); return e.decode_contents().strip() if e else ''
pg=L.select_one('.page'); kids=[c for c in pg.find_all(True,recursive=False)]
calc_js=[sc.get_text() for sc in L.find_all('script') if 'calcLiability' in sc.get_text()][0]
def raw(sel,root=None): 
    e=(root or L).select_one(sel); return e.decode_contents().strip()
out=head('Section 45Q Carbon Tax Credits — ROI CFO','Section 45Q Carbon Tax Credits — ROI CFO','/carbon-credits/')
links=[('Mechanics','#mechanics'),('The Transaction','#transaction'),('Economics','#economics'),('Protections','#protections'),('Compliance','#compliance')]
out+=navbar(links,('Request Packet','#lead-form'),'https://roicfo.com')
h=kids[0]
mets=''
for c in h.select('.metric-cell'):
    v=c.select_one('.metric-val'); attrs=''.join(f' {k}="{v.get(k)}"' for k in ('data-count','data-prefix','data-suffix','data-decimals') if v.get(k) is not None)
    cls='gr' if 'grn' in v.get('class',[]) else ''
    if v.get('data-count')=='5.25': attrs+=' data-decimals="2"'
    mets+=f'<div class="stat rv"><span class="gl"></span><div class="v"><span class="val {cls}"{attrs}>{v.decode_contents()}</span></div><div class="t">{I(".metric-label",c)}</div></div>'
co=kids[1]; vb=kids[2]
out+=f'''<header class="hero sm" id="hero">{hero_amb()}
<div class="wrap wide"><div class="hero-grid"><div>
<div class="kicker rv">{I('.hero-kicker',h)}</div>
{h1(["A dollar of federal tax credit","acquired for","<em>eighty-five cents.</em>"],'s2')}
<p class="lead rv" style="--d:2">{I('.hero-lead',h)}</p>
<div class="cta rv" style="--d:3">{btn('Schedule a Zoom','https://calendly.com/d/dv9z-zgv-63g/roi-cfo-tax-strategy-explainer','','target="_blank" rel="noopener"')}{btn('Request Packet','#lead-form','ghost')}</div>
</div>
<div class="rv" style="--d:3"><div class="mathcard"><div class="mc-core"><div class="mc-label" style="display:block;margin-bottom:14px">{I('.callout-label',co)}</div><p style="font-family:var(--serif);font-size:clamp(20px,1.8vw,26px);line-height:1.4;color:var(--stone)">{I('.callout-body',co)}</p></div></div></div></div>
<div class="stats stg herostats" style="--cols:4">{mets}</div></div>
</header>
'''
out+=marquee(['Dollar for Dollar','Section 45Q','Section 6418','Form 3800','Pre-Filing Registration','2025 Vintage'])
# vintage + mechanics
s3=kids[3]; steps=''
for i,x in enumerate(s3.select('.step-card')):
    steps+=f'<div class="bezel s4 rv"><div class="core2"><span class="n g">{I(".step-num",x)}</span><span class="gl"></span><h3>{I(".step-title",x)}</h3><p>{I(".step-body",x)}</p></div></div>'
irs=''.join(f'<span>{x.get_text(strip=True)}</span>' for x in s3.select('.irs-item'))
out+=f'''<section id="mechanics" class="lt"><div class="wrap wide">
<div class="bezel rv"><div class="core2 navycore"><div class="banner"><div><span class="ph">{I('.vintage-title',vb)}</span><p style="font-family:var(--serif);font-size:clamp(20px,1.9vw,27px);line-height:1.45;color:var(--stone)!important;max-width:60ch">{I('.vintage-body',vb)}</p></div>
<div class="seal"><svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="47" fill="none" stroke="rgba(217,178,76,.55)" stroke-dasharray="2 5"/><circle cx="50" cy="50" r="38" fill="none" stroke="rgba(247,245,240,.18)"/></svg><b>{I('.vintage-year',vb)}</b><span>{I('.vintage-seal-label',vb)}</span></div></div></div></div>
<div class="head2" style="margin-top:110px"><div>{kicker(I('.section-kicker',s3))}<h2 class="rv">{I('.section-title',s3)}</h2></div><span></span></div>
<div class="rl rl-lt rv" style="margin-top:34px">{irs}</div>
<div class="bento stg">{steps}</div></div></section>
'''
# transaction flow
s4=kids[4]; fc=[]
for x in s4.select('.flow-step'):
    amt=x.select_one('.flow-amount')
    fc.append(f'<div class="bezel s4 rv"><div class="core2"><span class="n g">{I(".flow-num",x)}</span><span class="gl"></span><h3>{I(".flow-title",x)}</h3><p>{I(".flow-body",x)}</p>'+(f'<div class="rule"></div><span class="hl" style="font-family:var(--mono);font-size:13px;color:var(--gold2)">{I(".flow-amount",x)}</span>' if amt else '')+'</div></div>')
flow='''<div class="fd deskonly rv"><svg viewBox="0 0 1000 380" role="img" aria-label="Transaction flow: the Credit Holder transfers $35,000,000 face value of Section 45Q credits to the buyer; the buyer pays a $5,250,000 assignment fee to Welcome 123 1 LLC and $24,500,000 directly to the Credit Holder">
<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#D9B24C" stroke-width="1.6" stroke-linecap="round"/></marker><marker id="ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#46B27A" stroke-width="1.6" stroke-linecap="round"/></marker></defs>
<g class="ringy"><circle cx="500" cy="190" r="104" fill="none" stroke="rgba(217,178,76,.4)" stroke-dasharray="3 9"/></g>
<path class="dash" d="M130 108 C130 -10 870 -10 870 108" style="stroke:#46B27A" marker-end="url(#ag)"/>
<path class="dash" d="M806 190 H566" style="stroke:#D9B24C" marker-end="url(#ah)"/>
<path class="dash" d="M870 272 C870 390 130 390 130 272" style="stroke:#D9B24C;opacity:.9" marker-end="url(#ah)"/>
<circle cx="130" cy="190" r="76" fill="#146B3A"/><circle cx="500" cy="190" r="66" fill="#0F3060" stroke="#D9B24C"/><circle cx="870" cy="190" r="76" fill="#B88A22"/>
<g text-anchor="middle" font-size="21" style="font-family:'EB Garamond',Georgia,serif"><text x="130" y="184" fill="#F7F5F0">Credit</text><text x="130" y="208" fill="#F7F5F0">Holder</text><text x="500" y="184" fill="#F7F5F0">Welcome</text><text x="500" y="208" fill="#F7F5F0">123 1 LLC</text><text x="870" y="198" fill="#0B2545">Buyer</text></g>
<g fill="#F7F5F0" text-anchor="middle" font-size="14.5" font-weight="500"><text x="500" y="30">$35,000,000 face value of Section 45Q credits</text><text x="686" y="170">$5,250,000 assignment fee</text><text x="500" y="366" style="paint-order:stroke;stroke:#0B2545;stroke-width:10px">$24,500,000 paid directly to the Credit Holder</text></g>
<g fill="rgba(247,245,240,.78)" text-anchor="middle" font-size="12" letter-spacing="1.6" font-weight="600"><text x="130" y="86">PARTY A</text><text x="500" y="108">PARTY B</text><text x="870" y="86">PARTY C</text></g>
</svg></div>'''
out+=f'''<section id="transaction" class="dk">{amb()}<div class="wrap wide"><div class="head2"><div>{kicker(I('.section-kicker',s4))}<h2 class="rv">{I('.section-title',s4)}</h2></div><span></span></div>
{flow}<div class="bento stg">{''.join(fc)}</div></div></section>
'''
# economics
s5=kids[5]; rows=''
for tr in s5.select('tr'):
    tds=tr.find_all('td')
    if tds:
        hi=any('hi' in (t.get('class') or []) for t in tds)
        cells=''.join(f'<td class="{" ".join(t.get("class",[]))}">{t.decode_contents()}</td>' for t in tds)
        rows+=f'<tr class="{"row-highlight" if hi else ""}">{cells}</tr>'
ths=''.join(f'<th>{t.decode_contents()}</th>' for t in s5.select('th'))
s6=kids[6]; sv=''
for tr in s6.select('.savings-table tr'):
    tds=tr.find_all('td')
    if tds:
        hi=any('hi' in (t.get('class') or []) for t in tds)
        sv+=f'<tr class="{"row-highlight" if hi else ""}">'+''.join(f'<td class="{" ".join(t.get("class",[]))}">{t.decode_contents()}</td>' for t in tds)+'</tr>'
sth=''.join(f'<th>{t.decode_contents()}</th>' for t in s6.select('.savings-table th'))
cw=s6.select_one('.calc-wrap')
cres=''
for i,x in enumerate(cw.select('.calc-result-item')):
    v=x.select_one('.calc-result-value'); idd=v.get('id'); dl=x.select_one('.calc-result-delta')
    did=f' id="{dl.get("id")}"' if dl.get('id') else ''
    feat='hi' if 'featured' in x.get('class',[]) else ''
    cres+=f'<div class="{feat}"><span class="rl2">{I(".calc-result-label",x)}</span><span class="rv2 {"green" if feat else ""}" id="{idd}">{v.decode_contents()}</span><small{did}>{dl.decode_contents()}</small></div>'
out+=f'''<section id="economics" class="lt"><div class="wrap wide"><div class="head2"><div>{kicker(I('.section-kicker',s5))}<h2 class="rv">{I('.section-title',s5)}</h2></div><span></span></div>
<div class="bezel rv" style="margin-top:56px"><div class="core2" style="padding:0;overflow:hidden"><div class="tbl"><table><thead><tr>{ths}</tr></thead><tbody>{rows}</tbody></table></div></div></div>
<div class="head2" style="margin-top:120px"><div>{kicker(I('.section-kicker',s6))}<h2 class="rv">{I('.section-title',s6)}</h2></div><p class="lead rv">{I('.savings-intro',s6)}</p></div>
<div class="bezel rv" style="margin-top:56px"><div class="core2" style="padding:0;overflow:hidden"><div class="tbl"><table><thead><tr>{sth}</tr></thead><tbody>{sv}</tbody></table></div></div></div>
<p class="note2 rv" style="margin-top:22px;max-width:80ch;color:var(--mute)">{I('.savings-note',s6)}</p>
<div class="bezel rv calc1" style="margin-top:70px"><div class="core2"><span class="ph">{I('.calc-kicker',cw)}</span><h3>{I('.calc-headline',cw)}</h3>
<div class="cfield" style="margin-top:28px"><label class="l" for="calcLiability">{I('.calc-label',cw)}</label><div class="cwrap"><span class="pre">$</span><input id="calcLiability" inputmode="numeric" min="0" placeholder="5,000,000" type="number" value="5000000"></div><p class="note">{I('.calc-rate-note',cw)}</p></div>
<div class="cres">{cres}</div><p class="note" style="margin-top:20px;max-width:80ch">{I('.calc-cta-note',cw)}</p></div></div></div></section>
'''
# book cta
bk=kids[7]
out+=f'''<section id="book" class="dk close">{amb()}<div class="wrap wide"><div class="split">
<div>{kicker(I('.book-cta-label',bk))}<h2 class="closeh rv" style="font-size:clamp(36px,5.4vw,84px)">{I('.book-cta-h2',bk)}</h2></div>
<div class="rv"><p class="lead">{I('.book-cta-sub',bk)}</p><div class="cta" style="margin-top:34px;display:flex;gap:14px;flex-wrap:wrap">{btn('Schedule a Zoom','https://calendly.com/d/dv9z-zgv-63g/roi-cfo-tax-strategy-explainer','','target="_blank" rel="noopener"')}{btn('Request Packet Instead','#lead-form','ghost')}</div><p class="lbl" style="margin-top:26px">{I('.book-avail',bk)}</p></div></div></div></section>
'''
# protections
s8=kids[8]; pc=''
spans=['s6','s6','s4','s4','s4','s12']
for i,x in enumerate(s8.select('.protection-card')):
    pc+=f'<div class="bezel {spans[i]} rv"><div class="core2"><span class="bgnum" aria-hidden="true" style="font-size:clamp(70px,8vw,130px)">{i+1:02d}</span><span class="gl"></span><h3>{I(".prot-title",x)}</h3><p>{I(".prot-body",x)}</p></div></div>'
out+=f'''<section id="protections" class="lt"><div class="wrap wide"><div class="head2"><div>{kicker(I('.section-kicker',s8))}<h2 class="rv">{I('.section-title',s8)}</h2></div><span></span></div><div class="bento stg">{pc}</div></div></section>
'''
# legal
s9=kids[9]; lc=''
for i,x in enumerate(s9.select('.legal-card')):
    lc+=f'<div class="bezel s4 rv"><div class="core2"><span class="n g">{I(".legal-code",x)}</span><h3>{I(".legal-title",x)}</h3><p>{I(".legal-body",x)}</p></div></div>'
out+=f'''<section id="legal" class="st2"><div class="wrap wide"><div class="head2"><div>{kicker(I('.section-kicker',s9))}<h2 class="rv">{I('.section-title',s9)}</h2></div><span></span></div><div class="bento stg">{lc}</div></div></section>
'''
# layers
s10=kids[10]; li=''
for x in s10.select('.layer-item'):
    li+=f'<div class="vi rv"><div class="stepn">{I(".layer-numeral",x)}</div><span class="cat">{I(".layer-cat",x)}</span><h4>{I(".layer-h3",x)}</h4><p>{I(".layer-text",x)}</p></div>'
ls=''
for i,x in enumerate(s10.select('.ls-cell')):
    ls+=f'<div class="bezel s4 rv"><div class="core2"><span class="ph">{I(".ls-label",x)}</span><h3>{I(".ls-title",x)}</h3><p>{I(".ls-body",x)}</p></div></div>'
out+=f'''<section id="compliance" class="dk">{amb()}<div class="wrap wide"><div class="split hd"><div>{kicker(I('.section-kicker',s10))}<h2 class="rv">{I('.section-title',s10)}</h2></div><p class="lead rv">{I('.layers-lede',s10)}</p></div>
<div class="vt">{li}</div><div class="bento stg">{ls}</div></div></section>
'''
# process
s11=kids[11]; ps=''
for i,x in enumerate(s11.select('.step-card')):
    ps+=f'<div class="step rv"><div class="stepn">{i+1:02d}</div><span class="tag">{I(".step-num",x)}</span><h4>{I(".step-title",x)}</h4><p>{I(".step-body",x)}</p></div>'
out+=f'''<section id="process" class="st2"><div class="wrap wide"><div class="head2"><div>{kicker(I('.section-kicker',s11))}<h2 class="rv">{I('.section-title',s11)}</h2></div><span></span></div><div class="steps" style="--n:3">{ps}</div></div></section>
'''
# form
s12=kids[12]; f=s12.select_one('form')
fsel=select('Client Federal Tax Liability Range','tax_liability',['Select range...','Under $1M','$1M – $5M','$5M – $15M','$15M – $30M','$30M+'],'cl-tl')
frm=form(FORMSPREE,'45Q Carbon Credits — ROI CFO — New Advisor Lead','Section 45Q Carbon Tax Credits — ROI CFO','cl-',fsel,'Request CPA Advisor Packet',I('.lead-form-note',s12),'(801) 555-0100')
out+=f'''<section id="lead-form" class="dk close lead-form">{amb()}<div class="wrap wide"><div class="split">
<div>{kicker(I('.section-kicker',s12))}<h2 class="closeh rv">{I('.section-title',s12)}</h2></div>
<div class="rv"><div class="formbox"><div class="formin"><div class="ftitle">{I('.lead-form-title',s12)}</div>{frm}</div></div></div></div></div></section>
'''
ft=kids[13]
out+=f'''<footer>{amb(1)}<div class="wrap wide"><div class="cols" style="grid-template-columns:1fr auto"><div>
<a class="logoplate" href="https://roicfo.com" aria-label="ROI CFO"><img src="/assets/brand/roicfo-logo.png" width="545" height="180" alt="ROI CFO"></a>
<div class="tagline">{I('.footer-entity',ft)}</div></div>
<div><h5>Navigate</h5><a href="https://roicfo.com">Back to ROI CFO</a><a href="https://roicfo.com#strategies">All Strategies</a></div></div>
<div class="fine">{I('.footer-disc',ft)}</div></div></footer>
<div class="sticky-cta" id="stickyCta"><div class="tx">{I('.sticky-cta-text',L)}</div><div class="bt">{btn('Schedule a Zoom','https://calendly.com/d/dv9z-zgv-63g/roi-cfo-tax-strategy-explainer','sm','target="_blank" rel="noopener"')}{btn('Request Packet','#lead-form','sm ghost','id="stickyPacket"')}<button class="x" id="stickyClose" aria-label="Dismiss">&times;</button></div></div>
<script src="/assets/js/fx.js?v=3"></script>
<script>
{calc_js}
</script>
<script>
(function(){{
function easeOutExpo(t){{return t===1?1:1-Math.pow(2,-10*t);}}
function countUp(el){{var target=parseFloat(el.dataset.count),prefix=el.dataset.prefix||'',suffix=el.dataset.suffix||'',dec=parseInt(el.dataset.decimals||'0'),dur=target>=1000?2200:1400,sv=target>=1000?target-8:0,st=Date.now();
 function tick(){{var p=Math.min((Date.now()-st)/dur,1),v=sv+(target-sv)*easeOutExpo(p);el.textContent=prefix+v.toFixed(dec)+suffix;if(p<1)requestAnimationFrame(tick);else el.textContent=prefix+target.toFixed(dec)+suffix;}}requestAnimationFrame(tick);}}
setTimeout(function(){{document.querySelectorAll('.stat .val[data-count]').forEach(function(el,i){{setTimeout(function(){{countUp(el);}},i*200);}});}},500);
var bar=document.getElementById("stickyCta"),cb=document.getElementById("stickyClose"),d=false,s=false;
window.addEventListener("scroll",function(){{if(d)return;var p=window.scrollY/(document.documentElement.scrollHeight-window.innerHeight);if(p>0.18&&!s){{bar.classList.add("show");s=true;}}}},{{passive:true}});
cb.addEventListener("click",function(){{bar.classList.remove("show");d=true;}});
document.querySelectorAll("a[href='#lead-form']").forEach(function(a){{a.addEventListener("click",function(e){{e.preventDefault();var el=document.getElementById("lead-form");if(el)el.scrollIntoView({{behavior:"smooth",block:"start"}});}});}});
}})();
</script>
</body>
</html>
'''
os.makedirs('../carbon-credits',exist_ok=True)
open('../carbon-credits/index.html','w').write(out)
print(len(out))
