/* Progressive enhancement: all lessons and wiki text exist without JavaScript. */
(() => {
  'use strict';
  const body=document.body;
  body.classList.add('js-enabled');
  const slides=[...document.querySelectorAll('[data-slide]')];
  const toggle=document.getElementById('present-toggle');
  const controls=document.querySelector('.presentation-controls');
  const deck=document.querySelector('.course-main');
  let current=0;
  let lastFocus=null;
  function fromHash(){const i=slides.findIndex(s=>`#${s.id}`===location.hash);if(i>=0)current=i;}
  function render(){
    slides.forEach((s,i)=>s.classList.toggle('active',i===current));
    const count=document.getElementById('slide-count');
    if(count)count.textContent=`${current+1} / ${slides.length}`;
    const prev=document.getElementById('prev-slide'),next=document.getElementById('next-slide');
    if(prev)prev.disabled=current===0&&!deck?.dataset.prevDeck;
    if(next)next.disabled=current===slides.length-1&&!deck?.dataset.nextDeck;
  }
  function move(offset){
    if(current+offset>=slides.length&&deck?.dataset.nextDeck){location.assign(deck.dataset.nextDeck);return;}
    if(current+offset<0&&deck?.dataset.prevDeck){location.assign(deck.dataset.prevDeck);return;}
    current=Math.min(slides.length-1,Math.max(0,current+offset));
    history.pushState(null,'',`#${slides[current].id}`);render();window.scrollTo({top:0,behavior:'instant'});
  }
  function present(on){
    if(!slides.length)return;
    if(on)lastFocus=document.activeElement;
    fromHash();body.classList.toggle('presenting',on);
    controls.hidden=!on;toggle.setAttribute('aria-pressed',String(on));render();
    if(on){window.scrollTo({top:0,behavior:'instant'});document.getElementById('exit-present').focus({preventScroll:true});}
    else{const u=new URL(location.href);u.searchParams.delete('present');history.replaceState(null,'',u);body.classList.remove('show-notes');document.getElementById('notes-toggle').setAttribute('aria-pressed','false');slides.forEach(s=>{const n=s.querySelector('.speaker-notes');if(n)n.open=false;});slides[current].scrollIntoView({block:'start',behavior:'instant'});if(lastFocus)lastFocus.focus({preventScroll:true});}
  }
  toggle?.addEventListener('click',()=>present(!body.classList.contains('presenting')));
  document.getElementById('exit-present')?.addEventListener('click',()=>present(false));
  document.getElementById('prev-slide')?.addEventListener('click',()=>move(-1));
  document.getElementById('next-slide')?.addEventListener('click',()=>move(1));
  document.getElementById('notes-toggle')?.addEventListener('click',e=>{const on=body.classList.toggle('show-notes');e.currentTarget.setAttribute('aria-pressed',String(on));slides.forEach(s=>s.querySelector('.speaker-notes').open=on);});
  document.getElementById('print-page')?.addEventListener('click',()=>window.print());
  document.addEventListener('keydown',e=>{
    if(!body.classList.contains('presenting')||/INPUT|TEXTAREA|SELECT/.test(e.target.tagName)||e.target.isContentEditable)return;
    if(e.key==='Escape'){present(false);return;}
    if(['ArrowRight','PageDown'].includes(e.key)){e.preventDefault();move(1);}
    if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();move(-1);}
    if(e.key==='Home'){e.preventDefault();move(-current);}
    if(e.key==='End'){e.preventDefault();move(slides.length-1-current);}
  });
  window.addEventListener('hashchange',()=>{fromHash();render();});
  window.addEventListener('popstate',()=>{fromHash();render();});
  fromHash();render();
  if(new URL(location.href).searchParams.get('present')==='1')present(true);
})();
