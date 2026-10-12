import re
SITE='https://www.roicfo.com'
ARW='<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>'
def btn(label,href,cls='',attrs=''):
    return f'<a class="btn {cls}" href="{href}" {attrs}><span>{label}</span><span class="ic">{ARW}</span></a>'
def h1(lines,cls=''):
    return f'<h1 class="{cls}">'+''.join(f'<span class="ln"><span style="--d:{i}">{l}</span></span>' for i,l in enumerate(lines))+'</h1>'
def kicker(t,extra=''):
    return f'<div class="kicker rv {extra}">{t}</div>'
def amb(n=2):
    s='<div class="amb" aria-hidden="true"><i class="orb o1"></i>'+('<i class="orb o2"></i>' if n>1 else '')+'<div class="gridbg"></div></div>'
    return s
def hero_amb():
    return ('<div class="pxw" data-px="46" aria-hidden="true"><i class="orb o1"></i><i class="orb o2"></i></div>'
            '<div class="pxw" data-px="-30" aria-hidden="true"><i class="orb o3"></i></div>'
            '<div class="gridbg" aria-hidden="true"></div><div class="arcs pxw" data-px="18" aria-hidden="true"><i></i><i></i></div>')
def head(title,desc,path,extra_head=''):
    url=SITE+path
    return f'''<!DOCTYPE html>
<html lang="en" class="nojs">
<head>
  <script id="vtag-ai-js" async src="https://r2.leadsy.ai/tag.js" data-pid="YnIS0TzjMHYSSJQg" data-version="062024"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="{desc}">
<title>{title}</title>
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ROI CFO">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/brand/roicfo-logo.png">
<link rel="icon" type="image/x-icon" href="/assets/favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
<meta name="theme-color" content="#0B2545">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css?v=2">
{extra_head}
<script>document.documentElement.className='js';</script>
</head>
<body>
<div id="progress"></div>
'''
def navbar(links,cta,logo_href='/'):
    a=''.join(f'<a class="t" href="{h}">{t}</a>' for t,h in links)
    m=''.join(f'<a href="{h}">{t}</a>' for t,h in links)+f'<a href="{cta[1]}">{cta[0]}</a>'
    return f'''<nav class="fl" aria-label="Primary"><div class="in">
<a class="mark" href="{logo_href}" aria-label="ROI CFO home"><img class="full" src="/assets/brand/roicfo-logo.png" width="545" height="180" alt="ROI CFO"></a>
<div class="links">{a}{btn(cta[0],cta[1],'sm cta-d')}</div>
<button class="hamburger" id="hamburger" aria-label="Open menu" aria-expanded="false"><span></span><span></span></button>
</div></nav>
<div class="mobile-nav" id="mobile-nav">{m}</div>
'''
def marquee(words):
    w=''.join(f'<span>{x}</span>' for x in words)
    return f'<div class="marq" aria-hidden="true"><div class="track">{w}{w}</div></div>'
def field(label,name,ph='',typ='text',req=True,fid=''):
    r=' required' if req else ''
    return f'<div><label class="l" for="{fid}">{label}</label><input id="{fid}" name="{name}" placeholder="{ph}" type="{typ}"{r}></div>'
def select(label,name,opts,fid):
    o=''.join(f'<option>{x}</option>' for x in opts)
    return f'<div><label class="l" for="{fid}">{label}</label><select id="{fid}" name="{name}"><option value="">{opts[0]}</option>{o[len("<option>"+opts[0]+"</option>"):]}</select></div>'
def role_sel(fid):
    return select('Your Role','role',['Select...','CPA / Tax Partner','RIA / Financial Advisor','CFP','CFO / Business Manager','Family Office','Other'],fid)
def form(action,subject,product,prefix,sel_extra,btn_label,note,ph_phone='(801) 555-0100',extra_before_btn=''):
    return f'''<form action="{action}" method="POST">
<input name="_subject" type="hidden" value="{subject}"/>
<input name="product" type="hidden" value="{product}"/>
<div class="frow">{field('First Name','first_name','Jane',fid=prefix+'fn')}{field('Last Name','last_name','Smith',fid=prefix+'ln')}</div>
<div class="frow">{field('Email','email','jane@smithcpa.com','email',fid=prefix+'em')}{field('Phone (optional)','phone',ph_phone,'tel',False,fid=prefix+'ph')}</div>
<div class="frow">{field('Firm Name','firm','Smith CPA Group',fid=prefix+'fm')}{role_sel(prefix+'rl')}</div>
{sel_extra}
<button class="btn" type="submit"><span>{btn_label}</span><span class="ic">{ARW}</span></button>
<p class="fnote">{note}</p>
</form>'''
FORMSPREE='https://formspree.io/f/xdarooko'
def footer_close(inner):
    return f'<footer>{amb(1)}<div class="wrap">{inner}</div></footer>\n'
