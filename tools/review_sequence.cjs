/* A timed visual cue rehearsal. It does not simulate speech or audience reactions. */
const fs=require('node:fs'),path=require('node:path');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),out=path.join(root,'.work/sequence-review');
fs.mkdirSync(out,{recursive:true});
const base=process.env.WEB_BASE||'http://127.0.0.1:8769';
const cues=[
 [0,'T04-1',-1,'두 요청이 읽은 번호를 관찰합니다.'],
 [40,'T04-1',0,'A의 반영 뒤 현재 값 8을 확인합니다.'],
 [95,'T04-1',1,'B의 결과를 예측하고 15초 기다립니다.'],
 [110,'T04-1',2,'B 거부를 공개하고 두 번호를 대응시킵니다.'],
 [142,'T04-2',-1,'관찰한 상태 번호를 리비전으로 정의합니다.'],
 [180,'T04-2',0,'비교 후 갱신에 이 정의를 적용합니다.'],
 [218,'T04-3',-1,'읽었던 7과 현재 8을 다시 대조합니다.'],
 [280,'T04-3',1,'최신 상태를 읽어야 하는 이유를 설명합니다.'],
 [360,'T05-1',-1,'그림의 두 번호를 코드의 두 변수에 대응시킵니다.'],
 [395,'T05-1',0,'실제 오류 문구를 공개합니다.'],
 [425,'T05-1',1,'비교가 변경보다 먼저라는 규칙을 정리합니다.'],
 [450,'T05-2',-1,'실제 실행 녹화를 재생합니다.','play'],
 [495,'T05-3',-1,'최신 번호만 넣으면 충분한지 적용 질문을 냅니다.'],
 [525,'T05-3',0,'최신 계획과 상태를 읽는 선택을 설명합니다.'],
 [570,'T05-3',1,'번호에서 계획의 승인으로 다음 질문을 연결합니다.'],
 [600,'T05-3',1,'10분 발췌 큐 점검을 마칩니다.']
];
let browser;
(async()=>{
 browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||undefined});
 const page=await browser.newPage({viewport:{width:1280,height:720}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+'/slides/tasks/index.html#/T04-1',{waitUntil:'domcontentloaded'});
 await page.waitForFunction(()=>document.body.dataset.ready==='true');await page.evaluate(()=>document.fonts.ready);
 const start=Date.now(),events=[];let previous='';
 for(const [at,id,fragment,cue,action] of cues){
  while(Date.now()-start<at*1000)await page.waitForTimeout(Math.min(1000,at*1000-(Date.now()-start)));
  const elapsed=(Date.now()-start)/1000;
  await page.evaluate(({id,fragment,changed})=>{const i=Reveal.getSlides().findIndex(s=>s.id===id);if(changed)Reveal.slide(i,0,-1);Reveal.navigateFragment(fragment)},{id,fragment,changed:id!==previous});
  if(action==='play')await page.locator('section.present video').evaluate(v=>v.play());
  await page.waitForTimeout(250);
  const state=await page.evaluate(()=>{const v=document.querySelector('video');return {slide:Reveal.getCurrentSlide().id,fragment:Reveal.getIndices().f,video:v?{time:v.currentTime,duration:v.duration,ended:v.ended}:null}});
  await page.screenshot({path:path.join(out,`${String(at).padStart(3,'0')}-${id}.png`)});
  events.push({at,elapsed,cue,...state});previous=id;console.log(JSON.stringify(events.at(-1)));
 }
 const report={scope:'Ten-minute visual cue rehearsal using actual media and authored notes; no speech performance or audience response measured.',durationSeconds:(Date.now()-start)/1000,events,errors,ok:errors.length===0&&events.every((e,i)=>e.slide===cues[i][1]&&Math.abs(e.elapsed-e.at)<3)&&events.find(e=>e.at===495).video.ended};
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');if(!report.ok)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close()});
