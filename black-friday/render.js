// usage: PW=<playwright> node render.js opt1 [fps] [workers]  -> frames in $FRAMES/<opt>/00001.jpg, EVENTS in out/<opt>.events.json
const {chromium}=require(process.env.PW||'playwright');
const path=require('path'),fs=require('fs');
(async()=>{
 const opt=process.argv[2],fps=+(process.argv[3]||30),N=+(process.argv[4]||4);
 const dir=path.join(process.env.FRAMES,opt);fs.mkdirSync(dir,{recursive:true});
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const url='file://'+path.resolve(__dirname,opt+'.html');
 const pages=[];for(let i=0;i<N;i++){const pg=await b.newPage({viewport:{width:1080,height:1920}});await pg.goto(url);await pg.waitForSelector('body[data-ready]');pages.push(pg)}
 const dur=await pages[0].evaluate(()=>window.DURATION);
 fs.writeFileSync(path.join(__dirname,'out',opt+'.events.json'),JSON.stringify({dur,events:await pages[0].evaluate(()=>window.EVENTS)}));
 const total=Math.round(dur*fps);let next=0;
 await Promise.all(pages.map(async pg=>{while(true){const i=next++;if(i>=total)break;
   await pg.evaluate(t=>window.render(t),i/fps);
   await pg.screenshot({path:path.join(dir,String(i+1).padStart(5,'0')+'.jpg'),type:'jpeg',quality:92});}}));
 console.log(opt,'frames',total,'dur',dur);await b.close();
})();
