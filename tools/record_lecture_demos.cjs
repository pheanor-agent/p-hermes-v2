/* Record real step receipts. Optional SSH runner uses explicitly supplied host/path. */
const fs=require('node:fs'),path=require('node:path'),cp=require('node:child_process'),readline=require('node:readline');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const root=path.resolve(__dirname,'..'),out=path.join(root,'site/slides/media');
const fontData=fs.readFileSync(path.join(root,'docs/assets/HermesKR.woff2')).toString('base64');
const titles={cas:'같은 상태를 읽은 두 요청',knowledge:'기록은 남고, 검색이 달라집니다',integration:'파일과 DB를 다시 열어 확인합니다',probe:'실제 2초 파일의 규격 검사'};
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROME_PATH||undefined});
 for(const scenario of process.argv.slice(2).length?process.argv.slice(2):Object.keys(titles)){
  const count=scenario==='probe'?3:4;
  const worker=process.env.DEMO_HOST?cp.spawn('ssh',['-o','BatchMode=yes',process.env.DEMO_HOST,'python3',`${process.env.DEMO_ROOT}/tools/lecture_worker.py`,scenario]):cp.spawn(process.env.PYTHON_PATH||'python',['tools/lecture_worker.py',scenario],{cwd:root});
  const lines=readline.createInterface({input:worker.stdout});const queue=[];let waiting=null;let stderr='';
  worker.stderr.on('data',data=>stderr+=data);lines.on('line',line=>{if(waiting){const done=waiting;waiting=null;done(JSON.parse(line))}else queue.push(JSON.parse(line))});
  const context=await browser.newContext({viewport:{width:1280,height:720},recordVideo:{dir:path.join(root,'.work/demo-recordings'),size:{width:1280,height:720}}});
  const page=await context.newPage();
  await page.setContent(`<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>@font-face{font-family:Hermes;src:url('data:font/woff2;base64,${fontData}')}*{box-sizing:border-box}body{margin:0;padding:50px 70px;background:#121d34;color:#f6f4ed;font:25px/1.5 Hermes,sans-serif}header{font-size:20px;color:#b8c6dc}h1{font-size:43px;margin:20px 0 32px;letter-spacing:-.04em}pre{font:25px/1.55 Consolas,Hermes,monospace;white-space:pre-wrap;overflow-wrap:anywhere;margin:18px 0}#command{color:#bdd0ff;border-bottom:1px solid #60708b;padding-bottom:25px}#output{font-size:26px;line-height:1.45;margin:0}.log-grid{display:grid;grid-template-columns:1fr 1.3fr;gap:45px;align-items:start}.log-grid pre{min-width:0}#command{border-bottom:0;border-right:1px solid #60708b;padding:0 35px 0 0;margin:0;font-size:${scenario==='integration'?21:27}px;line-height:1.5}footer{position:absolute;bottom:28px;color:#b8c6dc;font-size:18px}.step{position:absolute;right:70px;top:52px}</style></head><body><header>공개 코드 실행 · 합성 입력</header><span class="step" id="step"></span><h1>${titles[scenario]}</h1><div class="log-grid"><pre id="command">실행 준비</pre><pre id="output"></pre></div><footer>실제 실행 직후 선택한 필드의 출력 · 모델 생성이나 영상 인코딩 시연과 구분합니다.</footer></body></html>`);
  await page.evaluate(()=>document.fonts.ready);
  const receipts=[];
  for(let i=0;i<count;i++){
   worker.stdin.write(i+'\n');
   const result=await Promise.race([queue.length?Promise.resolve(queue.shift()):new Promise(resolve=>waiting=resolve),new Promise((_,reject)=>setTimeout(()=>reject(Error('Worker timed out '+stderr)),15000))]);
   receipts.push(result);
   await page.evaluate(({result,i,count})=>{document.querySelector('#step').textContent=`${i+1} / ${count}`;document.querySelector('#command').textContent=result.command;document.querySelector('#output').textContent=Object.entries(result.output).map(([k,v])=>k+': '+(Array.isArray(v)?'\n'+v.map(x=>'  '+JSON.stringify(x)).join('\n'):JSON.stringify(v))).join('\n\n')},{result,i,count});
   await page.waitForTimeout(4600);
   const safe=await page.evaluate(()=>document.querySelector('#output').getBoundingClientRect().bottom<document.querySelector('footer').getBoundingClientRect().top-8);if(!safe)throw Error(scenario+' output overlaps footer at step '+i);
   const review=path.join(root,'.work/demo-review',scenario);fs.mkdirSync(review,{recursive:true});await page.screenshot({path:path.join(review,`step-${i+1}.png`)});
   if(i===0)await page.screenshot({path:path.join(out,`demo-${scenario}-poster.png`)});
  }
  worker.stdin.end();await new Promise((resolve,reject)=>worker.on('close',code=>code===0?resolve():reject(Error(stderr))));
  const video=page.video();await context.close();await video.saveAs(path.join(out,`demo-${scenario}.webm`));
  fs.writeFileSync(path.join(root,`content/slides/recording-${scenario}.json`),JSON.stringify({scenario,scope:'Real function calls on synthetic inputs; selected fields displayed immediately after each return.',receipts},null,2)+'\n');
  console.log(scenario,'recorded',receipts.length,'real steps');
 }
 await browser.close();
})().catch(error=>{console.error(error);process.exitCode=1});
