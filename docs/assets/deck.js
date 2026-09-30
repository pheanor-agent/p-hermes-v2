(() => {
  const stage = document.getElementById('deck');
  const slides = [...stage.querySelectorAll('.dk-slide')];
  const bar = stage.querySelector('.dk-progress span');
  const viewport = document.querySelector('.dk-viewport');
  let current = 0;
  const liveCount = document.querySelector('.dk-live-count');
  const previousButton = document.querySelector('[data-go="-1"]');
  const nextButton = document.querySelector('[data-go="1"]');

  function fit() {
    const w = viewport.clientWidth, h = viewport.clientHeight;
    const scale = Math.min(w / stage.offsetWidth, h / stage.offsetHeight);
    stage.style.setProperty('--dk-scale', scale.toFixed(4));
  }

  function show(i, push = true) {
    const last = current;
    current = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, k) => {
      s.classList.toggle('is-active', k === current);
      s.setAttribute('aria-hidden', String(k !== current));
    });
    bar.style.width = ((current + 1) / slides.length * 100) + '%';
    if (liveCount) liveCount.textContent = `${current + 1} / ${slides.length}`;
    previousButton.disabled = current === 0;
    nextButton.disabled = current === slides.length - 1;
    if (last !== current) viewport.scrollTop = 0;
    if (push) history.replaceState(null, '', '#' + (current + 1));
  }

  function fromHash() {
    const n = parseInt(location.hash.replace(/^#s?/, ''), 10);
    return Number.isFinite(n) ? n - 1 : 0;
  }

  function toggleFs() {
    if (document.fullscreenElement) document.exitFullscreen();
    else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
  }

  document.addEventListener('keydown', e => {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    // Space/Enter keep their native activation behavior on navigation controls.
    if (e.target.closest('input,textarea,select,[contenteditable="true"]')) return;
    if (e.target.closest('a,button') && [' ', 'Enter'].includes(e.key)) return;
    if (['ArrowRight', 'PageDown', ' ', 'Enter'].includes(e.key)) { e.preventDefault(); show(current + 1); }
    else if (['ArrowLeft', 'PageUp', 'Backspace'].includes(e.key)) { e.preventDefault(); show(current - 1); }
    else if (e.key === 'Home') show(0);
    else if (e.key === 'End') show(slides.length - 1);
    else if (e.key === 'f' || e.key === 'F') toggleFs();
  });
  document.querySelectorAll('[data-go]').forEach(b => b.addEventListener('click', () => show(current + Number(b.dataset.go))));
  document.querySelector('[data-fs]').addEventListener('click', toggleFs);
  document.addEventListener('fullscreenchange', () => {
    document.body.classList.toggle('is-fs', !!document.fullscreenElement);
    requestAnimationFrame(fit);
  });

  let x0 = null;
  let y0 = null;
  viewport.addEventListener('touchstart', e => {
    x0 = e.target.closest('.dk-diagram,a,button') ? null : e.touches[0].clientX;
    y0 = e.touches[0].clientY;
  }, { passive: true });
  viewport.addEventListener('touchend', e => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    const dy = e.changedTouches[0].clientY - y0;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.4) show(current + (dx < 0 ? 1 : -1));
    x0 = null;
  });
  viewport.addEventListener('click', e => {
    if (e.target.closest('a,button,.dk-diagram,.dk-copy,.dk-foot')) return;
    const r = viewport.getBoundingClientRect();
    show(current + (e.clientX > r.left + r.width / 2 ? 1 : -1));
  });

  window.addEventListener('resize', fit);
  window.addEventListener('hashchange', () => show(fromHash(), false));
  fit();
  show(fromHash(), false);
  window.__deck = { show, count: slides.length, get current() { return current; } };
})();
