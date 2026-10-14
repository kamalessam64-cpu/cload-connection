// usage: node render.js <tier: premium|elite> "<Athlete Name>" [photo-path] [out.png]
const {chromium}=require(process.env.PW||'playwright');
const path=require('path');
(async()=>{
 const [tier='premium',name='Athlete Name',photo='',out]=process.argv.slice(2);
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const pg=await b.newPage({viewport:{width:1080,height:1350}});
 const q=new URLSearchParams({tier,name:name.toUpperCase()});if(process.env.POS)q.set('pos',process.env.POS);
 if(photo)q.set('photo','file://'+path.resolve(photo));
 await pg.goto('file://'+path.resolve(__dirname,'template.html')+'?'+q);
 await pg.waitForSelector('body[data-ready]');
 const o=out||`${tier}-${name.replace(/\s+/g,'-').toLowerCase()}.png`;
 await pg.screenshot({path:path.resolve(__dirname,o)});
 await b.close();console.log('saved',o);
})();
