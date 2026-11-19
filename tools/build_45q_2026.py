import sys,os
sys.path.insert(0,'.')
from lib import *
CAL='https://calendly.com/d/dv9z-zgv-63g/roi-cfo-tax-strategy-explainer'
def card(span,n,title,body):
    return f'<div class="bezel {span} rv"><div class="core2"><span class="n g">{n}</span><span class="gl"></span><h3>{title}</h3><p>{body}</p></div></div>'
def table(ths,rows,hl=None):
    h=''.join(f'<th>{x}</th>' for x in ths)
    b=''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)
    return f'<div class="bezel rv" style="margin-top:48px"><div class="core2" style="padding:0;overflow:hidden"><div class="tbl"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div></div></div>'
def sec(id_,cls,k,title,body,lead=''):
    l=f'<p class="lead rv">{lead}</p>' if lead else '<span></span>'
    return f'<section id="{id_}" class="{cls}"><div class="wrap wide"><div class="head2"><div>{kicker(k)}<h2 class="rv">{title}</h2></div>{l}</div>{body}</div></section>\n'
out=head('Section 45Q Tax Credits for 2026 | Adviser Guide | ROI CFO','A dollar of federal tax credit for eighty five cents. How Section 45Q credits are delivered through EstateSpace, what the client receives, and how the strategy stacks with minerals.','/carbon-credits/2026/')
out+=navbar([('What It Is','#what'),('Process','#process'),('Pricing','#pricing'),('Stacking','#stacking'),('Protections','#protections'),('FAQ','#faq')],('Request Packet','#lead-form'),'https://roicfo.com')
stats=''.join(f'<div class="stat rv"><span class="gl"></span><div class="v"><span class="val">{v}</span></div><div class="t">{t}</div></div>' for v,t in [('$1 : $1','Federal tax offset'),('$0.85','Per $1 of credit'),('$2B','2026 supply'),('22+ yrs','EstateSpace experience')])
out+=f'''<header class="hero sm" id="hero">{hero_amb()}
<div class="wrap wide"><div class="hero-grid"><div>
<div class="kicker rv">Section 45Q Carbon Tax Credits | 2026 Tax Season</div>
{h1(["A dollar of federal tax credit","for","<em>eighty five cents.</em>"],'s2')}
<p class="lead rv" style="--d:2">Your client buys a federal Section 45Q tax credit and applies it dollar for dollar against federal income tax. No equity, no K-1, no project to run. EstateSpace handles registration, escrow and delivery.</p>
<div class="cta rv" style="--d:3">{btn('Schedule a Zoom',CAL,'','target="_blank" rel="noopener"')}{btn('Request Packet','#lead-form','ghost')}</div>
</div>
<div class="rv" style="--d:3"><div class="stats stg herostats" style="--cols:2">{stats}</div></div></div></div></header>
'''
out+=marquee(['Dollar for Dollar','Section 45Q','Section 6418','Form 3800','IRS Registered','EstateSpace'])
what=''.join([
 card('s4','01','The credit','A federal income tax credit created for carbon capture and storage. Under Section 6418 the holder can sell it for cash to another taxpayer.'),
 card('s4','02','The buyer','Applies the credit dollar for dollar against federal income tax on Form 3800. A $10M tax bill is paid with about $8.5M. Net savings are $1.5M.'),
 card('s4','03','The delivery','Each credit arrives with serial numbers, a Certificate of Title and Transfer and an IRS registration number. EstateSpace manages the process end to end.')])
out+=sec('what','lt','What it is','One thing is purchased. The credit.',f'<div class="bento stg">{what}</div>','About $2 billion of credits are available for the 2026 tax season, so each purchase is sized to the client\'s liability. The IRS and the Department of Energy confirmed the project met the approval conditions.')
steps=''.join([
 card('s4','Step 01','Registration','Client registration form and ID verification. That is the only paperwork to start.'),
 card('s4','Step 02','Agreements','Placement Agreement, W-9 and Master Purchase Agreement signed. The client\'s CPA reviews first.'),
 card('s4','Step 03','Escrow','Wire instructions arrive by email and text. Funds go to escrow, not to the seller.'),
 card('s4','Step 04','Delivery','The seller delivers the credit and closing package directly to the client. Vintage credits deliver within 20 business days of full payment.'),
 card('s4','Step 05','Filing','The CPA claims the credit on Form 3800 with the registration number and the delivery package.'),
 card('s4','Step 06','Forward credits','EstateSpace works with the client on forward credits for the current year so next year is covered too.')])
