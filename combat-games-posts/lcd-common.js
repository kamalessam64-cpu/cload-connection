function fit(el,maxW,base){const sp=el.firstChild;let f=base;el.style.fontSize=f+'px';while(sp.offsetWidth>maxW&&f>40){f-=2;el.style.fontSize=f+'px'}}
function setPhoto(p,imgId,phId){const ph=p.get('photo');const i=document.getElementById(imgId);
 if(!ph){document.body.dataset.ready=1;return}
 i.onload=()=>{i.style.display='block';if(phId)document.getElementById(phId).style.display='none';document.body.dataset.ready=1};
 i.onerror=()=>document.body.dataset.ready=1;
 i.style.transform='scale('+(p.get('zoom')||1)+')';i.style.transformOrigin=p.get('origin')||'50% 50%';i.style.objectPosition=p.get('pos')||'50% 50%';i.src=ph}
function twoLines(name){const parts=name.split(' ');const last=parts.length>1?parts.pop():'';return [parts.join(' '),last]}
