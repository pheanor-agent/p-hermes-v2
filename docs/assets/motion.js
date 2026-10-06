/* p-hermes motion layer: line draw-in, packets travelling along wires, step builds
   and small interactive simulators. No external libraries. Respects reduced motion. */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
  const el = (tag, attrs = {}, text) => {
    const n = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    if (text !== undefined) n.textContent = text;
    return n;
  };

  /* ---------- packets: <circle class="mo-pkt" data-path="id" data-dur="2.4" data-delay="0"> ---------- */
  const packets = [];
  function bindPackets(slide) {
    $$('.mo-pkt', slide).forEach(p => {
      if (p.__bound) return;
      const svg = p.ownerSVGElement;
      const path = svg && svg.querySelector('#' + CSS.escape(p.dataset.path));
      if (!path) return;
      p.__bound = true;
      packets.push({ p, path, slide, len: path.getTotalLength(), dur: +p.dataset.dur || 2.4, delay: +p.dataset.delay || 0, loop: p.dataset.loop !== 'no' });
    });
  }
  let t0 = performance.now();
  function tick(now) {
    for (const k of packets) {
      if (!k.slide.classList.contains('is-active')) continue;
      if (k.p.closest('[data-build]:not(.built)')) { k.p.style.opacity = 0; continue; }
      const start = k.slide.__t0 || t0;
      let t = (now - start) / 1000 - k.delay;
      if (t < 0) { k.p.style.opacity = 0; continue; }
      let u = t / k.dur;
      if (k.loop) u = u % 1; else u = Math.min(u, 1);
      const pt = k.path.getPointAtLength(u * k.len);
      k.p.setAttribute('cx', pt.x.toFixed(1));
      k.p.setAttribute('cy', pt.y.toFixed(1));
      k.p.style.opacity = k.loop ? Math.min(1, Math.min(u, 1 - u) * 8) : 1;
    }
    requestAnimationFrame(tick);
  }

  /* ---------- builds: elements with data-build="n" appear on successive presses ---------- */
  function builds(slide) { return Math.max(0, ...$$('[data-build]', slide).map(b => +b.dataset.build)); }
  function setBuild(slide, n) {
    slide.__build = n;
    $$('[data-build]', slide).forEach(b => b.classList.toggle('built', +b.dataset.build <= n));
    $$('[data-build-on]', slide).forEach(b => b.classList.toggle('lit', +b.dataset.buildOn === n));
    const dots = $('.mo-dots', slide);
    if (dots) $$('i', dots).forEach((d, k) => d.classList.toggle('on', k < n));
  }
  function addDots(slide) {
    const total = builds(slide);
    if (!total || $('.mo-dots', slide)) return;
    const dots = el('span', { class: 'mo-dots', 'aria-hidden': 'true' });
    for (let k = 0; k < total; k++) dots.append(el('i'));
    const head = $('.dk-head', slide);
    head && head.insertBefore(dots, head.lastElementChild);
  }

  /* Called by deck.js. Returns true when the press was consumed by a build step. */
  function step(slide, dir) {
    const total = builds(slide);
    const n = slide.__build || 0;
    if (dir > 0 && n < total) { setBuild(slide, n + 1); return true; }
    if (dir < 0 && n > 0) { setBuild(slide, n - 1); return true; }
    return false;
  }
  function enter(slide, fromBehind) {
    slide.__t0 = performance.now();
    addDots(slide);
    bindPackets(slide);
    setBuild(slide, fromBehind ? builds(slide) : 0);
    // restart CSS draw-in animations
    slide.classList.remove('mo-play'); void slide.offsetWidth; slide.classList.add('mo-play');
    $$('[data-sim]', slide).forEach(s => s.__sim && s.__sim.enter && s.__sim.enter());
  }

  /* ---------- simulator scaffolding ---------- */
  function panel(root, title) {
    root.classList.add('sim');
    root.innerHTML = '';
    const head = el('div', { class: 'sim-head' });
    head.append(el('span', { class: 'sim-tag' }, 'SIMULATOR'), el('b', {}, title));
    const body = el('div', { class: 'sim-body' });
    const view = el('div', { class: 'sim-view' });
    const ctrl = el('div', { class: 'sim-ctrl' });
    body.append(view, ctrl);
    const metrics = el('div', { class: 'sim-metrics' });
    root.append(head, body, metrics);
    return { view, ctrl, metrics };
  }
  function metric(metrics, label) {
    const box = el('div', { class: 'sim-metric' });
    const v = el('strong', {}, '–');
    box.append(el('span', {}, label), v);
    metrics.append(box);
    return v;
  }
  function group(ctrl, label) {
    const g = el('div', { class: 'sim-group' });
    g.append(el('span', { class: 'sim-label' }, label));
    ctrl.append(g);
    return g;
  }
  function seg(g, options, value, onChange) {
    const box = el('div', { class: 'sim-seg', role: 'radiogroup' });
    options.forEach(([v, label]) => {
      const b = el('button', { type: 'button', role: 'radio', 'aria-checked': String(v === value) }, label);
      b.addEventListener('click', () => {
        $$('button', box).forEach(x => x.setAttribute('aria-checked', 'false'));
        b.setAttribute('aria-checked', 'true');
        onChange(v);
      });
      box.append(b);
    });
    g.append(box);
    return box;
  }
  function toggle(g, label, value, onChange) {
    const b = el('button', { type: 'button', class: 'sim-toggle', 'aria-pressed': String(value) }, label);
    b.addEventListener('click', () => {
      const v = b.getAttribute('aria-pressed') !== 'true';
      b.setAttribute('aria-pressed', String(v));
      onChange(v);
    });
    g.append(b);
    return b;
  }
  function button(g, label, onClick, primary) {
    const b = el('button', { type: 'button', class: 'sim-btn' + (primary ? ' primary' : '') }, label);
    b.addEventListener('click', onClick);
    g.append(b);
    return b;
  }
  const NS = 'http://www.w3.org/2000/svg';
  const svgEl = (tag, attrs = {}, text) => {
    const n = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    if (text !== undefined) n.textContent = text;
    return n;
  };

  /* ---------- 01: 직접 할까, 맡길까 ---------- */
  function simDelegate(root) {
    const { view, ctrl, metrics } = panel(root, '직접 할까, 맡길까 — POLICY (a)·(i) 판단기');
    const s = { long: false, big: false, quality: false, irreversible: 'none' };
    const flow = el('div', { class: 'sim-flow' });
    const steps = [
      ['q1', '되돌릴 수 없는 4개 범주인가?', '영구 삭제 · 외부 게시 · 자격증명 · POLICY 개정'],
      ['q2', '세션을 오래 점유하거나 산출이 큰가?', '긴 실행 · 대량 파일 · 미디어 · 반복'],
      ['q3', '결과 품질을 좌우하는 판단인가?', '설계 · 정책 · 글 완성도 · 시각 결과 · 모호한 의도'],
    ];
    const rows = steps.map(([id, q, sub]) => {
      const r = el('div', { class: 'sim-q' });
      r.append(el('b', {}, q), el('span', {}, sub), el('em', {}, ''));
      flow.append(r);
      return r;
    });
    view.append(flow);
    const g1 = group(ctrl, '작업의 성격');
    toggle(g1, '오래 걸린다', false, v => { s.long = v; draw(); });
    toggle(g1, '산출이 크다', false, v => { s.big = v; draw(); });
    toggle(g1, '품질 판단이 핵심', false, v => { s.quality = v; draw(); });
    const g2 = group(ctrl, '되돌릴 수 없는 변경');
    seg(g2, [['none', '없음'], ['delete', '영구 삭제'], ['publish', '외부 게시'], ['cred', '자격증명']], 'none', v => { s.irreversible = v; draw(); });
    const mWho = metric(metrics, '누가 하나'), mWhy = metric(metrics, '근거 조항'), mRec = metric(metrics, '기록');
    root.append(el('p', { class: 'sim-try' }, '해볼 것: ① 아무것도 켜지 않으면 매니저가 직접 합니다. ② "오래 걸린다"를 켜면 워커에게 파일로 맡깁니다. ③ "품질 판단이 핵심"까지 켜면 판단은 매니저가, 실행량만 워커가 맡습니다. ④ 외부 게시를 고르면 무엇을 켜도 사용자 승인으로 멈춥니다.'));
    function draw() {
      rows.forEach(r => r.className = 'sim-q');
      let who, why, rec, hit;
      if (s.irreversible !== 'none') {
        hit = 0; who = '사용자 승인'; why = 'POLICY (i)'; rec = '승인 문장 기록';
        rows[0].querySelector('em').textContent = '예 → 멈춤';
      } else {
        rows[0].querySelector('em').textContent = '아니오';
        const heavy = s.long || s.big;
        rows[1].querySelector('em').textContent = heavy ? '예' : '아니오';
        rows[2].querySelector('em').textContent = s.quality ? '예' : '아니오';
        if (heavy && s.quality) { hit = 2; who = '판단은 매니저 · 실행은 워커'; why = 'POLICY (a)'; rec = 'JOB + 요청서'; }
        else if (heavy) { hit = 1; who = '워커에 위임'; why = 'POLICY (a)·(a-3)'; rec = '요청서 · 응답서'; }
        else { hit = 2; who = '매니저가 직접'; why = 'POLICY (a)'; rec = '백업 + 원장 한 줄'; }
      }
      rows.forEach((r, k) => { if (k < hit) r.classList.add('pass'); if (k === hit) r.classList.add('hit'); });
      mWho.parentNode.dataset.kind = s.irreversible !== 'none' ? 'stop' : (who.includes('워커') ? 'worker' : 'manager');
      mWho.textContent = who; mWhy.textContent = why; mRec.textContent = rec;
    }
    draw();
    return {};
  }

  /* ---------- 01: 결과 판정 ---------- */
  function simVerdict(root) {
    const { view, ctrl, metrics } = panel(root, '응답이 돌아왔을 때 — 판정과 복구 (a-4)');
    const s = { status: 'done', same: 1, checked: true };
    const card = el('div', { class: 'sim-card' });
    view.append(card);
    const g1 = group(ctrl, '응답서 status');
    seg(g1, [['done', 'done'], ['partial', 'partial'], ['blocked', 'blocked'], ['timeout', '시간 초과']], 'done', v => { s.status = v; draw(); });
    const g2 = group(ctrl, '같은 사유로 막힌 횟수');
    seg(g2, [[1, '1회'], [2, '2회'], [3, '3회']], 1, v => { s.same = v; draw(); });
    const g3 = group(ctrl, '원천 대조');
    toggle(g3, '핵심 수치 1개를 원천과 대조함', true, v => { s.checked = v; draw(); });
    const mState = metric(metrics, '판정'), mNext = metric(metrics, '다음 행동'), mReq = metric(metrics, '새 request_id');
    root.append(el('p', { class: 'sim-try' }, '해볼 것: done이어도 원천 대조를 끄면 완료로 보고하지 않습니다. partial은 "원인 1줄 + 바꾼 점 1줄 + 남은 항목"만 붙여 이어가고, 같은 사유가 2회면 멈추고 보고합니다.'));
    function draw() {
      let st, next, req, lines;
      if (s.status === 'done') {
        if (s.checked) { st = '완료'; next = '사용자에게 결과 보고'; req = '불필요'; lines = ['응답서 status: done', '핵심 수치 1개 원천 대조 ✓', '품질 산출은 매니저가 직접 읽음']; }
        else { st = '확인 전'; next = '원천과 직접 대조'; req = '불필요'; lines = ['응답서 status: done', '대조 전에는 done으로 보고하지 않음']; }
      } else if (s.same >= 2 && s.status !== 'timeout') {
        st = '멈춤'; next = s.same >= 3 ? '쓸 수 있는 결과 · 남은 것 · 대안 보고' : '원인 진단 후 사용자에게 보고'; req = '보류';
        lines = [`같은 사유 ${s.same}회`, '같은 요청을 반복하지 않음', '진단 기록: 원인 · 조치 · 상태'];
      } else if (s.status === 'partial') {
        st = '이어가기'; next = '이어가기 요청 1건'; req = '발급'; lines = ['원 목표 유지', '+ 직전 실패 원인 1줄', '+ 바꾼 점 1줄 + 남은 항목', '새 조건·게이트 추가 금지'];
      } else if (s.status === 'blocked') {
        st = '승인 확인'; next = '선택형 질문 1개'; req = '승인 후 발급'; lines = ['실제 승인이 필요한 부분만 질문', '나머지는 계속 진행', '게이트 우회 금지'];
      } else {
        st = '크기 조정'; next = 'timeout 한 단계 상향 또는 분할'; req = '발급'; lines = ['같은 크기로 재시도하지 않음', '조사 1800 · 구현 3600 · 생성 5400~10800초'];
      }
      card.innerHTML = '';
      lines.forEach((l, k) => { const p = el('p', { style: `--d:${k}` }, l); card.append(p); });
      card.dataset.kind = st === '완료' ? 'ok' : (st === '멈춤' ? 'stop' : 'warn');
      mState.textContent = st; mNext.textContent = next; mReq.textContent = req;
    }
    draw();
    return {};
  }

  /* ---------- 02: light JOB gate ---------- */
  function simGate(root) {
    const { view, ctrl, metrics } = panel(root, 'light JOB 게이트 — 요청 → 실행 → 검증 → 완료');
    const stages = [
      ['요청', 'request.md', '범위와 완료 조건 고정'],
      ['실행', 'execution.md', '허용 경계 안에서 수행'],
      ['검증', 'verification.md', '실물과 완료 조건 대조'],
      ['완료', 'result.md', '결과 · 남은 것 · 교훈 링크'],
    ];
    const files = { 'approval.md': true, 'request.md': true, 'execution.md': true, 'verification.md': true, 'result.md': true };
    let at = -1, blocked = '';
    const svg = svgEl('svg', { viewBox: '0 0 760 230', class: 'sim-svg', role: 'img', 'aria-label': 'light JOB 단계' });
    svg.append(svgEl('path', { id: root.id + '-rail', d: 'M60 110H700', class: 'sim-rail' }));
    const nodes = stages.map(([name, file], k) => {
      const x = 60 + k * 213.3;
      const g = svgEl('g', { class: 'sim-node' });
      g.append(svgEl('circle', { cx: x, cy: 110, r: 34 }), svgEl('text', { x, y: 118, class: 'n' }, name), svgEl('text', { x, y: 178, class: 'f' }, file));
      svg.append(g);
      return g;
    });
    const token = svgEl('circle', { r: 11, cx: 60, cy: 58, class: 'sim-token' });
    const barrier = svgEl('g', { class: 'sim-barrier' });
    barrier.append(svgEl('rect', { x: -6, y: 66, width: 12, height: 88, rx: 3 }), svgEl('text', { x: 0, y: 52 }, '게이트 차단'));
    svg.append(barrier, token);
    view.append(svg);
    const log = el('ol', { class: 'sim-log' });
    view.append(log);
    const g1 = group(ctrl, '진행');
    button(g1, '1단계 진행', () => advance(), true);
    button(g1, '자동 재생', () => play());
    button(g1, '초기화', () => reset());
    const g2 = group(ctrl, '제출물 (끄면 누락)');
    Object.keys(files).forEach(f => toggle(g2, f, true, v => { files[f] = v; }));
    const mStage = metric(metrics, '현재 단계'), mNeed = metric(metrics, '게이트가 읽는 파일'), mJudge = metric(metrics, '판정');
    root.append(el('p', { class: 'sim-try' }, '해볼 것: verification.md를 끄고 진행하면 게이트가 "검증"에서 멈춥니다. approval.md를 끄면 실행 단계로 넘어가지 못합니다 — light JOB은 실행 전에 승인 근거가 필요합니다. 파일을 다시 켜고 진행하면 그 자리부터 이어집니다.'));
    let timer = null;
    function need(k) { return k === 1 ? ['approval.md', 'execution.md'] : [stages[k][1]]; }
    function advance() {
      const k = at + 1;
      if (k >= stages.length) return false;
      const missing = need(k).filter(f => !files[f]);
      if (missing.length) {
        blocked = missing.join(', ');
        log.append(el('li', { class: 'bad' }, `${stages[k][0]} 전이 거부 — ${blocked} 없음`));
        draw(k, true);
        return false;
      }
      blocked = '';
      at = k;
      log.append(el('li', {}, `${stages[k][0]} 통과 — ${need(k).join(', ')} 확인`));
      draw(k, false);
      return true;
    }
    function play() {
      clearInterval(timer);
      timer = setInterval(() => { if (!advance()) clearInterval(timer); }, reduce ? 50 : 900);
    }
    function reset() { clearInterval(timer); at = -1; blocked = ''; log.innerHTML = ''; draw(0, false); }
    function draw(k, isBlocked) {
      nodes.forEach((n, i) => { n.classList.toggle('done', i <= at); n.classList.toggle('now', i === at); });
      const x = 60 + Math.max(at, 0) * 213.3;
      token.style.transform = `translateX(${x - 60}px)`;
      token.classList.toggle('idle', at < 0);
      barrier.style.transform = `translateX(${60 + k * 213.3 - 106}px)`;
      barrier.classList.toggle('on', isBlocked);
      mStage.textContent = at < 0 ? '시작 전' : stages[at][0];
      mNeed.textContent = at + 1 < stages.length ? need(at + 1).join(' + ') : '—';
      mJudge.textContent = isBlocked ? '차단' : (at === stages.length - 1 ? 'JOB 종결' : (at < 0 ? '대기' : '통과'));
      log.scrollTop = log.scrollHeight;
    }
    reset();
    return { enter: reset };
  }

  /* ---------- 03: 어디에 적을까 ---------- */
  function simShelf(root) {
    const { view, ctrl, metrics } = panel(root, '이 정보는 어디에 적을까 — CLASSIFICATION');
    const shelves = [
      ['skill', '스킬', '반복되는 절차'],
      ['lesson', 'lessons', '사건 · 교훈'],
      ['canon', '실물 정본', '현재 사실'],
      ['memory', 'MEMORY', '사용자 선호'],
      ['policy', 'POLICY.md', '역할 · 권한 · 금지 · 의무'],
    ];
    const items = [
      ['요청서를 등록하는 명령 순서', 'skill'],
      ['3시간 timeout 뒤 산출이 남아 있었다', 'lesson'],
      ['airouter 동시 한도는 3', 'canon'],
      ['확인 질문 없이 추천안으로 진행', 'memory'],
      ['외부 게시는 사용자 승인 필요', 'policy'],
      ['워커 결과가 QA 결함 0이었지만 화면이 깨졌다', 'lesson'],
    ];
    const board = el('div', { class: 'sim-shelves' });
    const bins = {};
    shelves.forEach(([id, name, sub]) => {
      const b = el('div', { class: 'sim-bin', 'data-id': id });
      b.append(el('b', {}, name), el('span', {}, sub), el('div', { class: 'sim-bin-items' }));
      bins[id] = b; board.append(b);
    });
    const deck = el('div', { class: 'sim-cards' });
    view.append(deck, board);
    let right = 0, tries = 0, idx = 0;
    const g = group(ctrl, '분류할 정보');
    const cardText = el('p', { class: 'sim-current' });
    g.append(cardText);
    const g2 = group(ctrl, '보낼 곳');
    shelves.forEach(([id, name]) => button(g2, name, () => pick(id)));
    const g3 = group(ctrl, '');
    button(g3, '처음부터', () => reset());
    const mScore = metric(metrics, '맞힌 수'), mRule = metric(metrics, '규칙'), mLeft = metric(metrics, '남은 카드');
    root.append(el('p', { class: 'sim-try' }, '해볼 것: 같은 내용을 여러 곳에 복사하지 않는 것이 규칙입니다. 절차를 MEMORY에 적거나 사건을 POLICY에 덧붙이면 나중에 서로 어긋납니다.'));
    function show() {
      deck.innerHTML = '';
      if (idx >= items.length) { cardText.textContent = '모두 분류했습니다.'; mLeft.textContent = '0'; return; }
      cardText.textContent = '“' + items[idx][0] + '”';
      deck.append(el('div', { class: 'sim-chip fly' }, items[idx][0]));
      mLeft.textContent = String(items.length - idx);
    }
    function pick(id) {
      if (idx >= items.length) return;
      tries++;
      const [text, ans] = items[idx];
      const ok = id === ans;
      if (ok) right++;
      const chip = el('div', { class: 'sim-chip ' + (ok ? 'ok' : 'moved') }, text);
      $('.sim-bin-items', bins[ans]).append(chip);
      bins[ans].classList.remove('flash'); void bins[ans].offsetWidth; bins[ans].classList.add('flash');
      mScore.textContent = `${right} / ${tries}`;
      mRule.textContent = ok ? '맞음' : `정답: ${shelves.find(s => s[0] === ans)[1]}`;
      idx++; show();
    }
    function reset() { right = tries = idx = 0; $$('.sim-bin-items', board).forEach(b => b.innerHTML = ''); mScore.textContent = '0 / 0'; mRule.textContent = '–'; show(); }
    reset();
    return {};
  }

  /* ---------- 04: 요청 하나의 일생 ---------- */
  function simLifecycle(root) {
    const { view, ctrl, metrics } = panel(root, '요청 하나의 일생 — 등록에서 보고까지');
    const steps = [
      ['사용자', '요청: "사이트를 최신 내용으로 갱신해"', 'u'],
      ['매니저', '직접/위임 판단 → light JOB 생성 · 승인 근거 기록', 'm'],
      ['매니저', 'context pack으로 관련 교훈·결정 확인', 'k'],
      ['매니저', '요청서 작성: 목표 / 완성 기준 / 참조 경로 / 금지 범위', 'm'],
      ['디스패처', 'ensure_request.py 등록 → worker_dispatch.py 실행', 'd'],
      ['워커', 'WORKER.md 규칙으로 수행 · 산출물 기록', 'w'],
      ['워커', '응답서: 같은 request_id · status · 산출 경로', 'w'],
      ['매니저', '핵심 수치 1개를 원천과 직접 대조', 'v'],
      ['게이트', '요청 → 실행 → 검증 → 완료 전이', 'g'],
      ['지식', 'result.md · lessons → 다음 날 위키 요약에 반영', 'k'],
      ['사용자', '결과 · 남은 것 · 교훈 보고', 'u'],
    ];
    const fail = { on: false };
    const lanes = ['사용자', '매니저', '디스패처', '워커', '게이트', '지식'];
    const svg = svgEl('svg', { viewBox: '0 0 760 262', class: 'sim-svg life', role: 'img', 'aria-label': '요청 처리 타임라인' });
    lanes.forEach((l, k) => {
      svg.append(svgEl('text', { x: 8, y: 16 + k * 46, class: 'lane-l' }, l));
      svg.append(svgEl('path', { d: `M92 ${16 + k * 46}H748`, class: 'lane' }));
    });
    const trail = svgEl('path', { class: 'sim-trail', d: '' });
    const dot = svgEl('circle', { r: 10, class: 'sim-token' });
    svg.append(trail, dot);
    view.append(svg);
    const say = el('p', { class: 'sim-say' });
    view.append(say);
    let k = -1, timer = null, pts = [];
    const g1 = group(ctrl, '재생');
    button(g1, '1스텝', () => next(), true);
    button(g1, '자동 재생', () => { clearInterval(timer); timer = setInterval(() => { if (!next()) clearInterval(timer); }, reduce ? 60 : 1100); });
    button(g1, '초기화', () => reset());
    const g2 = group(ctrl, '사고 주입');
    toggle(g2, '워커 시간 초과', false, v => { fail.on = v; reset(); });
    const mWho = metric(metrics, '지금 누가'), mStep = metric(metrics, '단계'), mState = metric(metrics, 'status');
    root.append(el('p', { class: 'sim-try' }, '해볼 것: "워커 시간 초과"를 켜고 재생하면 응답이 partial로 돌아옵니다. 매니저는 같은 크기로 재시도하지 않고, 원인·바꾼 점·남은 항목만 붙인 이어가기 요청을 새 request_id로 보냅니다.'));
    function seq() {
      if (!fail.on) return steps;
      const s = steps.slice(0, 6);
      s.push(['워커', '시간 초과 — 만든 산출물은 보존, status: partial', 'w']);
      s.push(['매니저', '이어가기 1건: 원인 1줄 + 바꾼 점 1줄 + 남은 항목', 'm']);
      s.push(['디스패처', '새 request_id 등록 · timeout 한 단계 상향', 'd']);
      s.push(['워커', '남은 항목 수행 → status: done', 'w']);
      return s.concat(steps.slice(7));
    }
    function next() {
      const s = seq();
      if (k + 1 >= s.length) return false;
      k++;
      const [who, what] = s[k];
      const lane = lanes.indexOf(who);
      const x = 110 + k * (630 / (s.length - 1)), y = 16 + lane * 46;
      pts.push([x, y]);
      trail.setAttribute('d', pts.map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(0) + ' ' + p[1]).join(''));
      const mark = svgEl('circle', { cx: x, cy: y, r: 6, class: 'sim-mark' + (what.includes('partial') || what.includes('초과') ? ' bad' : '') });
      svg.insertBefore(mark, dot);
      dot.setAttribute('cx', x); dot.setAttribute('cy', y);
      say.textContent = `${k + 1}. ${who} — ${what}`;
      mWho.textContent = who; mStep.textContent = `${k + 1} / ${s.length}`;
      mState.textContent = what.includes('partial') ? 'partial' : (k >= s.length - 4 && s.slice(0, k + 1).some(x => x[1].includes('응답서') || x[1].includes('done')) ? 'done' : (k >= 5 ? '수행 중' : '준비'));
      return true;
    }
    function reset() {
      clearInterval(timer); k = -1; pts = [];
      $$('.sim-mark', svg).forEach(m => m.remove());
      trail.setAttribute('d', ''); dot.setAttribute('cx', -20); dot.setAttribute('cy', -20);
      say.textContent = '1스텝을 눌러 요청 하나를 따라가 보세요.';
      mWho.textContent = '–'; mStep.textContent = `0 / ${seq().length}`; mState.textContent = '–';
    }
    reset();
    return { enter: reset };
  }

  const SIMS = { delegate: simDelegate, verdict: simVerdict, gate: simGate, shelf: simShelf, lifecycle: simLifecycle };
  function init() {
    $$('[data-sim]').forEach((root, i) => {
      if (!root.id) root.id = 'sim-' + i;
      const f = SIMS[root.dataset.sim];
      if (f) root.__sim = f(root);
    });
    // stop deck navigation keys from firing while operating a simulator
    $$('.sim').forEach(s => s.addEventListener('keydown', e => { if (e.target.closest('button')) e.stopPropagation(); }));
    if (!reduce) requestAnimationFrame(tick);
  }
  window.__motion = { init, enter, step, builds };
})();