out+=sec('process','dk','Process','Six steps from first form to filed credit.',f'<div class="bento stg">{steps}</div>').replace('<section id="process" class="dk">','<section id="process" class="dk">'+amb())
pr=[('$1,000,000','$850,000','+$150,000','17.6%'),('$2,500,000','$2,125,000','+$375,000','17.6%'),('$5,000,000','$4,250,000','+$750,000','17.6%'),('$10,000,000','$8,500,000','+$1,500,000','17.6%'),('$25,000,000','$21,250,000','+$3,750,000','17.6%')]
out+=sec('pricing','lt','Pricing','$0.85 buys $1.00 of federal credit.',table(['Client federal tax','Client pays','Net savings','Savings on spend'],pr),'Every dollar of credit removes a dollar of federal tax. Market range is 70 to 85 cents. Partial amounts are available.')
st=[('$1,000,000','$55,500','$129,750'),('$2,000,000','$111,000','$259,500'),('$5,000,000','$277,500','$648,750'),('$10,000,000','$555,000','$1,297,500')]
out+=sec('stacking','dk','Stacking','Minerals first. Then the credit.',table(['Client income','45Q alone saves','Stacked net savings'],st)+'<p class="note2 rv" style="margin-top:22px;max-width:80ch;color:var(--mute)">Illustrative. 37% federal, 13.3% state, mineral investment at 6% of income, 5x deduction, credits at $0.85. The client\'s CPA models actual brackets.</p>','Minerals shrink taxable income first and reach the state return. The 45Q credit then eliminates the federal tax that remains. The client buys fewer credits to reach zero.').replace('<section id="stacking" class="dk">','<section id="stacking" class="dk">'+amb())
pc=''.join([
 card('s6','01','Escrow','Payment is held in escrow. Vintage credits are paid into escrow at signing. Forward credits release in two stages.'),
 card('s6','02','Seller indemnity','The seller indemnifies for recapture and compliance failures tied to seller matters, including penalties and interest.'),
 card('s4','03','Replace or refund','Invalidated credits are replaced with equal type and vintage, or the price is refunded.'),
 card('s4','04','Triple reserve','For each forward credit sold, the seller generates three.'),
 card('s4','05','Audit and records','Annual third party audit right, IRS cooperation and seven years of record retention.')])
out+=sec('protections','lt','Protections','Built into the Master Purchase Agreement.',f'<div class="bento stg">{pc}</div>')
faq=[('Does the passive activity limit apply?','Counsel\'s opinion is that when the buyer has no ownership of or participation in the project, Section 469 does not apply by reference to that activity. The credit is a general business credit under Section 38.'),
 ('Does it reduce state tax?','No. 45Q is federal only. That is why it stacks with the minerals strategy.'),
 ('What if the client cannot use it all this year?','Unused credit carries forward 20 years and back 1 year under the general business credit rules.'),
 ('How much work is it for the client?','A form, an ID, three signatures and a wire.'),
 ('Can the CPA review everything first?','Yes. The diligence file goes to the client\'s CPA before the client commits.')]
fq=''.join(card('s6','Q',q,a) for q,a in faq)
out+=sec('faq','st2','Adviser FAQ','The questions advisers ask first.',f'<div class="bento stg">{fq}</div>')
fsel=select('Client Federal Tax Liability Range','tax_liability',['Select range...','Under $1M','$1M – $5M','$5M – $15M','$15M – $30M','$30M+'],'cl-tl')
frm=form(FORMSPREE,'45Q 2026 Adviser Guide | ROI CFO | New Advisor Lead','Section 45Q 2026 Adviser Guide | ROI CFO','cl-',fsel,'Request Adviser Packet','Packet includes the adviser briefing and Q&A. We reply the same day.')
out+=f'''<section id="lead-form" class="dk close lead-form">{amb()}<div class="wrap wide"><div class="split">
<div>{kicker('Adviser Packet')}<h2 class="closeh rv">Run a client scenario with us.</h2></div>
<div class="rv"><div class="formbox"><div class="formin"><div class="ftitle">Request the adviser packet</div>{frm}</div></div></div></div></div></section>
<footer>{amb(1)}<div class="wrap wide"><div class="cols" style="grid-template-columns:1fr auto"><div>
<a class="logoplate" href="https://roicfo.com" aria-label="ROI CFO"><img src="/assets/brand/roicfo-logo.png" width="545" height="180" alt="ROI CFO"></a></div>
<div><h5>Navigate</h5><a href="https://roicfo.com">Back to ROI CFO</a><a href="/carbon-credits/">Carbon Credits</a></div></div>
<div class="fine">This page is intended for qualified financial advisors, CPAs and institutional clients. It is not tax, legal or investment advice and does not constitute an offer or solicitation. Examples are illustrative. Consult independent legal counsel and a qualified CPA before executing any agreement.</div></div></footer>
<script src="/assets/js/fx.js?v=3"></script>
</body>
</html>
'''
os.makedirs('../carbon-credits/2026',exist_ok=True)
open('../carbon-credits/2026/index.html','w').write(out)
print(len(out))
