import sys,re
sys.path.insert(0,'.')
from lib import *
from bs4 import BeautifulSoup
L=BeautifulSoup(open('legacy/lev.html').read(),'html.parser')
for e in L.find_all(True):
    if e.has_attr('style'): del e['style']
def I(sel,root=None):
    e=(root or L).select_one(sel); return e.decode_contents().strip() if e else ''
def sec_head(sid):
    r=L.select_one('#'+sid) if sid else None
    return r
def S(sid): return L.select_one('#'+sid)
js_src=open('legacy/lev.html').read()
# preserve original scripts verbatim
scripts=[sc.get_text() for sc in L.find_all('script') if not sc.get('src')]
main_js=scripts[0]
# drop old nav/fade/stagger/table observers and scroll-bar, keep globe, countup, calculator
g_end=main_js.index('/* ── NAV ── */')
globe=main_js[:g_end]
cu_a=main_js.index('/* ── COUNT UP ── */'); cu_b=main_js.index('/* ── FADE UP ── */')
countup=main_js[cu_a:cu_b]
ca=main_js.index('/* ── CALCULATOR ── */')
calc=main_js[ca:]

out=head('Leveraged Donation Strategy — ROI CFO','ROI CFO — A federally compliant 5:1 leveraged donation strategy for high-income taxpayers.','/leveraged-donation/')
links=[('How It Works','#how'),('The Math','#math'),('The Asset','#asset'),('Compliance','#compliance'),('Compensation','#compensation')]
out+=navbar(links,('Get Started','#cta'),'https://roicfo.com')

# HERO
stats=''
for st in L.select('.hero-stat'):
    v=st.select_one('.val'); attrs=''.join(f' {k}="{v.get(k)}"' for k in ('data-count','data-prefix','data-suffix','data-decimals') if v.get(k) is not None)
    stats+=f'<div class="stat rv"><span class="gl"></span><div class="v"><span class="val"{attrs}>{v.decode_contents()}</span></div><div class="t">{I(".lbl",st)}</div></div>'
terms=''.join(f'<span>{t.decode_contents()}</span>' for t in L.select('.hero-terms .term'))
kick=L.select_one('.hero-kicker').get_text(strip=True)
out+=f'''<header class="hero" id="hero">{hero_amb()}
<div class="wrap wide"><div class="hero-grid"><div>
<div class="kicker rv">{kick}</div>
{h1(["Turn Tax Liability Into","<em>Real Cash Return</em>"])}
<p class="lead rv" style="--d:2">{I('.hero-sub')}</p>
<div class="cta rv" style="--d:3">{btn('Request Advisor Package','#cta')}{btn('See How It Works','#how','ghost')}</div>
<div class="rl rv" style="--d:4">{terms}</div>
<p class="legalline rv" style="--d:5">{I('.hero-legal')}</p>
</div>
<div class="rv" style="--d:3"><div class="globe"><div id="hero-three"></div></div></div></div>
<div class="stats stg herostats" style="--cols:4">{stats}</div></div>
</header>
'''
out+=marquee(['Deduction','Documentation','Qualified Appraisal','Related Use','Form 8283','K-1'])

# HOW
how=S('how'); steps=''
for i,s in enumerate(how.select('.step-v')):
    steps+=f'<div class="vi rv"><div class="stepn">{I(".step-v-num",s)}</div><h4>{I(".step-v-head",s)}</h4><p>{I(".step-v-body",s)}</p></div>'
out+=f'''<section id="how" class="lt"><div class="wrap wide"><div class="split hd">
<div>{kicker(I('.sec-kicker',how))}<h2 class="rv">{I('.sec-title',how)}</h2></div><p class="lead rv">{I('.sec-body',how)}</p></div>
<div class="vt">{steps}</div></div></section>
'''
# LEVERAGE dark
lv=S('leverage'); bl=''
for b in lv.select('.bullet-item'):
    t=b.select_one('.bullet-text'); st=t.find('strong'); head=st.decode_contents(); st.extract()
    bl+=f'<div class="bezel s6 rv"><div class="core2"><span class="gl"></span><h3>{head}</h3><p>{t.decode_contents().strip()}</p></div></div>'
