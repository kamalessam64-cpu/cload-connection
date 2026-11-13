// Deterministic frame-by-frame animation helpers. Every scene is a pure function of time t (seconds).
const W=1080,H=1920;
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const E={lin:x=>x,out:x=>1-Math.pow(1-x,3),expo:x=>x>=1?1:1-Math.pow(2,-10*x),
  back:x=>{const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)},
  inOut:x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2,in:x=>x*x*x};
const P=(t,t0,d,fn=E.out)=>fn(clamp((t-t0)/d));          // eased progress 0..1
const pulse=(t,t0,k=.25)=>t<t0?0:Math.exp(-(t-t0)/k);       // 1 at hit, decays
const rnd=(n)=>{const s=Math.sin(n*127.1+311.7)*43758.5453;return s-Math.floor(s)};
const shake=(t,t0,d,amp)=>{if(t<t0||t>t0+d)return[0,0];const k=1-(t-t0)/d,n=Math.floor(t*60);return[(rnd(n)-.5)*2*amp*k,(rnd(n+99)-.5)*2*amp*k]};
function mk(parent,cls,html,css){const e=document.createElement('div');e.className=cls||'';if(html!=null)e.innerHTML=html;if(css)Object.assign(e.style,css);parent.appendChild(e);return e}
function tf(e,o){o=o||{};const x=o.x||0,y=o.y||0,s=o.s==null?1:o.s,r=o.r||0,k=o.k||0;
  e.style.transform=`translate(${x}px,${y}px) rotate(${r}deg) skewX(${k}deg) scale(${s})`;
  if(o.o!=null)e.style.opacity=o.o;}
const vis=(e,on)=>{e.style.display=on?'':'none'};
const logoImg=(parent,src,w)=>{const i=new Image();i.src=src;i.style.width=w+'px';i.className='abs';parent.appendChild(i);return i};
async function ready(){await document.fonts.ready;await Promise.all([...document.images].map(i=>i.complete?1:new Promise(r=>{i.onload=i.onerror=r})));document.body.dataset.ready=1}
function textW(e){const r=document.createRange();r.selectNodeContents(e);return r.getBoundingClientRect().width}
function fit(e,max=1000){let f=parseFloat(getComputedStyle(e).fontSize);let n=0;while(textW(e)>max&&f>30&&n++<80){f*=.97;e.style.fontSize=f+'px'}}
function centerX(e,dx=0){e.style.left=((W-e.offsetWidth)/2+dx)+'px'}
