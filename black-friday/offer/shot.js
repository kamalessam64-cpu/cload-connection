const {chromium}=require(process.env.PW);const path=require('path');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
for(const [fmt,h] of [['post',1350],['story',1920]]){const pg=await b.newPage({viewport:{width:1080,height:h}});
await pg.goto('file://'+path.resolve(__dirname,'offer.html')+'?fmt='+fmt);await pg.waitForSelector('body[data-ready]');
await pg.screenshot({path:path.resolve(__dirname,'../final/X7-Black-Friday-Offer-'+(fmt==='post'?'Post-4x5':'Story-9x16')+'.png')});await pg.close()}
await b.close()})();