rb=I('.ratio-body',lv)
out+=f'''<section id="leverage" class="dk">{amb()}<div class="wrap wide">
<div class="split hd"><div>{kicker(I('.sec-kicker',lv))}<h2 class="rv">{I('.sec-title',lv)}</h2></div><div class="rv"><div class="bignum gd">{I('.ratio-num',lv)}</div><div class="lbl" style="margin-top:8px">{I('.ratio-lbl',lv)}</div></div></div>
<p class="statement wide" style="margin-top:50px">{rb}</p>
<div class="bento stg">{bl}</div></div></section>
'''
# MATH
def table(t,cls):
    t=BeautifulSoup(str(t),'html.parser')
    return f'<div class="tbl">{t.decode()}</div>'
m=S('math')
sums=''
for c in m.select('.sum-card'):
    k={'g':'gr','o':'acc','n':''}[c.select_one('.sum-val').get('class')[-1]]
    sums+=f'<div class="stat rv"><span class="gl"></span><div class="v"><span class="{k}">{I(".sum-val",c)}</span></div><div class="t" style="text-transform:none;letter-spacing:0;font-size:14px;line-height:1.6;font-weight:400">{I(".sum-lbl",c)}</div></div>'
out+=f'''<section id="math" class="lt"><div class="wrap wide"><div class="split hd"><div>{kicker(I('.table-note',m))}<h2 class="rv">{I('.sec-title',m)}</h2></div><p class="lead rv">{I('.sec-body',m)}</p></div>
<div class="bezel rv" style="margin-top:56px"><div class="core2" style="padding:0;overflow:hidden">{table(m.select_one('table'),'')}</div></div>
<div class="stats stg" style="--cols:3;margin-top:60px">{sums}</div></div></section>
'''
# TIERS
t=S('tiers')
out+=f'''<section id="tiers" class="st2"><div class="wrap wide"><div class="split hd"><div>{kicker(I('.sec-kicker',t))}<h2 class="rv">{I('.sec-title',t)}</h2></div><p class="lead rv">{I('.sec-body',t)}</p></div>
<div class="bezel rv" style="margin-top:56px"><div class="core2" style="padding:0;overflow:hidden">{table(t.select_one('table'),'')}</div></div></div></section>
'''
# CALCULATOR
c=S('calculator')
def fld(label,inner): return f'<div class="cfield"><label class="l">{label}</label>{inner}</div>'
def pre(i,v,extra=''): return f'<div class="cwrap"><span class="pre">$</span><input class="hp" id="{i}" oninput="fmtInput(this);{extra}" type="text" value="{v}"></div>'
def suf(i,mx,v,fn): return f'<div class="cwrap"><input class="hs" id="{i}" max="{mx}" min="0" oninput="{fn}()" step="0.1" type="number" value="{v}"><span class="suf">%</span></div>'
def res(lbl,i,val,cls='',full=False,hi=False):
    return f'<div class="{"full " if full else ""}{"hi" if hi else ""}"><span class="rl2">{lbl}</span><span class="rv2 {cls}" id="{i}">{val}</span></div>'
