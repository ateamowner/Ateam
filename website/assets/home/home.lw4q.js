/* A Team draft homepage: scroll-scrubbed real job footage. Same technique as the TL draft:
   lw3: a looping <video> plays the film at native frame rate; scroll drives text, scrims and a light zoom. Lenis + one rAF loop. */
(function(){
'use strict';
var doc=document.documentElement, $=function(s,c){return (c||document).querySelector(s)}, $$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
var RM=window.matchMedia('(prefers-reduced-motion: reduce)').matches || /[?&]still\b/.test(location.search);
var clamp=function(v,a,b){return v<a?a:v>b?b:v}, lerp=function(a,b,t){return a+(b-a)*t};
var ss=function(a,b,v){var t=clamp((v-a)/(b-a),0,1);return t*t*(3-2*t)};
var BG='#0b0f14';
/* Bump this folder name whenever the footage changes. /assets is cached for a week, so reusing a path shows stale footage. */
var FILM_BASE='/assets/film-lw4/';
var isMobile=function(){return Math.min(innerWidth,screen.width||innerWidth)<=900 && innerHeight>innerWidth*0.9};
var MOB=isMobile();
/* lw3+: the film is a real <video> (H.264 1080p 30fps, HEVC first where supported) that plays at native frame rate.
   No scroll-scrubbing currentTime and no frame preloading: iOS Safari stutters on both. Scroll only drives text, scrims and a light zoom. */
var VID=MOB?{w:1080,h:1920,h264:'m-1080.mp4',hevc:'m-1080.hevc.mp4',poster:'m-poster.jpg'}:{w:1088,h:870,h264:'d-1088.mp4',hevc:'d-1088.hevc.mp4',poster:'d-poster.jpg'};
var SRC=[VID.w,VID.h], CLIP_S=8.7, NS=261;
var SHOT=/[?&]shot\b/.test(location.search);
function pad(n,l){n=String(n);while(n.length<l)n='0'+n;return n}

/* ---------- menu ---------- */
var mb=$('.menu-btn'), drawer=$('#drawer');
if(mb&&drawer){mb.addEventListener('click',function(){var o=drawer.hasAttribute('hidden');if(o){drawer.removeAttribute('hidden')}else{drawer.setAttribute('hidden','')}mb.setAttribute('aria-expanded',o?'true':'false');mb.textContent=o?'Close':'Menu';doc.classList.toggle('menu-open',o)})}

/* ---------- loader: done as soon as the first video frame is ready (2.5 s fallback) ---------- */
var ready=false, loaderVal=$('.loader__val'), loaderFr=$('.loader__frames'), loaderBar=$('.loader__bar i'), loader=$('.loader');
function setLoader(pct){if(loaderVal)loaderVal.textContent=pad(pct,3);if(loaderBar)loaderBar.style.width=pct+'%'}
function done(){if(ready)return;ready=true;setLoader(100);if(loaderFr)loaderFr.textContent='FILM READY';setTimeout(function(){if(loader)loader.classList.add('done');doc.classList.add('is-ready')},150);needs=true}
/* ---------- reduced motion: still poster, no scrub ---------- */
if(RM){
  doc.classList.add('rm'); if(loader)loader.classList.add('done');
  $$('.reveal-words').forEach(function(el){el.style.opacity=1});
  return;
}

/* ---------- smooth scroll (wheel); native touch on phones ---------- */
var lenis=null;
if(window.Lenis){try{lenis=new Lenis({lerp:0.085,smoothWheel:true,wheelMultiplier:0.9})}catch(e){lenis=null}}
$$('a[href^="#"]').forEach(function(a){a.addEventListener('click',function(e){var id=a.getAttribute('href');var t=id==='#top'?document.body:$(id);if(!t)return;e.preventDefault();
  if(lenis)lenis.scrollTo(id==='#top'?0:t,{duration:1.6});else window.scrollTo({top:id==='#top'?0:t.getBoundingClientRect().top+scrollY,behavior:'smooth'})})});

/* ---------- video ---------- */
var film=$('.film'), stage=$('.film__stage'), vid=$('.film__video');
var scrimL=$('.film__scrim--l'),scrimR=$('.film__scrim--r'),tint=$('.film__tint'),shade=$('.film__shade'),frEl=$('.film__fr'),tcEl=$('.film__tc'),progEl=$('.film__prog i');
var W=0,H=0,needs=true,inView=true,playing=false;
function size(){var w=stage.clientWidth,h=stage.clientHeight;if(w!==W||h!==H){W=w;H=h;needs=true}}
function setupVideo(){
  if(!vid)return;
  vid.muted=true;vid.defaultMuted=true;vid.playsInline=true;vid.setAttribute('playsinline','');vid.setAttribute('webkit-playsinline','');
  vid.poster=FILM_BASE+VID.poster;
  /* perf: the loader clears right away; the poster (preloaded in <head>) and then the video fade in behind the hero text */
  done();
  var hv=document.createElement('source');hv.src=FILM_BASE+VID.hevc;hv.type='video/mp4; codecs="hvc1"';
  var av=document.createElement('source');av.src=FILM_BASE+VID.h264;av.type='video/mp4; codecs="avc1.640029"';
  /* HEVC only where the browser says it can play it (Safari/iOS); everyone else gets H.264 */
  /* perf: attach the sources after window load so the ~5 MB video never competes with the first paint (poster shows until then) */
  var attach=function(){if(vid.firstChild)return;if(hv.type&&vid.canPlayType(hv.type)==='probably')vid.appendChild(hv);vid.appendChild(av);vid.load();sync()};
  if(document.readyState==='complete')setTimeout(attach,0);else window.addEventListener('load',function(){setTimeout(attach,0)});
  vid.addEventListener('loadeddata',done);vid.addEventListener('canplay',done);
  vid.addEventListener('progress',function(){if(ready)return;try{var b=vid.buffered;if(b.length)setLoader(Math.min(99,Math.round(b.end(b.length-1)/CLIP_S*100)))}catch(e){}});
  vid.addEventListener('playing',function(){playing=true});vid.addEventListener('pause',function(){playing=false});
  vid.addEventListener('timeupdate',function(){var t=vid.currentTime||0;if(frEl)frEl.textContent='FR '+pad(Math.min(NS,Math.floor(t*30)+1),3)+' / '+NS;if(tcEl)tcEl.textContent='TC 00:'+pad(Math.floor(t),2)+' / 00:08'});
  setTimeout(done,1200);
  if('IntersectionObserver' in window){new IntersectionObserver(function(es){es.forEach(function(e){inView=e.isIntersecting;sync()})},{threshold:0}).observe(film)}
  document.addEventListener('visibilitychange',sync);
  /* iOS Low Power Mode blocks muted autoplay: start on the first tap instead */
  var kick=function(){sync();if(!vid.paused){window.removeEventListener('touchend',kick);window.removeEventListener('click',kick)}};
  window.addEventListener('touchend',kick,{passive:true});window.addEventListener('click',kick);
  sync();
}
function sync(){if(!vid)return;var want=inView&&!document.hidden;
  if(want&&vid.paused){var p=vid.play();if(p&&p.catch)p.catch(function(){})}else if(!want&&!vid.paused){vid.pause()}}

/* light zoom on scroll (GPU transform on the video; the camera move itself is in the clip) */
var ZK=[[0,1.0],[0.1,1.0],[0.27,1.06],[0.67,1.1],[0.88,1.04],[1,1.0]];
function zoomAt(p){for(var i=0;i<ZK.length-1;i++){if(p<=ZK[i+1][0]){var a=ZK[i],b=ZK[i+1];return lerp(a[1],b[1],ss(a[0],b[0],p))}}return 1}
/* lw4 = Anthony's real iPhone footage (src 12.3-22.0 s). Callout anchors normalized over the full 1088x1920 portrait clip: streak lines left of the vent, the window run, the long drips below */
var PTS={streaks:[.22,.5],spray:[.6,.42],rinse:[.42,.6]}, OPX=.5;
function toSrc(u,v){ if(MOB) return [u*SRC[0], v*SRC[1]]; return [u*SRC[0],((v*1920-620)/870)*SRC[1]] }
function xf(z){ var s=Math.max(W/SRC[0],H/SRC[1]), dw=SRC[0]*s, dh=SRC[1]*s; return {s:s,z:z,dx:(W-dw)*OPX,dy:(H-dh)*0.5} }
function project(u,v,T){var sc=toSrc(u,v),x=T.dx+sc[0]*T.s,y=T.dy+sc[1]*T.s;return [W/2+(x-W/2)*T.z, H/2+(y-H/2)*T.z]}
var lastZ=-1;
function drawFilm(p){
  var z=zoomAt(p), T=xf(z);
  if(Math.abs(z-lastZ)>0.0004||needs){lastZ=z;vid.style.transform='translate3d(0,0,0) scale('+z.toFixed(4)+')'}
  return T;
}

/* ---------- beats ---------- */
var beats=$$('.beat').map(function(el){return {el:el,a:+el.dataset.in,b:+el.dataset.out,pt:el.dataset.pt,
  dot:$('.call__dot',el),line:$('.call__line',el),box:$('.call__box',el),lines:$$('.offer__line',el).map(function(l){return {el:l,at:+l.dataset.at}})}});
var hwA=$('.hw--a'),hwB=$('.hw--b'),heroLine=$('.hero__line'),heroCta=$('.hero__cta'),cue=$('.scrollcue');
function beatsUpdate(p,T){
  beats.forEach(function(B){
    var F=0.026, inA=B.a<0?1:ss(B.a,B.a+F,p), outA=1-ss(B.b-F,B.b,p), a=inA*outA, el=B.el;
    if(a<=0.001){if(el.style.opacity!=='0'){el.style.opacity='0';el.style.visibility='hidden'}return}
    el.style.visibility='visible';el.style.opacity=a.toFixed(3);
    if(el.classList.contains('beat--hero')){
      var e=ss(0,B.b,p);
      hwA.style.transform='translate3d('+(-e*16)+'vw,0,0) scale('+(1+e*0.2)+')';
      hwB.style.transform='translate3d('+(e*16)+'vw,0,0) scale('+(1+e*0.2)+')';
      heroLine.style.transform='translate3d(0,'+(e*30)+'px,0)';
      if(heroCta){heroCta.style.transform='translate3d(0,'+(e*40)+'px,0)';heroCta.style.pointerEvents=e<0.3?'auto':'none'}
      cue.style.opacity=(1-ss(0,0.02,p)).toFixed(2);
      el.style.filter=e>0.05?'blur('+(e*6).toFixed(1)+'px)':'none';
      return;
    }
    var dir=p<(B.a+B.b)/2?1:-1, y=(1-a)*36*dir;
    if(B.pt){
      var an=PTS[B.pt], pt=project(an[0],an[1],T);
      B.dot.style.left='0';B.dot.style.top='0';B.dot.style.transform='translate3d('+pt[0]+'px,'+pt[1]+'px,0)';
      if(!B.bw){B.bw=B.box.offsetWidth;B.bh=B.box.offsetHeight}var bx,by,bw=B.bw,bh=B.bh;
      if(MOB){bx=W*0.07;by=H*0.66;if(by+bh>H-80)by=H-80-bh;if(pt[1]>by-40)by=Math.max(90,pt[1]-bh-120)}
      else{var right=pt[0]<W*0.5;bx=right?Math.max(pt[0]+W*0.14,W*0.52):Math.min(pt[0]-W*0.14-bw,W*0.44-bw);by=H*0.5-bh*0.5}
      B.box.style.left='0';B.box.style.top='0';B.box.style.transform='translate3d('+bx+'px,'+(by+y)+'px,0)';
      var tx=MOB?bx+20:(bx>pt[0]?bx-14:bx+bw+14), ty=MOB?(by>pt[1]?by-14:by+bh+14):by+bh*0.2;
      var dx=tx-pt[0],dy=ty-pt[1],len=Math.sqrt(dx*dx+dy*dy),ang=Math.atan2(dy,dx),grow=ss(B.a,B.a+0.04,p);
      B.line.style.width=(len*grow)+'px';B.line.style.left='0';B.line.style.top='0';
      B.line.style.transform='translate3d('+pt[0]+'px,'+pt[1]+'px,0) rotate('+ang+'rad)';
      return;
    }
    if(B.lines.length){
      B.lines.forEach(function(L){var k=ss(L.at,L.at+0.022,p);L.el.style.opacity=k.toFixed(3);L.el.style.transform='translate3d('+((1-k)*-9)+'vw,0,0) skewX('+((1-k)*-12)+'deg)'});
      el.style.transform='translate3d(0,'+(dir<0?y:0)+'px,0)';return;
    }
    el.style.transform='translate3d(0,'+y+'px,0)';
  });
}

/* ---------- sections ---------- */
var hudVal=$('.hud__val'),hudFill=$('.hud__fill'),hudNeedle=$('.hud__needle'),stages=$$('.hud__stages li');
var gradeEls=[film].concat($$('[data-bg]')),grade=[];
function hex(h){h=h.replace('#','');return [parseInt(h.substr(0,2),16),parseInt(h.substr(2,2),16),parseInt(h.substr(4,2),16)]}
var words=[];$$('.reveal-words').forEach(function(el){var t=el.textContent.trim().split(/\s+/);el.innerHTML=t.map(function(w){return '<span class="w">'+w+'</span>'}).join(' ');words.push({el:el,w:$$('.w',el)})});
var svcRows=$$('.svc__row'),towns=$$('.towns a'),cols=$$('.grid__col'),pieces=$('.pieces'),how=$('.how'),path=$('.how__thread path'),howNums=$$('.how__n');
var wipe=$('.wipe'),pairs=$$('.wipe__pair').map(function(el){return {el:el,a:+el.dataset.a,b:+el.dataset.b,after:$('.wipe__after',el),line:$('.wipe__line',el)}}),tagB=$('.wipe__tb'),tagA=$('.wipe__ta');
var endSec=$('.end'),endWords=$$('.end__text span'),strip=$('.strip'),scv=$('.strip__canvas'),sctx=scv.getContext('2d',{alpha:false});
var pathLen=path?path.getTotalLength():0;if(path){path.style.strokeDasharray=pathLen;path.style.strokeDashoffset=pathLen}
var layout={};
function measure(){
  size();var y=scrollY;layout.filmTop=film.getBoundingClientRect().top+y;layout.filmLen=film.offsetHeight-stage.offsetHeight;
  layout.vh=innerHeight;layout.docH=document.documentElement.scrollHeight;
  grade=gradeEls.map(function(el){return {y:el.getBoundingClientRect().top+y,c:hex(el===film?BG:el.dataset.bg)}});
  layout.wipeTop=wipe.getBoundingClientRect().top+y;layout.wipeLen=wipe.offsetHeight-layout.vh;
  var r=strip.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,2);scv.width=Math.round(r.width*d);scv.height=Math.round(r.height*d);stripLast=-1;
  beats.forEach(function(B){B.bw=0});
  needs=true;
}
function secProg(el,vh){var r=el.getBoundingClientRect();return clamp((vh-r.top)/(r.height+vh),0,1)}
var curBg='';
function sections(y,pFilm){
  var vh=layout.vh,mid=y+vh*0.6,c=grade[0].c;
  for(var i=0;i<grade.length-1;i++){var A=grade[i],B=grade[i+1];if(mid>=A.y){var t=ss(B.y-vh*0.5,B.y+vh*0.1,mid);c=[lerp(A.c[0],B.c[0],t),lerp(A.c[1],B.c[1],t),lerp(A.c[2],B.c[2],t)]}}
  var bg='rgb('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+')';if(bg!==curBg){curBg=bg;document.body.style.backgroundColor=bg;document.body.style.setProperty('--bg',bg)}
  words.forEach(function(W_){var r=W_.el.getBoundingClientRect();if(r.bottom<-50||r.top>vh+50)return;var k=clamp((vh*0.85-r.top)/(r.height+vh*0.35),0,1)*W_.w.length*1.08;W_.w.forEach(function(w,i){w.style.opacity=(0.12+0.88*clamp(k-i,0,1)).toFixed(2)})});
  svcRows.forEach(function(row,i){var r=row.getBoundingClientRect();if(r.bottom<-50||r.top>vh+50)return;var cy=(r.top+r.height/2)/vh-0.5;
    row.children[1].style.transform='translate3d('+((i%2?1:-1)*cy*-7)+'vw,0,0)';row.classList.toggle('on',Math.abs(cy)<0.15)});
  towns.forEach(function(a){var r=a.getBoundingClientRect();if(r.bottom<-50||r.top>vh+50)return;var cy=(r.top+r.height/2)/vh-0.5;a.classList.toggle('on',Math.abs(cy)<0.12)});
  // before/after wipe
  var pw=clamp((y-layout.wipeTop)/Math.max(1,layout.wipeLen),0,1), wipeAmt=0;
  pairs.forEach(function(P,i){var t=clamp((pw-P.a)/(P.b-P.a),0,1),last=i===pairs.length-1;
    var vis=(i===0?1:ss(0,0.1,t))*(last?1:1-ss(0.9,1,t));
    P.el.style.opacity=vis.toFixed(3);
    var w=ss(0.14,0.78,t); if(vis>0.5)wipeAmt=w;
    P.after.style.clipPath='inset(0 0 0 '+((1-w)*100).toFixed(2)+'%)';P.line.style.left=((1-w)*100).toFixed(2)+'%';
    P.line.style.opacity=(w>0.002&&w<0.998)?1:0;
    P.el.style.transform=(MOB?'':'translateY(-50%) ')+'scale('+(0.96+0.04*vis).toFixed(3)+')';
  });
  if(tagB){tagB.classList.toggle('on',wipeAmt<0.5);tagA.classList.toggle('on',wipeAmt>=0.5)}
  var pp=secProg(pieces,vh);cols.forEach(function(col){var sp=+col.dataset.speed*(MOB?0.5:1);col.style.transform='translate3d(0,'+((pp-0.5)*sp)+'px,0)'});
  if(path){var hp=clamp((vh*0.8-how.getBoundingClientRect().top)/(how.offsetHeight*0.75),0,1);path.style.strokeDashoffset=(pathLen*(1-hp)).toFixed(1);
    howNums.forEach(function(n,i){n.style.color=hp>(i+0.6)/3.4?'var(--ink)':'transparent'})}
  var sr=strip.getBoundingClientRect();if(sr.bottom>0&&sr.top<vh)drawStrip(clamp((vh-sr.top)/(sr.height+vh),0,1));
  var er=endSec.getBoundingClientRect(),ek=clamp((vh*0.9-er.top)/(er.height*0.7),0,1)*endWords.length*1.1;
  endWords.forEach(function(w,i){var k=clamp(ek-i,0,1);w.style.opacity=(0.07+0.93*k).toFixed(2);w.style.transform='translate3d(0,'+((1-k)*0.12)+'em,0)'});
  // HUD: rinse progress through the reel, then holds at 100
  var pct=Math.round(pFilm*100);hudVal.textContent=pad(pct,3);
  var f=pFilm;hudFill.style.transform='scaleY('+f+')';hudNeedle.style.top=(f*100)+'%';
  var st=pFilm<0.26?0:pFilm<0.55?1:pFilm<0.9?2:3;stages.forEach(function(li,i){li.classList.toggle('on',i===st)});
}
var stripLast=-1, stripImg=new Image(); stripImg.decoding='async'; stripImg.onload=function(){stripLast=-1;needs=true}; stripImg.src=FILM_BASE+'strip.jpg';
function drawStrip(k){
  if(!stripImg.complete||!stripImg.naturalWidth)return; var key=Math.round(k*400); if(key===stripLast)return; stripLast=key;
  var w=scv.width,h=scv.height,iw=stripImg.naturalWidth,ih=stripImg.naturalHeight; sctx.fillStyle=BG;sctx.fillRect(0,0,w,h);
  var s=Math.max(w/iw,h/ih)*1.15, dw=iw*s, dh=ih*s; sctx.drawImage(stripImg,(w-dw)*k,(h-dh)/2,dw,dh);
}

/* ---------- services hover peek (desktop) ---------- */
var peek=$('.svc__peek'),peekImg=peek&&$('img',peek);
if(peek&&window.matchMedia('(hover:hover)').matches){
  window.addEventListener('mousemove',function(e){peek.style.left=e.clientX+'px';peek.style.top=e.clientY+'px'},{passive:true});
  svcRows.forEach(function(r){r.addEventListener('mouseenter',function(){peekImg.src=r.dataset.img;peek.classList.add('show')});r.addEventListener('mouseleave',function(){peek.classList.remove('show')})});
}

/* ---------- main loop ---------- */
var pS=0,lastT=performance.now(),barState='',dockState='';
function tick(now){
  requestAnimationFrame(tick);
  var dt=Math.min(64,now-lastT);lastT=now;if(lenis)lenis.raf(now);
  var y=scrollY;
  /* idle: nothing moved and the film has settled, skip the frame's work */
  if(y===lastY&&!needs&&settled)return;
  lastY=y;
  try{step(y,dt)}catch(e){if(!tickErr){tickErr=1;if(window.console)console.error(e)}}
  needs=false;
}
var lastY=-1,settled=false,tickErr=0;
function step(y,dt){
  var pRaw=clamp((y-layout.filmTop)/Math.max(1,layout.filmLen),0,1);
  var k=1-Math.pow(1-(lenis&&!MOB?0.35:0.2),dt/16.7);settled=(SHOT||Math.abs(pRaw-pS)<0.00005);pS=settled?pRaw:lerp(pS,pRaw,k);
  if(y<layout.filmTop+layout.filmLen+layout.vh){
    var T=drawFilm(pS);beatsUpdate(pS,T);
    shade.style.opacity=(Math.max((MOB?0.62:0.7)*(1-ss(0.085,0.17,pS)),0.9*ss(0.955,1,pS))).toFixed(3);
    tint.style.opacity=(0.78*ss(0.675,0.72,pS)*(1-ss(0.88,0.96,pS))).toFixed(3);
    if(!MOB){
      scrimL.style.opacity=(Math.max(ss(0.10,0.13,pS)*(1-ss(0.22,0.245,pS)),ss(0.685,0.71,pS)*(1-ss(0.86,0.885,pS)))).toFixed(3);
      scrimR.style.opacity=(Math.max(ss(0.26,0.29,pS)*(1-ss(0.38,0.40,pS)),ss(0.56,0.59,pS)*(1-ss(0.66,0.68,pS)))*0.85).toFixed(3);
    }else{
      scrimL.style.opacity=(Math.max(ss(0.10,0.13,pS)*(1-ss(0.22,0.245,pS)),ss(0.685,0.71,pS)*(1-ss(0.86,0.885,pS)))).toFixed(3);
      scrimR.style.opacity=(Math.max(ss(0.26,0.29,pS)*(1-ss(0.65,0.68,pS)))*0.9).toFixed(3);
    }
    progEl.style.transform='scaleX('+pS.toFixed(4)+')';
  }
  sections(y,pS);
  var bb=y>layout.filmTop+layout.filmLen+layout.vh*0.5?'1':'0';if(bb!==barState){barState=bb;doc.style.setProperty('--barbg',bb)}
  var dk=y>layout.filmTop+layout.filmLen*0.96?'1':'0';if(dk!==dockState){dockState=dk;doc.classList.toggle('dock-on',dk==='1')}
}

/* ---------- boot ---------- */
var rw=innerWidth;
window.addEventListener('resize',function(){if(Math.abs(innerWidth-rw)>2||!MOB){rw=innerWidth;measure()}else{size();measure()}});
window.addEventListener('orientationchange',function(){setTimeout(measure,300)});
window.addEventListener('load',measure);
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(measure);
document.addEventListener('toggle',function(){setTimeout(measure,50)},true);
measure();setupVideo();requestAnimationFrame(tick);
window.__at={get p(){return pS},video:vid,lenis:lenis,layout:layout,ready:function(){return ready}};
})();
