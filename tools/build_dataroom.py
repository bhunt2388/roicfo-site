import sys,os
sys.path.insert(0,'.')
from lib import *
SRC='https://utahseabed.com/data-room'
out=head('Data Room — ROI CFO','Secure data room for qualified advisors and buyers. Geologist reports, claims, SITLA files, appraisals, and tax documentation, hosted by Utah Seabed.','/data-room/')
links=[('Strategies','/#strategies'),('Who We Serve','/#serve'),('For Advisors','/#network'),('Insights','/#insights'),('Data Room','/data-room/')]
out+=navbar(links,('Request Introduction','/#cta'),'/')
out+=f'''<header class="hero sm" id="hero">{hero_amb()}
<div class="wrap wide" style="width:100%"><div class="hero-grid" style="grid-template-columns:1fr"><div>
{kicker('Data Room')}
{h1(['Diligence documents,','<em>in one place.</em>'],'s2')}
<p class="lead rv" style="--d:2">Geologist reports, lab sheets, claims, SITLA files, BLM notices, Form 8283s, charity acceptance letters, tax opinions, and appraisals. The room is hosted by Utah Seabed and is password protected. Enter your password below. If you do not have one, request an introduction.</p>
<div class="cta rv" style="--d:3">{btn('Request Access','/#cta')}{btn('Open in a New Tab',SRC,'ghost','target="_blank" rel="noopener"')}</div>
</div></div></div>
</header>
<section id="room" class="st2" style="padding-top:clamp(40px,6vw,80px);padding-bottom:clamp(60px,8vw,100px)"><div class="wrap wide">
<div class="formbox rv"><div class="formin" style="padding:0;overflow:hidden;background:#fff">
<iframe src="{SRC}" title="Utah Seabed Data Room" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" style="display:block;width:100%;height:max(900px,85vh);border:0;background:#fff"></iframe>
</div></div>
<p class="fnote" style="margin-top:18px;text-align:center">Content is hosted by Utah Seabed at utahseabed.com. Trouble loading the room? <a href="{SRC}" target="_blank" rel="noopener" style="text-decoration:underline">Open it in a new tab</a>.</p>
</div></section>
<footer>{amb(1)}<div class="wrap wide"><div class="cols" style="grid-template-columns:1fr auto"><div>
<a class="logoplate" href="/" aria-label="ROI CFO"><img src="/assets/brand/roicfo-logo.png" width="545" height="180" alt="ROI CFO"></a>
<div class="tagline">Strategic Returns. Responsible Impact.</div></div>
<div><h5>Navigate</h5><a href="/">Back to ROI CFO</a><a href="/#strategies">All Strategies</a><a href="/#cta">Request Introduction</a></div></div>
<div class="fine">Documents in the data room are provided for diligence by qualified advisors, CPAs, and institutional parties. Nothing here is tax, legal, or investment advice or an offer to sell any security. ROI CFO is not a registered investment adviser, broker-dealer, or tax adviser. Confirm current operating documents with Utah Seabed. © 2026 ROI CFO LLC • Utah</div></div></footer>
<script src="/assets/js/fx.js?v=3"></script>
</body>
</html>
'''
os.makedirs('../data-room',exist_ok=True)
open('../data-room/index.html','w').write(out)
print(len(out))
