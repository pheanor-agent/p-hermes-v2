/* Verify website navigation, scene links, media controls and local-file playback. */
const fs=require('node:fs'),path=require('node:path'),{pathToFileURL}=require('node:url');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),out=path.join(root,'.work/web-review');fs.mkdirSync(out,{recursive:true});
const base=process.env.WEB_BASE||'http://127.0.0.1:8769';
let browser;
(async()=>{
 browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||undefined});
 const page=await browser.newPage({viewport:{width:1280,height:900}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const report={base,views:[],media:[],errors};
 for(const width of [1280,390]){
  await page.setViewportSize({width,height:width===1280?900:844});
  for(const [name,url] of [['home','/index.html'],['lectures','/lectures/index.html'],['course','/lectures/tasks.html'],['guide','/lectures/guide.html'],['media','/lectures/media.html'],['blog','/blog/image.html']]){
   await page.goto(base+url,{waitUntil:'networkidle'});await page.evaluate(()=>document.fonts.ready);
   const metrics=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+2,missingImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src)}));
   await page.screenshot({path:path.join(out,`${name}-${width}.png`),fullPage:true});report.views.push({name,width,...metrics});
  }
 }
 await page.setViewportSize({width:1280,height:720});
 await page.goto(base+'/index.html');await page.getByRole('link',{name:'강의',exact:true}).click();
 await page.getByRole('link',{name:/작업을 끝내는 조건/}).click();await page.locator('.scene-row[href*="T04-1"]').click();
 await page.waitForFunction(()=>document.body.dataset.ready==='true');
 report.deepLink=await page.evaluate(()=>Reveal.getCurrentSlide().dataset.scene==='T04');
 await page.keyboard.press('f');await page.waitForTimeout(200);report.fullscreen=await page.evaluate(()=>!!document.fullscreenElement);if(report.fullscreen)await page.evaluate(()=>document.exitFullscreen());
 await page.keyboard.press('ArrowRight');await page.waitForTimeout(150);report.fragment=await page.evaluate(()=>Reveal.getIndices().f===0);
 for(const [slug,id] of [['overview','O07-4'],['tasks','T05-2'],['knowledge','K10-3'],['video','V09-3'],['video','V04-1'],['video','V07-2'],['video','V09-1']]){
  await page.goto(`${base}/slides/${slug}/index.html#/${id}`,{waitUntil:'domcontentloaded'});await page.waitForFunction(()=>document.body.dataset.ready==='true');
  const video=page.locator('section.present video');await video.waitFor();
  await page.keyboard.press('v');await page.waitForTimeout(1300);
  const state=await video.evaluate(v=>({time:v.currentTime,duration:v.duration,paused:v.paused,width:v.videoWidth,height:v.videoHeight,ready:v.readyState}));
  await page.keyboard.press('v');const paused=await video.evaluate(v=>v.paused);
  await page.screenshot({path:path.join(out,`${slug}-${id}-playing.png`)});
  report.media.push({slug,id,...state,pauses:paused});
 }
 const reduced=await browser.newContext({reducedMotion:'reduce'});const rp=await reduced.newPage();await rp.goto(base+'/slides/tasks/index.html');await rp.waitForFunction(()=>document.body.dataset.ready==='true');report.reducedMotion=await rp.evaluate(()=>Reveal.getConfig().transition==='none');await reduced.close();
 const offline=await browser.newContext({offline:true});const op=await offline.newPage({viewport:{width:1280,height:720}});const requests=[];op.on('request',r=>{if(/^https?:/.test(r.url()))requests.push(r.url())});
 await op.goto(pathToFileURL(path.join(root,'docs/slides/video/index.html')).href+'#/V04-1');await op.waitForFunction(()=>document.body.dataset.ready==='true');
 await op.keyboard.press('v');await op.waitForTimeout(1100);report.localMedia=await op.locator('section.present video').evaluate(v=>v.currentTime>0);await op.keyboard.press('v');
 const popupPromise=op.waitForEvent('popup');await op.keyboard.press('s');const sp=await popupPromise;await sp.waitForLoadState();report.localSpeaker=await sp.locator('#notes').innerText();report.localSpeaker=report.localSpeaker.includes('타임라인');report.externalRequests=requests;await offline.close();
 report.ok=errors.length===0&&report.views.every(v=>!v.overflow&&!v.missingImages.length)&&report.deepLink&&report.fullscreen&&report.fragment&&report.media.every(v=>v.time>0&&v.width>0&&v.pauses)&&report.reducedMotion&&report.localMedia&&report.localSpeaker&&requests.length===0;
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));await browser.close();if(!report.ok)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close()});
