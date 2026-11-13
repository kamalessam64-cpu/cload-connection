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
// ---- explainer-high-energy look: HUD viewfinder frame, seeded film grain, vignette, VIDEO/seek contract ----
function seeded(s){return()=>(s=(s+0x6D2B79F5)|0,s=Math.imul(s^(s>>>15),1|s),s^=s+Math.imul(s^(s>>>7),61|s),((s^(s>>>14))>>>0)/4294967296)}
function addFinish(scenes){ // scenes: [[startTime,'LABEL'],...]
  const top=document.body;
  const vig=mk(top,'abs','',{width:W+'px',height:H+'px',pointerEvents:'none',background:'radial-gradient(ellipse 75% 60% at 50% 50%,transparent 55%,rgba(0,0,0,.38) 100%)',zIndex:50});
  // grain: 6 seeded tiles drawn once, cycled per frame
  const R=seeded(2026),tiles=[];
  for(let k=0;k<6;k++){const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d'),im=g.createImageData(256,256);
    for(let i=0;i<im.data.length;i+=4){const v=R()*255;im.data[i]=im.data[i+1]=im.data[i+2]=v;im.data[i+3]=255}g.putImageData(im,0,0);tiles.push(c.toDataURL())}
  const grain=mk(top,'abs','',{width:W+'px',height:H+'px',pointerEvents:'none',opacity:.07,mixBlendMode:'overlay',zIndex:51});
  const hud=mk(top,'abs','',{width:W+'px',height:H+'px',pointerEvents:'none',zIndex:52,color:'#fff',textShadow:'0 0 4px rgba(0,0,0,.85),0 0 1px #000',fontFamily:"'DejaVu Sans Mono','Liberation Mono',monospace",fontSize:'22px',letterSpacing:'3px',opacity:.8});
  const br=(css)=>mk(hud,'abs','',Object.assign({width:'54px',height:'54px',borderColor:'#fff',borderStyle:'solid',borderWidth:'0',filter:'drop-shadow(0 0 2px rgba(0,0,0,.8))'},css));
  br({left:'34px',top:'34px',borderLeftWidth:'3px',borderTopWidth:'3px'});br({right:'34px',left:'auto',top:'34px',borderRightWidth:'3px',borderTopWidth:'3px'});
  br({left:'34px',bottom:'34px',top:'auto',borderLeftWidth:'3px',borderBottomWidth:'3px'});br({right:'34px',left:'auto',bottom:'34px',top:'auto',borderRightWidth:'3px',borderBottomWidth:'3px'});
  const sc=mk(hud,'abs','',{right:'110px',left:'auto',top:'46px'});
  const lab=mk(hud,'abs','',{left:'110px',bottom:'46px',top:'auto'});
  const tc=mk(hud,'abs','',{right:'110px',left:'auto',bottom:'46px',top:'auto'});
  const tag=mk(hud,'abs','X7PLUS / BLACK FRIDAY',{left:'110px',top:'46px'});
  return function(t){
    grain.style.backgroundImage=`url(${tiles[Math.floor(t*24)%tiles.length]})`;
    let i=0;for(let k=0;k<scenes.length;k++)if(t>=scenes[k][0])i=k;
    sc.textContent=`SCENE ${String(i+1).padStart(2,'0')} / ${String(scenes.length).padStart(2,'0')}`;
    lab.textContent=scenes[i][1];
    const f=Math.floor(t*30)%30,s=Math.floor(t);
    tc.innerHTML=`<span style="color:#ff2a2a">●</span> 00:${String(s).padStart(2,'0')}:${String(f).padStart(2,'0')}`;
  };
}
function contract(scenes){const fin=addFinish(scenes);const r=window.render;window.render=t=>{r(t);fin(t)};window.seek=window.render;window.VIDEO={w:W,h:H,duration:window.DURATION}}
