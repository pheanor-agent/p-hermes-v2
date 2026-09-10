/* Inspect the rendered decks, capture every slide, and exercise local presentation controls. */
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname, '..');
const base = process.env.SLIDES_BASE || 'http://127.0.0.1:8769/slides';
const slug = process.argv[2] || 'preview';
const output = path.join(root, '.work', 'slide-review', slug);
fs.mkdirSync(output, {recursive:true});
(async()=>{
  const browser = await chromium.launch({headless:true, executablePath:process.env.CHROME_PATH || undefined});
  const page = await browser.newPage({viewport:{width:1280,height:720}});
  const errors=[]; const failed=[];
  page.on('pageerror',error=>errors.push(error.message));
  page.on('response',response=>{if(response.status()>=400)failed.push({url:response.url(),status:response.status()})});
  await page.goto(`${base}/${slug}/`,{waitUntil:'networkidle'});
  await page.waitForFunction(()=>document.body.dataset.ready==='true');
  await page.evaluate(()=>document.fonts.ready);
  const count=await page.evaluate(()=>Reveal.getTotalSlides());
  const report={slug,slides:count,views:[],errors,failed};
  for(const size of [{width:1280,height:720},{width:1920,height:1080}]){
    await page.setViewportSize(size);
    await page.evaluate(()=>Reveal.layout());
    for(let i=0;i<count;i++){
      await page.evaluate(i=>Reveal.slide(i,-1,-1),i);
      await page.waitForTimeout(220);
      const initial=await page.evaluate(()=>({id:Reveal.getCurrentSlide().id, fragments:Reveal.getCurrentSlide().querySelectorAll('.fragment').length}));
      if(size.width===1280)await page.screenshot({path:path.join(output,`${String(i+1).padStart(2,'0')}-start.png`)});
      await page.evaluate(()=>{const s=Reveal.getCurrentSlide();const indexes=[...s.querySelectorAll('.fragment')].map(n=>Number(n.dataset.fragmentIndex||0));Reveal.navigateFragment(indexes.length?Math.max(...indexes):-1)});
      await page.waitForTimeout(180);
      const metrics=await page.evaluate(()=>{
        const s=Reveal.getCurrentSlide(), frame=s.getBoundingClientRect();
        const overflow=[...s.querySelectorAll('h1,h2,p,td,th,code,strong,img,.big-value,.record-row,.cas-row,.photo-copy')].filter(n=>!n.closest('.notes')&&getComputedStyle(n).visibility!=='hidden'&&getComputedStyle(n).display!=='none').map(n=>({n,b:n.getBoundingClientRect()})).filter(({b})=>b.width&&b.height&&(b.left<frame.left-2||b.top<frame.top-2||b.right>frame.right+2||b.bottom>frame.bottom+2)).map(({n,b})=>({tag:n.tagName,text:n.textContent.slice(0,100),box:{x:b.x,y:b.y,w:b.width,h:b.height}}));
        return {overflow, missingImages:[...s.querySelectorAll('img')].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.getAttribute('src')),fontLoaded:document.fonts.check('48px Hermes'),notesHidden:[...s.querySelectorAll('.notes')].every(n=>getComputedStyle(n).display==='none')};
      });
      const file=`${String(i+1).padStart(2,'0')}-${size.width}-final.png`;
      await page.screenshot({path:path.join(output,file)});
      report.views.push({slide:i+1,id:initial.id,viewport:size,...metrics,screenshot:file});
    }
  }
  await page.evaluate(()=>Reveal.slide(1,-1,-1));
  const popupPromise=page.waitForEvent('popup');
  await page.keyboard.press('s');
  const speaker=await popupPromise;await speaker.waitForLoadState();
  report.speaker={title:await speaker.locator('h1').textContent(),body:await speaker.locator('#notes').innerText()};
  await speaker.locator('#next').click();await page.waitForTimeout(120);
  report.speaker.controlWorks=await page.evaluate(()=>Reveal.getIndices().f>=0);
  await speaker.close();
  await page.keyboard.press('h');report.helpOpens=await page.locator('.deck-help').isVisible();
  await page.locator('[data-close-help]').click();
  await page.evaluate(()=>Reveal.slide(0,-1,-1));
  await page.keyboard.press('ArrowRight');report.keyboardFragment=await page.evaluate(()=>Reveal.getIndices().f);
  report.ok=errors.length===0&&failed.length===0&&report.views.every(v=>v.overflow.length===0&&v.missingImages.length===0&&v.fontLoaded&&v.notesHidden)&&report.speaker.controlWorks&&report.helpOpens;
  fs.writeFileSync(path.join(output,'report.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify({slug,slides:count,ok:report.ok,errors,failed,issues:report.views.filter(v=>v.overflow.length||v.missingImages.length||!v.fontLoaded),speaker:report.speaker.controlWorks,output}));
  await browser.close();if(!report.ok)process.exitCode=1;
})().catch(error=>{console.error(error);process.exitCode=1});
