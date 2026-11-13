// usage: node preview.js opt1 t1,t2,...  -> still frames for checking
const {chromium}=require(process.env.PW);const path=require('path');
(async()=>{const [opt,ts]=process.argv.slice(2);const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const pg=await b.newPage({viewport:{width:1080,height:1920}});const errs=[];pg.on('pageerror',e=>errs.push(e.message));
await pg.goto('file://'+path.resolve(__dirname,opt+'.html'));await pg.waitForSelector('body[data-ready]');
for(const t of ts.split(',')){await pg.evaluate(t=>window.render(t),+t);await pg.screenshot({path:path.join(process.env.FRAMES,`${opt}-t${t}.png`)})}
console.log('errors:',errs);await b.close()})();
