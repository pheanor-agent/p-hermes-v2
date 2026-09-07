'use strict';
(() => {
  const slides = Array.from(document.querySelectorAll('.slide'));
  const prev = document.getElementById('prev');
  const next = document.getElementById('next');
  const progress = document.getElementById('progress');
  if (!slides.length || !prev || !next || !progress) return;
  let current = 0;
  function render(focus = false) {
    const index = slides.findIndex(slide => '#' + slide.id === location.hash);
    current = index < 0 ? 0 : index;
    slides.forEach((slide, i) => { slide.hidden = i !== current; });
    prev.disabled = current === 0;
    next.disabled = current === slides.length - 1;
    progress.textContent = `${current + 1} / ${slides.length}`;
    document.title = `${slides[current].querySelector('h1,h2').textContent} · 강의 시안`;
    if (focus) {
      slides[current].focus({preventScroll: true});
      window.scrollTo({top: 0, behavior: 'instant'});
    }
  }
  function move(delta) {
    const target = Math.max(0, Math.min(slides.length - 1, current + delta));
    if (target !== current) location.hash = slides[target].id;
  }
  prev.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  window.addEventListener('hashchange', () => render(true));
  document.addEventListener('keydown', event => {
    if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    if (event.target.closest('input,textarea,select,button,a,[contenteditable]:not([contenteditable="false"]),[role="textbox"],[role="slider"]')) return;
    const directions = {ArrowLeft: -1, ArrowUp: -1, PageUp: -1, ArrowRight: 1, ArrowDown: 1, PageDown: 1};
    if (Object.hasOwn(directions, event.key)) {
      event.preventDefault();
      move(directions[event.key]);
    }
  });
  render();
  document.querySelector('.controls').hidden = false;
})();
