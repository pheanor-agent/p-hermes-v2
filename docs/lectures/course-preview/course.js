'use strict';
// Reading is native HTML. This file only reports position; it never moves focus or scroll.
(() => {
  const lessons = [...document.querySelectorAll('section.lesson')];
  const links = [...document.querySelectorAll('.toc a')];
  const wrap = document.querySelector('.progress-wrap');
  const meter = document.querySelector('#reading-progress');
  const label = document.querySelector('#position-label');
  if (!lessons.length || !wrap || !meter || !label) return;
  wrap.hidden = false;
  let queued = false;
  function update() {
    queued = false;
    const height = document.documentElement.scrollHeight - window.innerHeight;
    const percent = height > 0 ? Math.min(100, Math.max(0, Math.round(window.scrollY / height * 100))) : 100;
    meter.value = percent;
    let current = null;
    for (const lesson of lessons) {
      if (lesson.getBoundingClientRect().top <= window.innerHeight * 0.4) current = lesson;
    }
    links.forEach(link => {
      if (current && link.hash === '#' + current.id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    const index = current ? lessons.indexOf(current) + 1 : 0;
    label.textContent = index ? `${String(index).padStart(2, '0')} / 04 구간 · 읽기 ${percent}%` : `강의 안내 · 읽기 ${percent}%`;
  }
  function schedule() { if (!queued) { queued = true; window.requestAnimationFrame(update); } }
  window.addEventListener('scroll', schedule, {passive:true});
  window.addEventListener('resize', schedule);
  window.addEventListener('load', schedule);
  if (document.fonts) document.fonts.ready.then(schedule);
  update();
})();
