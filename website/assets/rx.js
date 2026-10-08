/* A Team rx v1: B/A slider sync + stat count-up. No deps; reduced-motion aware. */
(function(d,w){
var RM=w.matchMedia&&w.matchMedia('(prefers-reduced-motion: reduce)').matches;
[].forEach.call(d.querySelectorAll('.rx-ba'),function(f){
  var r=f.querySelector('input');if(!r)return;
  function take(){if(f.classList.contains('rx-ba-user'))return;
    var p=parseFloat(getComputedStyle(f).getPropertyValue('--pos'));
    if(!isNaN(p)){r.value=Math.round(p);f.style.setProperty('--pos',r.value+'%');}
    f.classList.add('rx-ba-user');}
  r.addEventListener('pointerdown',take);r.addEventListener('keydown',take);
  r.addEventListener('input',function(){f.classList.add('rx-ba-user');f.style.setProperty('--pos',r.value+'%');});
});
if(RM||!('IntersectionObserver' in w))return;
function run(el){var s=el.getAttribute('data-count'),t=parseFloat(s),dp=(s.split('.')[1]||'').length,t0=0;
  function f(n){t0=t0||n;var k=Math.min(1,(n-t0)/1100);el.textContent=(t*(1-Math.pow(1-k,3))).toFixed(dp);if(k<1)requestAnimationFrame(f);}
  requestAnimationFrame(f);}
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.unobserve(e.target);run(e.target);}});},{threshold:.5});
[].forEach.call(d.querySelectorAll('[data-count]'),function(el){
  var b=el.getBoundingClientRect();if(b.top<w.innerHeight&&b.bottom>0)return; /* already on screen: keep final value */
  el.style.minWidth=el.offsetWidth+'px';el.textContent=(0).toFixed((el.getAttribute('data-count').split('.')[1]||'').length);io.observe(el);
});
})(document,window);