p1=f'''<div class="bezel rv"><div class="core2"><span class="ph">Client Tax Savings</span><h3>Client Tax Savings</h3><p>Adjust income and tax rates to match your client</p>
<div style="margin-top:26px">{fld('Client Annual Income',pre('c-income','1,000,000','calcClient()'))}
<div class="two">{fld('Federal Rate',suf('c-fed',50,37,'calcClient'))}{fld('State Rate',suf('c-state',15,9.3,'calcClient'))}</div></div>
<div class="cres">{res('Investment Required','r-investment','$60,000','gold')}{res('Charitable Deduction (5×)','r-deduction','$300,000')}{res('Federal Tax Saved','r-fed-saved','$111,000','green')}{res('State Tax Saved','r-state-saved','$27,900','green')}{res('Net Cash Benefit (after investment cost)','r-net','$78,900','green big',True,True)}{res('Return on Investment','r-roi','131.5%','gold',True)}</div></div></div>'''
p2=f'''<div class="bezel rv"><div class="core2"><span class="ph">Your Referral Earnings</span><h3>Your Referral Earnings</h3><p>Tier unlocked by total charitable deductions generated</p>
<div style="margin-top:26px" class="two">{fld('Clients Per Year','<div class="cwrap"><input id="a-clients" max="500" min="1" oninput="calcAdvisor()" type="number" value="5"></div>')}{fld('Avg Client Income',pre('a-income','1,000,000','calcAdvisor()'))}</div>
<div class="cres">{res('Avg Investment / Client','a-avg-inv','$60,000')}{res('Total Client Investment','a-total-inv','$300,000')}{res('Total Charitable Deductions Generated','a-total-ded','$1,500,000','',True)}</div>
<div style="margin-top:22px"><span class="rl2">Your Current Tier</span><span class="tier-label t1" id="a-tier-label">Standard — 10%</span>
<div class="tier-track"><div class="tier-track-bar"><div class="tier-track-fill" id="a-progress-fill" style="width:8%"></div></div><div class="tier-labels"><span>$0</span><span>$5M → 15%</span><span>$10M → 20%</span></div><div class="tier-next" id="a-next-tier">Generate $5M in charitable deductions to unlock the 15% tier.</div></div></div>
<div class="cres"><div class="full hi"><span class="rl2">Your Annual Referral Fee</span><span class="rv2 gold big" id="a-fee">$15,000</span></div></div></div></div>'''
out+=f'''<section id="calculator" class="lt"><div class="wrap wide"><div class="split hd"><div>{kicker(I('.sec-kicker',c))}<h2 class="rv">{I('.sec-title',c)}</h2></div><p class="lead rv">{I('.sec-body',c)}</p></div>
<div class="calcgrid stg">{p1}{p2}</div></div></section>
'''
# ASSET
a=S('asset'); cards=''
ac=a.select('.asset-card')
def acard(x,span):
    extra=''
    pr=x.select_one('.product-row')
    if pr:
        extra='<ul class="srvlist">'+''.join(f'<li><b>{I(".product-name",p)}</b> · {I(".product-sub",p)}</li>' for p in pr.select('.product-item'))+'</ul>'; pr.decompose()
    return f'<div class="bezel {span} rv"><div class="core2"><span class="ph">{I(".asset-label",x)}</span><h3>{I(".asset-head",x)}</h3><p>{I(".asset-body",x)}</p>{extra}</div></div>'
cards=acard(ac[0],'s6')+acard(ac[1],'s6')+acard(ac[2],'s12')
cb=a.select_one('.charity-banner')
bul=''.join(f'<li>{x.decode_contents()}</li>' for x in cb.select('li'))
out+=f'''<section id="asset" class="st2"><div class="wrap wide"><div class="head2"><div>{kicker(I('.sec-kicker',a))}<h2 class="rv">{I('.sec-title',a)}</h2></div><p class="lead rv">{I('.sec-body',a)}</p></div>
<div class="bezel rv" style="margin-top:56px"><div class="core2 navycore"><div class="banner"><div><span class="ph">{I('.stout-label',a)}</span><h3>{I('.stout-firm',a)}</h3><p>{I('.stout-detail',a)}</p></div>
<div style="text-align:right"><div class="bignum gd">{I('.stout-num',a)}</div><div class="lbl" style="margin-top:10px">{I('.stout-num-label',a)}</div></div></div></div></div>
<div class="bento stg">{cards}
<div class="bezel s12 rv"><div class="core2"><div class="banner"><div><span class="ph">Related-Use Charitable Donation</span><h3>{I('.charity-title',cb)}</h3><p>{I('.charity-body',cb)}</p></div><ul class="tick">{bul}</ul></div></div></div></div></div></section>
'''
# DOCUMENTATION dark
d=S('documentation'); dc=''
spans=['s6','s6','s7','s5']
for i,x in enumerate(d.select('.doc-card')):
    k1=''
    kx=x.select_one('.k1-example')
    if kx:
        rows=''.join(f'<tr class="{"row-highlight" if "highlight" in r.get("class",[]) else ""}"><td>{r.find_all("span")[0].decode_contents()}</td><td>{r.find_all("span")[1].decode_contents()}</td></tr>' for r in kx.select('.k1-row'))
        k1=f'<div class="k1"><span class="ph" style="margin-top:20px">{I(".k1-label",kx)}</span><div class="tbl"><table style="min-width:0"><tbody>{rows}</tbody></table></div></div>'
    hl=I('.doc-highlight',x)
    out_hl=f'<span class="hl" style="display:block;margin-top:18px;font-family:var(--mono);font-size:12.5px;color:var(--gold2);letter-spacing:.04em">{hl}</span>' if hl else ''
    dc+=f'<div class="bezel {spans[i]} rv"><div class="core2"><span class="ph">{I(".doc-num",x)}</span><h3>{I(".doc-head",x)}</h3><p>{I(".doc-body",x)}</p>{k1}{out_hl}</div></div>'
