/* Play every authored video to its end and capture actual beginning/end frames. */
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),out=path.join(root,'.work/media-review');fs.mkdirSync(out,{recursive:true});
const base=process.env.WEB_BASE||'http://127.0.0.1:8769';let browser;
const selected=process.argv.slice(2);
(async()=>{
 browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||undefined});
 const page=await browser.newPage({viewport:{width:1280,height:720}});const previous=path.join(out,'report.json');
 const items=selected.length&&fs.existsSync(previous)?JSON.parse(fs.readFileSync(previous)).items.filter(x=>!selected.includes(x.file)):[];
 for(const file of selected.length?selected:['demo-cas.webm','demo-knowledge.webm','demo-integration.webm','demo-probe.webm','edit-a.mp4','edit-b.mp4','probe-2s.mp4']){
  await page.goto(base+'/index.html');await page.setContent(`<style>body{margin:0;background:#121d34}video{width:1280px;height:720px;object-fit:contain}</style><video preload="auto" muted src="${base}/slides/assets/media/${file}"></video>`);
  const v=page.locator('video');await v.evaluate(v=>v.play());await page.waitForTimeout(200);await page.screenshot({path:path.join(out,file+'-start.png')});
  const began=Date.now();await page.waitForFunction(()=>document.querySelector('video').ended,{},{timeout:40000});
  const state=await v.evaluate(v=>({duration:v.duration,time:v.currentTime,width:v.videoWidth,height:v.videoHeight,ended:v.ended,error:v.error?.code||null}));
  await page.screenshot({path:path.join(out,file+'-end.png')});items.push({file,elapsedSeconds:(Date.now()-began)/1000,reviewedAt:new Date().toISOString(),sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'site/slides/media',file))).digest('hex'),...state});console.log(JSON.stringify(items.at(-1)));
 }
 const report={scope:'Actual browser playback to ended, including first and last rendered frames.',items,ok:items.every(v=>v.ended&&!v.error&&v.width===1280&&v.height===720)};
 fs.writeFileSync(path.join(out,'report.json'),JSON.stringify(report,null,2)+'\n');if(!report.ok)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close()});
