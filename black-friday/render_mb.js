// usage: PW=<playwright> FRAMES=<dir> node render_mb.js opt1 [fps=30] [sub=3] [workers=4] -> out/<opt>_silent.mp4 with motion blur (180° shutter)
const {chromium}=require(process.env.PW||'playwright');
const path=require('path'),fs=require('fs'),{execFileSync}=require('child_process');
(async()=>{
 const opt=process.argv[2],fps=+(process.argv[3]||30),sub=+(process.argv[4]||3),N=+(process.argv[5]||4);
 const dir=path.join(process.env.FRAMES,opt+'-mb');fs.mkdirSync(dir,{recursive:true});
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const url='file://'+path.resolve(__dirname,opt+'.html');
 const pages=[];for(let i=0;i<N;i++){const pg=await b.newPage({viewport:{width:1080,height:1920}});await pg.goto(url);await pg.waitForSelector('body[data-ready]');pages.push(pg)}
 const V=await pages[0].evaluate(()=>window.VIDEO);const total=Math.round(V.duration*fps)*sub;let next=0;
 await Promise.all(pages.map(async pg=>{while(true){const k=next++;if(k>=total)break;const f=Math.floor(k/sub),s=k%sub;
   await pg.evaluate(t=>window.seek(t),(f+(s/sub)*0.5)/fps);
   await pg.screenshot({path:path.join(dir,String(k+1).padStart(6,'0')+'.jpg'),type:'jpeg',quality:92});}}));
 await b.close();
 execFileSync('ffmpeg',['-v','error','-y','-framerate',String(fps*sub),'-i',path.join(dir,'%06d.jpg'),'-vf',`tmix=frames=${sub},select='eq(mod(n\\,${sub})\\,${sub-1})',setpts=N/(${fps}*TB)`,'-r',String(fps),'-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium',path.join(__dirname,'out',opt+'_silent.mp4')]);
 console.log(opt,'silent video',V.duration,'s');
})();