out+=f'''<section id="documentation" class="dk">{amb()}<div class="wrap wide"><div class="head2"><div>{kicker(I('.sec-kicker',d))}<h2 class="rv">{I('.sec-title',d)}</h2></div><p class="lead rv">{I('.sec-body',d)}</p></div>
<div class="bento stg">{dc}</div></div></section>
'''
# COMPLIANCE
cp=[x for x in L.find_all('section') if x.get('id')=='compliance'][0]
cc=''
for x in cp.select('.comp-card'):
    cc+=f'<div class="bezel s6 rv"><div class="core2"><div class="sicon">{x.select_one("svg").decode()}</div><h3>{I(".comp-head",x)}</h3><p>{I(".comp-body",x)}</p></div></div>'
def vsc(col,cls):
    items=''.join(f'<li><i>{i.select_one(".vs-icon").get_text()}</i><span>{"".join(str(n) for n in i.select_one(".vs-icon").next_siblings).strip()}</span></li>' for i in col.select('.vs-item'))
    return f'<div class="bezel rv"><div class="core2 {cls}"><h4>{I(".vs-head",col)}</h4><ul>{items}</ul></div></div>'
cols=cp.select('.vs-col')
out+=f'''<section id="compliance" class="lt"><div class="wrap wide"><div class="head2"><div>{kicker(I('.sec-kicker',cp))}<h2 class="rv">{I('.sec-title',cp)}</h2></div><p class="lead rv">{I('.sec-body',cp)}</p></div>
<div class="bento stg">{cc}</div>
<div class="vs stg" style="margin-top:18px"><div class="good-wrap">{vsc(cols[0],'bad')}</div><div class="good good-wrap">{vsc(cols[1],'good')}</div></div></div></section>
'''
# PROCESS
pr=S('process'); ps=''
for x in pr.select('.p-step'):
    ps+=f'<div class="step rv"><div class="stepn">{I(".p-step-num",x).zfill(2)}</div><h4>{I(".p-step-head",x)}</h4><p>{I(".p-step-body",x)}</p></div>'
out+=f'''<section id="process" class="st2"><div class="wrap wide"><div class="split hd"><div>{kicker(I('.sec-kicker',pr))}<h2 class="rv">{I('.sec-title',pr)}</h2></div><p class="lead rv">{I('.sec-body',pr)}</p></div>
<div class="steps" style="--n:5">{ps}</div></div></section>
'''
# COMPENSATION
co=S('compensation'); tr=''
for x in co.select('.track-card'):
    rows=''.join(f'<li><b>{I(".track-row-lbl",r)}</b>{I(".track-row-val",r)}</li>' for r in x.select('.track-row'))
    tr+=f'<div class="bezel s6 rv"><div class="core2"><div class="sicon">{x.select_one("svg").decode()}</div><h3>{I(".track-title",x)}</h3><span class="ph">{I(".track-sub",x)}</span><ul class="tick rows">{rows}</ul></div></div>'
