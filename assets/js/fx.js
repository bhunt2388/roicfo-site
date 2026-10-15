(function(){
'use strict';
var d=document,root=d.documentElement,reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function $$(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s));}
requestAnimationFrame(function(){requestAnimationFrame(function(){root.classList.add('on-load');});});
/* progress + nav state */
var prog=d.getElementById('progress'),nav=d.querySelector('nav.fl');
function onScroll(){
  var h=root.scrollHeight-root.clientHeight;
  if(prog)prog.style.width=(h>0?root.scrollTop/h*100:0)+'%';
  if(nav)nav.classList.toggle('raised',window.scrollY>30);
  statement();
}
/* mobile menu */
var ham=d.getElementById('hamburger'),mn=d.getElementById('mobile-nav');
if(ham&&mn){ham.addEventListener('click',function(){var o=mn.classList.toggle('open');ham.setAttribute('aria-expanded',o?'true':'false');});
 $$('a',mn).forEach(function(a){a.addEventListener('click',function(){mn.classList.remove('open');ham.setAttribute('aria-expanded','false');});});}
window.closeMobile=function(){if(mn)mn.classList.remove('open');};
/* split statements into words */
var stm=$$('.statement');
stm.forEach(function(el){
  var out=[];
  (function walk(n,hl){
    Array.prototype.slice.call(n.childNodes).forEach(function(c){
      if(c.nodeType===3){c.textContent.split(/(\s+)/).forEach(function(t){
        if(!t)return; if(/^\s+$/.test(t)){out.push(d.createTextNode(' '));return;}
        var s=d.createElement('span');s.className='w'+(hl?' hl':'');s.textContent=t;out.push(s);});}
      else if(c.nodeType===1){walk(c,hl||c.tagName==='EM'||c.tagName==='STRONG');}
    });
  })(el,false);
  el.textContent='';out.forEach(function(n){el.appendChild(n);});
});
function statement(){
  if(!stm.length)return;
  var vh=window.innerHeight;
  stm.forEach(function(el){
    var r=el.getBoundingClientRect(),words=el.querySelectorAll('.w');
    var p=reduce?1:Math.min(1,Math.max(0,(vh*.88-r.top)/(r.height+vh*.35)));
    var n=Math.round(p*words.length*1.02);
    for(var i=0;i<words.length;i++){words[i].classList.toggle('on',i<n);}
  });
}
/* reveal */
$$('.stg').forEach(function(g){$$('.rv',g).forEach(function(el,i){el.style.setProperty('--d',i);});});
var io='IntersectionObserver' in window?new IntersectionObserver(function(es){
  es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target);
    if(e.target.classList.contains('steps')||e.target.classList.contains('vt'))e.target.classList.add('on');}});
},{threshold:.1,rootMargin:'0px 0px -6% 0px'}):null;
$$('.rv,.steps,.vt').forEach(function(el){if(io&&!reduce)io.observe(el);else el.classList.add('on');});
/* table row cascade */
var tio='IntersectionObserver' in window?new IntersectionObserver(function(es){
  es.forEach(function(e){if(!e.isIntersecting)return;tio.unobserve(e.target);
    $$('tbody tr',e.target).forEach(function(tr,i){setTimeout(function(){tr.classList.add('row-in');},i*55);});});
},{threshold:.08}):null;
$$('.tbl').forEach(function(t){if(tio&&!reduce)tio.observe(t);else $$('tbody tr',t).forEach(function(r){r.classList.add('row-in');});});
setTimeout(function(){root.classList.add('rvall');$$('tbody tr').forEach(function(r){r.classList.add('row-in');});},4500);
/* spotlight + magnetic + parallax */
if(!reduce&&window.matchMedia('(hover:hover)').matches){
  $$('.core2,.mc-core').forEach(function(c){c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();c.style.setProperty('--mx',(e.clientX-r.left)+'px');c.style.setProperty('--my',(e.clientY-r.top)+'px');});});
  $$('.btn').forEach(function(b){
    b.addEventListener('pointermove',function(e){var r=b.getBoundingClientRect();b.style.setProperty('--tx',((e.clientX-r.left-r.width/2)*.14).toFixed(1)+'px');b.style.setProperty('--ty',((e.clientY-r.top-r.height/2)*.22).toFixed(1)+'px');});
    b.addEventListener('pointerleave',function(){b.style.setProperty('--tx','0px');b.style.setProperty('--ty','0px');});
  });
  var hero=d.querySelector('.hero');
  if(hero){var pw=$$('.pxw',hero);
    hero.addEventListener('pointermove',function(e){var r=hero.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
      pw.forEach(function(p){var k=parseFloat(p.getAttribute('data-px')||'30');p.style.transform='translate3d('+(x*k).toFixed(1)+'px,'+(y*k).toFixed(1)+'px,0)';});});}
}
window.addEventListener('scroll',onScroll,{passive:true});window.addEventListener('resize',onScroll);
onScroll();setTimeout(onScroll,300);
})();

/* Lead forms: send to /api/lead (Command intake) instead of a plain Formspree post */
(function(){
  document.querySelectorAll('form[action*="formspree.io"],form[data-lead]').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var b=f.querySelector('button[type=submit]'),o=b?b.innerHTML:'';
      if(b){b.textContent='Sending...';b.disabled=true}
      var d=Object.fromEntries(new FormData(f)); d.source=location.pathname;
      fetch('/api/lead',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)})
        .then(function(r){return r.json().then(function(j){return r.ok&&j.ok})})
        .then(function(ok){
          if(ok){
            var nm=((d.first_name||'')+' '+(d.last_name||d.name||'')).trim(),
                cal='https://calendly.com/d/dv9z-zgv-63g/roi-cfo-tax-strategy-explainer?'+new URLSearchParams({name:nm,email:d.email||'',utm_source:'roicfo.com',utm_medium:'site',utm_campaign:'form-success',utm_content:location.pathname}).toString();
            f.innerHTML='<p style="font-size:20px;line-height:1.6;font-family:var(--serif,serif)">Received. We will be in touch within 24 hours.</p><p style="margin:18px 0 14px;line-height:1.6">Want to skip the wait? Pick a time now and we will already have your details.</p><a class="btn" href="'+cal.replace(/"/g,'&quot;')+'" target="_blank" rel="noopener"><span>Book a 20-Minute Explainer</span></a>';
          }
          else{if(b){b.innerHTML=o;b.disabled=false}alert('Something went wrong. Please email bryson@roicfo.com directly.')}
        })
        .catch(function(){if(b){b.innerHTML=o;b.disabled=false}alert('Network error. Please email bryson@roicfo.com directly.')});
    });
  });
})();
