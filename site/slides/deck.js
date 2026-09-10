/* Local-only presentation controls and a separate, offline-capable speaker view. */
(() => {
  'use strict';
  const metadata = JSON.parse(document.getElementById('course-data').textContent);
  const notes = metadata.slides;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let speaker = null;
  let timer = null;
  const help = document.querySelector('.deck-help');
  function speakerHtml() {
    return `<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>발표자 · ${metadata.title}</title><style>body{margin:0;background:#121d34;color:#f6f4ed;font:20px/1.7 system-ui,sans-serif;padding:32px}header{display:flex;justify-content:space-between;color:#b8c6dc}h1{font-size:34px;line-height:1.25}h2{font-size:18px;color:#b8c6dc;margin-top:28px}p{white-space:pre-line}button{font:inherit;padding:7px 18px;background:#f6f4ed;border:0;margin-right:10px;color:#19253b}a{color:#bdd0ff}.actions{position:sticky;bottom:0;background:#121d34;padding:15px 0}</style></head><body><header><span id="where"></span><span id="clock">0:00</span></header><h1 id="title"></h1><main id="notes"></main><div class="actions"><button id="back">이전</button><button id="next">다음</button></div><script>let began=Date.now();setInterval(()=>{let t=Math.floor((Date.now()-began)/1000);document.getElementById('clock').textContent=Math.floor(t/60)+':'+String(t%60).padStart(2,'0')},1000);document.getElementById('back').onclick=()=>opener.postMessage({type:'ph-speaker-command',action:'prev'},'*');document.getElementById('next').onclick=()=>opener.postMessage({type:'ph-speaker-command',action:'next'},'*');document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='PageDown'){e.preventDefault();opener.postMessage({type:'ph-speaker-command',action:'next'},'*')}});</script></body></html>`;
  }
  function updateSpeaker() {
    if (!speaker || speaker.closed) return;
    const index = Reveal.getIndices().h;
    const item = notes[index];
    const doc = speaker.document;
    doc.getElementById('where').textContent = `${metadata.title} · ${index + 1}/${notes.length} · ${item.scene}`;
    doc.getElementById('title').textContent = item.title;
    doc.getElementById('notes').innerHTML = item.notes_html;
  }
  function openSpeaker() {
    speaker = window.open('', 'p-hermes-speaker', 'popup,width=900,height=800');
    if (!speaker) { help.hidden = false; return; }
    speaker.document.open(); speaker.document.write(speakerHtml()); speaker.document.close();
    updateSpeaker();
  }
  function toolsVisible() {
    document.body.classList.add('show-tools');
    clearTimeout(timer); timer = setTimeout(() => document.body.classList.remove('show-tools'), 2300);
  }
  Reveal.initialize({width:1920,height:1080,margin:0,minScale:0.1,maxScale:2,center:false,
    controls:false,progress:false,hash:true,history:false,view:'slide',scrollActivationWidth:null,
    transition:reduced?'none':'fade',transitionSpeed:'fast',autoAnimate:false,
    pdfSeparateFragments:false,pdfMaxPagesPerSlide:1,showNotes:false,
    keyboard:{83:openSpeaker,72:()=>{help.hidden=!help.hidden},86:()=>{const v=Reveal.getCurrentSlide().querySelector('video');if(v){v.paused?v.play():v.pause()}}}
  }).then(() => {
    const refresh=()=>{document.getElementById('slide-count').textContent=`${Reveal.getIndices().h+1} / ${notes.length}`;updateSpeaker()};
    Reveal.on('slidechanged',refresh);Reveal.on('fragmentshown',updateSpeaker);Reveal.on('fragmenthidden',updateSpeaker);
    refresh();document.body.dataset.ready='true';
    document.querySelectorAll('video').forEach(video=>video.addEventListener('timeupdate',()=>{
      const slide=video.closest('section'),cursor=slide.querySelector('[data-cursor]'),label=slide.querySelector('[data-playback-time]');
      if(cursor&&Number.isFinite(video.duration))cursor.style.left=(100*video.currentTime/video.duration)+'%';
      if(label)label.textContent=video.currentTime.toFixed(2)+'s';
    }));
    Reveal.on('slidechanged',event=>{event.previousSlide?.querySelectorAll('video').forEach(v=>v.pause())});
  });
  document.querySelector('[data-deck="next"]').onclick=()=>Reveal.next();
  document.querySelector('[data-deck="prev"]').onclick=()=>Reveal.prev();
  document.querySelector('[data-deck="speaker"]').onclick=openSpeaker;
  document.querySelector('[data-deck="fullscreen"]').onclick=()=>document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen();
  document.querySelector('[data-deck="help"]').onclick=()=>{help.hidden=!help.hidden};
  document.querySelector('[data-close-help]').onclick=()=>{help.hidden=true};
  window.addEventListener('message',event=>{if(event.source!==speaker||event.data?.type!=='ph-speaker-command')return;if(event.data.action==='next')Reveal.next();if(event.data.action==='prev')Reveal.prev()});
  document.addEventListener('pointermove',toolsVisible,{passive:true});
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!help.hidden){help.hidden=true;event.preventDefault()}});
  toolsVisible();
})();