vt=''
for x in co.select('.vol-tier'):
    lbl=x.select_one('.vol-tier-lbl').decode_contents()
    vt+=f'<div class="tier{" f" if "t2" in x.get("class",[]) else ""}"><div class="tn">{I(".vol-tier-threshold",x)}</div><div class="tp">{I(".vol-tier-pct",x)}</div><div class="tv">{lbl}</div></div>'
cn=co.select_one('.comp-note')
out+=f'''<section id="compensation" class="dk">{amb()}<div class="wrap wide"><div class="split hd"><div>{kicker(I('.sec-kicker',co))}<h2 class="rv">{I('.sec-title',co)}</h2></div><p class="lead rv">{I('.sec-body',co)}</p></div>
<div class="bento stg">{tr}</div>
<div class="bezel rv" style="margin-top:18px"><div class="core2"><span class="ph">{I('.vol-tier-title',co)}</span><p style="margin-bottom:6px">{I('.vol-tier-sub',co)}</p><div class="tiers vtiers">{vt}</div></div></div>
<p class="note2 rv" style="margin-top:28px;max-width:80ch">{cn.decode_contents()}</p></div></section>
'''
# CTA
cta=[x for x in L.find_all('section') if x.get('id')=='cta'][0]
det=''.join(f'<div class="rv"><b>{I(".cta-detail-val",x)}</b><span>{I(".cta-detail-lbl",x)}</span></div>' for x in cta.select('.cta-detail'))
frm=form(FORMSPREE,'Leveraged Donation — ROI CFO — New Advisor Lead','Leveraged Donation Strategy — ROI CFO','l-',
  select('Client Tax Liability Range','tax_liability',['Select range...','Under $500K','$500K – $1M','$1M – $5M','$5M – $20M','$20M+'],'l-tl'),
  'Send My Advisor Packet','For licensed professionals only. We’ll reply within 24 hours. bryson@roicfo.com','(801) 555-0182')
mailto=cta.select_one('a.btn-primary').get('href')
out+=f'''<section id="cta" class="dk close">{amb()}<div class="wrap wide"><div class="split">
<div>{kicker(I('.sec-kicker',cta))}<h2 class="closeh rv">Start Referring<br><em>Clients Today</em></h2><p class="lead rv">{I('.sec-body',cta)}</p>
<div class="rv" style="margin-top:36px"><span class="ph">{I('.cta-title',cta)}</span><p class="lead" style="margin-top:0">{I('.cta-body',cta)}</p></div>
<div class="rv" style="margin-top:28px">{btn('Email Us Directly',mailto)}</div></div>
<div class="rv"><div class="formbox"><div class="formin"><div class="ftitle">{I('.lead-form-title',cta)}</div>{frm}</div></div></div></div>
<p class="fine2 rv">{I('.cta-legal',cta)}</p><div class="meta4 stg">{det}</div></div></section>
'''
# FOOTER
fo=L.select_one('footer'); fcols=''
for col in fo.select('.footer-links-wrap > div'):
    lk=''.join(f'<a href="{a.get("href")}">{a.decode_contents()}</a>' for a in col.select('a'))
    fcols+=f'<div><h5>{I(".footer-col-title",col)}</h5>{lk}</div>'
out+=f'''<footer>{amb(1)}<div class="wrap wide"><div class="cols"><div>
<a class="logoplate" href="https://roicfo.com" aria-label="ROI CFO"><img src="/assets/brand/roicfo-logo.png" width="545" height="180" alt="ROI CFO"></a>
<div class="tagline">{I('.footer-tagline',fo)}</div></div>{fcols}</div>
<div class="fine">{I('.footer-copy',fo)}</div></div></footer>
<script src="/assets/js/fx.js?v=2"></script>
<script>
{globe}
{countup}
{calc}
</script>
</body>
</html>
'''
import os
os.makedirs('../leveraged-donation',exist_ok=True)
open('../leveraged-donation/index.html','w').write(out)
print(len(out))
