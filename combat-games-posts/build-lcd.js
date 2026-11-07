// usage: PW=<playwright path> node build-lcd.js   -> lcd/NN-<design>-<name>.png
const {chromium}=require(process.env.PW||'playwright');
const path=require('path'),fs=require('fs');
const T={signature:'signature-land.html',hyrox:'hyrox-land.html',podium:'podium-land.html'};
(async()=>{
 const slides=JSON.parse(fs.readFileSync(path.join(__dirname,'slides.json')));
 const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const pg=await b.newPage({viewport:{width:1920,height:1080}});
 const files=[];
 for(const [i,s] of slides.entries()){
  const q=new URLSearchParams({name:s.name.toUpperCase(),photo:'file://'+path.resolve(__dirname,s.photo)});
  for(const k of ['pos','zoom','origin','div','tag','cat','comp']) if(s[k]!==undefined) q.set(k,s[k]);
  await pg.goto('file://'+path.resolve(__dirname,T[s.d])+'?'+q);
  await pg.waitForSelector('body[data-ready]');
  await pg.waitForTimeout(150);
  const f=`lcd/${String(i+1).padStart(2,'0')}-${s.d}-${s.name.toLowerCase().replace(/\s+/g,'-')}.png`;
  await pg.screenshot({path:path.join(__dirname,f)});
  files.push(f);console.log(f);
 }
 fs.writeFileSync(path.join(__dirname,'lcd/slides.json'),JSON.stringify(files.map(f=>path.basename(f))));
 await b.close();
})();
