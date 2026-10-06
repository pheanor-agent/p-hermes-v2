/* p-hermes motion layer: line draw-in, packets travelling along wires, timed builds
   and self-playing demonstrations. Nothing needs viewer input; everything starts when
   a slide becomes active and stops when it leaves. Respects reduced motion. */
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
  const NS = 'http://www.w3.org/2000/svg';
  const svgEl = (tag, attrs = {}, text) => {
    const n = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    if (text !== undefined) n.textContent = text;
    return n;
  };
  const SPEED = reduce ? 0.15 : 1;

  /* ---------- per-slide timers: cleared whenever the slide is left ---------- */
  function later(slide, ms, fn) {
    const gen = slide.__gen;
    const id = setTimeout(() => { if (slide.__gen === gen && slide.classList.contains('is-active')) fn(); }, ms * SPEED);
    (slide.__timers = slide.__timers || []).push(id);
  }
  function clearTimers(slide) { (slide.__timers || []).forEach(clearTimeout); slide.__timers = []; slide.__gen = (slide.__gen || 0) + 1; }

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
  function tick(now) {
    for (const k of packets) {
      if (!k.slide.classList.contains('is-active')) continue;
      if (k.p.closest('[data-build]:not(.built)')) { k.p.style.opacity = 0; continue; }
      let t = (now - (k.slide.__t0 || now)) / 1000 - k.delay;
      if (t < 0) { k.p.style.opacity = 0; continue; }
      let u = t / k.dur;
      u = k.loop ? u % 1 : Math.min(u, 1);
      const pt = k.path.getPointAtLength(u * k.len);
      k.p.setAttribute('cx', pt.x.toFixed(1));
      k.p.setAttribute('cy', pt.y.toFixed(1));
      k.p.style.opacity = k.loop ? Math.min(1, Math.min(u, 1 - u) * 8) : 1;
    }
    requestAnimationFrame(tick);
  }

  /* ---------- builds: [data-build=n] appear one after another, automatically ---------- */
  function builds(slide) { return Math.max(0, ...$$('[data-build]', slide).map(b => +b.dataset.build)); }
  function setBuild(slide, n) {
    $$('[data-build]', slide).forEach(b => b.classList.toggle('built', +b.dataset.build <= n));
  }
  function enter(slide) {
    clearTimers(slide);
    slide.__t0 = performance.now();
    bindPackets(slide);
    setBuild(slide, 0);
    const total = builds(slide);
    const gap = +(slide.dataset.buildGap || 1500);
    for (let n = 1; n <= total; n++) later(slide, 1300 + (n - 1) * gap, () => setBuild(slide, n));
    slide.classList.remove('mo-play'); void slide.offsetWidth; slide.classList.add('mo-play');
    $$('[data-sim]', slide).forEach(s => s.__sim && s.__sim(slide));
  }
  function leave(slide) { clearTimers(slide); }

  /* ---------- self-playing demo scaffolding ---------- */
  function panel(root, title) {
    root.classList.add('sim');
    root.innerHTML = '';
    const head = el('div', { class: 'sim-head' });
    head.append(el('span', { class: 'sim-tag' }, 'DEMO'), el('b', {}, title), el('span', { class: 'sim-live' }, '자동 재생'));
    const view = el('div', { class: 'sim-view' });
    const metrics = el('div', { class: 'sim-metrics' });
    const say = el('p', { class: 'sim-say' });
    root.append(head, view, metrics, say);
    return { view, metrics, say };
  }
  function metric(metrics, label) {
    const box = el('div', { class: 'sim-metric' });
    const v = el('strong', {}, '–');
    box.append(el('span', {}, label), v);
    metrics.append(box);
    return v;
  }
  function flash(node) { node.classList.remove('sim-flash'); void node.getBoundingClientRect(); node.classList.add('sim-flash'); }
  function setText(node, t) { if (node.textContent !== t) { node.textContent = t; flash(node); } }

  /* ---------- 01: 직접 할까, 맡길까 ---------- */
  function simDelegate(root) {
    const { view, metrics, say } = panel(root, '직접 할까, 맡길까 — 네 가지 경우');
    const cases = [
      { name: '설정 파일 한 줄 수정', tags: ['짧음', '되돌릴 수 있음'], ans: [0, 0, 0], who: '지휘 에이전트가 직접', why: '읽기·작은 수정', rec: '백업 + 원장 한 줄', kind: 'manager' },
      { name: '수백 개 파일 일괄 변환', tags: ['오래 걸림', '산출 큼'], ans: [0, 1, 0], who: '작업 에이전트에 위임', why: '긴 실행·큰 산출', rec: '요청서 · 응답서', kind: 'worker' },
      { name: '강의 자료 새 디자인', tags: ['오래 걸림', '품질 판단'], ans: [0, 1, 1], who: '판단은 지휘 · 실행은 작업', why: '품질을 좌우하는 판단', rec: 'JOB + 요청서', kind: 'worker' },
      { name: '공개 사이트에 게시', tags: ['외부 게시'], ans: [1], who: '사용자 승인 후 진행', why: '되돌릴 수 없는 범주', rec: '승인 원문 기록', kind: 'stop' },
    ];
    const qs = [['되돌릴 수 없는 4개 범주인가?', '영구 삭제 · 외부 게시 · 자격증명 · 규칙 개정'],
                ['오래 걸리거나 산출이 큰가?', '긴 실행 · 대량 파일 · 반복'],
                ['품질을 좌우하는 판단인가?', '설계 · 정책 · 글 완성도 · 시각 결과']];
    const card = el('div', { class: 'sim-case' });
    const flow = el('div', { class: 'sim-flow' });
    const rows = qs.map(([q, sub]) => { const r = el('div', { class: 'sim-q' }); r.append(el('b', {}, q), el('span', {}, sub), el('em', {}, '')); flow.append(r); return r; });
    view.append(card, flow);
    const mWho = metric(metrics, '누가 하나'), mWhy = metric(metrics, '이유'), mRec = metric(metrics, '남기는 기록');
    return slide => {
      let i = 0;
      const run = () => {
        const c = cases[i % cases.length];
        card.innerHTML = '';
        card.append(el('span', { class: 'sim-case-n' }, `경우 ${i % cases.length + 1} / ${cases.length}`), el('b', {}, c.name));
        c.tags.forEach(t => card.append(el('i', {}, t)));
        flash(card);
        rows.forEach(r => { r.className = 'sim-q'; r.querySelector('em').textContent = ''; });
        [mWho, mWhy, mRec].forEach(m => { m.textContent = '…'; m.parentNode.removeAttribute('data-kind'); });
        say.textContent = '질문을 위에서부터 차례로 확인합니다.';
        c.ans.forEach((a, k) => later(slide, 700 + k * 800, () => {
          rows[k].classList.add(a ? 'hit' : 'pass');
          rows[k].querySelector('em').textContent = a ? '예' : '아니오';
        }));
        later(slide, 700 + c.ans.length * 800 + 200, () => {
          setText(mWho, c.who); setText(mWhy, c.why); setText(mRec, c.rec);
          mWho.parentNode.dataset.kind = c.kind;
          say.textContent = `→ ${c.who}`;
        });
        i++;
        later(slide, 700 + c.ans.length * 800 + 2600, run);
      };
      run();
    };
  }

  /* ---------- 01: 응답 판정 ---------- */
  function simVerdict(root) {
    const { view, metrics, say } = panel(root, '응답이 돌아왔을 때 — 판정과 복구');
    const cases = [
      ['done · 대조 완료', ['응답서 status: done', '핵심 수치 1개를 원천과 대조 ✓', '시각 산출은 직접 보고 판정'], '완료', '사용자에게 결과 보고', 'ok'],
      ['done · 대조 전', ['응답서 status: done', '아직 원천과 대조하지 않음', '보고 문장만으로 완료 처리하지 않음'], '확인 전', '원천과 직접 대조', 'warn'],
      ['partial', ['원 목표는 그대로', '+ 직전 실패 원인 1줄', '+ 바꾼 점 1줄 + 남은 항목', '새 조건·게이트는 덧붙이지 않음'], '이어가기', '새 request_id로 1건', 'warn'],
      ['시간 초과', ['만든 산출물은 보존', '같은 크기로 재시도하지 않음', '시간을 늘리거나 작게 나눔'], '크기 조정', '나눠서 다시 요청', 'warn'],
      ['blocked', ['실제 승인이 필요한 부분만', '선택형 질문 1개로 묻고', '나머지는 계속 진행'], '승인 확인', '사용자에게 질문 1개', 'stop'],
      ['같은 사유 2회', ['같은 요청을 반복하지 않음', '원인을 한 번 진단', '원인 · 조치 · 상태를 기록'], '멈춤', '진단 후 보고', 'stop'],
    ];
    const tab = el('div', { class: 'sim-tabs' });
    const tabs = cases.map(c => { const t = el('span', {}, c[0]); tab.append(t); return t; });
    const card = el('div', { class: 'sim-card' });
    view.append(tab, card);
    const mState = metric(metrics, '판정'), mNext = metric(metrics, '다음 행동'), mN = metric(metrics, '경우');
    return slide => {
      let i = 0;
      const run = () => {
        const k = i % cases.length, [name, lines, st, next, kind] = cases[k];
        tabs.forEach((t, j) => t.classList.toggle('on', j === k));
        card.innerHTML = ''; card.dataset.kind = kind;
        lines.forEach((l, j) => card.append(el('p', { style: `--d:${j}` }, l)));
        setText(mState, st); setText(mNext, next); mN.textContent = `${k + 1} / ${cases.length}`;
        say.textContent = `응답: ${name}`;
        i++;
        later(slide, 3400, run);
      };
      run();
    };
  }

  /* ---------- 02: light JOB 게이트 ---------- */
  function simGate(root) {
    const { view, metrics, say } = panel(root, 'light JOB 게이트 — 파일이 빠지면 멈춘다');
    const stages = [['요청', 'request.md'], ['실행', 'approval.md · execution.md'], ['검증', 'verification.md'], ['완료', 'result.md']];
    const svg = svgEl('svg', { viewBox: '0 0 820 220', class: 'sim-svg gate', role: 'img', 'aria-label': 'light JOB 네 단계와 게이트' });
    const X = k => 90 + k * 213;
    svg.append(svgEl('path', { d: 'M90 118H729', class: 'sim-rail' }));
    const token = svgEl('circle', { r: 12, cx: 90, cy: 54, class: 'sim-token' });
    svg.append(token);
    const nodes = stages.map(([n, f], k) => {
      const g = svgEl('g', { class: 'sim-node' });
      g.append(svgEl('circle', { cx: X(k), cy: 118, r: 40 }), svgEl('text', { x: X(k), y: 126, class: 'n' }, n), svgEl('text', { x: X(k), y: 194, class: 'f' }, f));
      svg.append(g); return g;
    });
    const barrier = svgEl('g', { class: 'sim-barrier' });
    barrier.append(svgEl('rect', { x: -7, y: 70, width: 14, height: 96, rx: 3 }), svgEl('text', { x: 0, y: 190 }, '게이트 차단'));
    barrier.style.transform = 'translateX(200px)';
    svg.append(barrier);
    const files = el('div', { class: 'sim-files' });
    const names = ['request.md', 'approval.md', 'execution.md', 'verification.md', 'result.md'];
    const chips = Object.fromEntries(names.map(n => { const c = el('span', {}, n); files.append(c); return [n, c]; }));
    view.append(svg, files);
    const mRun = metric(metrics, '실행'), mStage = metric(metrics, '현재 단계'), mJudge = metric(metrics, '게이트 판정');
    const need = k => (k === 1 ? ['approval.md', 'execution.md'] : [names[k + 1]]);
    return slide => {
      let run = 0;
      const cycle = () => {
        const missing = run % 2 ? 'verification.md' : null;
        names.forEach(n => chips[n].className = n === missing ? 'missing' : 'ok');
        nodes.forEach(n => n.setAttribute('class', 'sim-node'));
        nodes[0].setAttribute('class', 'sim-node done');
        token.style.transform = 'translateX(0px)'; barrier.classList.remove('on');
        setText(mRun, missing ? '② 파일 누락' : '① 파일 모두 있음');
        mStage.textContent = '요청'; mJudge.textContent = '대기';
        say.textContent = missing ? '이번에는 verification.md가 빠진 상태로 진행합니다.' : '필수 파일이 모두 있는 JOB이 단계를 통과합니다.';
        let t = 1000;
        [1, 2, 3].forEach(k => {
          const lack = need(k).filter(f => f === missing);
          if (lack.length) {
            later(slide, t, () => {
              barrier.style.transform = `translateX(${X(k) - 106}px)`; barrier.classList.add('on');
              setText(mJudge, '차단'); say.textContent = `${stages[k][0]} 단계로 못 넘어갑니다 — ${lack[0]}가 없습니다.`;
            });
            t += 2000;
            later(slide, t, () => {
              chips[missing].className = 'ok added'; barrier.classList.remove('on');
              say.textContent = `${lack[0]}를 채우면 그 자리부터 이어집니다.`;
            });
            t += 1300;
          }
          later(slide, t, () => {
            token.style.transform = `translateX(${X(k) - 90}px)`;
            nodes[k].setAttribute('class', 'sim-node done');
            setText(mStage, stages[k][0]); setText(mJudge, '통과');
            if (!lack.length) say.textContent = `${stages[k][0]} 통과 — 게이트가 ${need(k).join(', ')}를 읽었습니다.`;
          });
          t += 1200;
        });
        later(slide, t + 300, () => { setText(mJudge, 'JOB 종결'); say.textContent = '네 단계를 모두 통과해 JOB이 종결됩니다.'; });
        run++;
        later(slide, t + 2700, cycle);
      };
      cycle();
    };
  }

  /* ---------- 03: 어디에 적을까 ---------- */
  function simShelf(root) {
    const { view, metrics, say } = panel(root, '이 정보는 어디에 적을까');
    const shelves = [['skill', '스킬', '반복되는 절차'], ['lesson', 'lessons', '사건 · 교훈'], ['canon', '실물 정본', '현재 사실'],
                     ['memory', 'MEMORY', '사용자 선호'], ['policy', 'POLICY', '역할 · 권한 · 금지']];
    const items = [['요청서를 등록하는 명령 순서', 'skill', '“어떻게”는 절차라서 스킬에 둡니다.'],
                   ['시간 초과 뒤에도 산출이 남아 있었다', 'lesson', '“무슨 일이 왜”는 사건이라서 교훈에 둡니다.'],
                   ['지금 활성화된 단계 정의', 'canon', '“지금 무엇이”는 실물 파일에서 직접 읽습니다.'],
                   ['확인 질문 없이 추천안으로 진행', 'memory', '사용자가 원하는 방식은 선호로 둡니다.'],
                   ['외부 게시는 사용자 승인 필요', 'policy', '권한과 금지는 규칙에 둡니다.'],
                   ['검사는 통과했지만 화면이 깨졌다', 'lesson', '실패 사례는 교훈으로 남깁니다.']];
    const stage = el('div', { class: 'sim-chipstage' });
    const board = el('div', { class: 'sim-shelves' });
    const bins = {};
    shelves.forEach(([id, n, sub]) => { const b = el('div', { class: 'sim-bin' }); b.append(el('b', {}, n), el('span', {}, sub), el('div', { class: 'sim-bin-items' })); bins[id] = b; board.append(b); });
    view.append(stage, board);
    const mTo = metric(metrics, '보낼 곳'), mQ = metric(metrics, '답하는 질문'), mN = metric(metrics, '분류');
    const Q = { skill: '어떻게', lesson: '무슨 일이 왜', canon: '지금 무엇이', memory: '무엇을 좋아하나', policy: '해도 되나' };
    return slide => {
      let i = 0;
      const run = () => {
        if (i % items.length === 0) $$('.sim-bin-items', board).forEach(b => b.innerHTML = '');
        const [text, to, why] = items[i % items.length];
        stage.innerHTML = '';
        const chip = el('div', { class: 'sim-chip fly' }, text); stage.append(chip);
        mTo.textContent = '…'; mQ.textContent = '…'; mN.textContent = `${i % items.length + 1} / ${items.length}`;
        say.textContent = '이 정보는 어떤 질문에 답할까요?';
        later(slide, 1500, () => {
          chip.classList.add('gone');
          $('.sim-bin-items', bins[to]).append(el('div', { class: 'sim-chip ok' }, text));
          flash(bins[to]); setText(mTo, shelves.find(s => s[0] === to)[1]); setText(mQ, Q[to]); say.textContent = why;
        });
        i++;
        later(slide, 3400, run);
      };
      run();
    };
  }

  /* ---------- 04: 요청 하나의 일생 ---------- */
  function simLifecycle(root) {
    const { view, metrics, say } = panel(root, '요청 하나의 일생');
    const base = [
      ['사용자', '요청: 사이트를 최신 내용으로 갱신'], ['지휘', '직접/위임 판단 → light JOB · 승인 원문 기록'], ['지휘', 'context pack으로 관련 교훈 확인'],
      ['지휘', '요청서: 목표 / 완성 기준 / 참조 / 금지'], ['디스패처', '등록 → 작업 에이전트 실행'], ['작업', '요청서대로 끝까지 수행 · 산출 기록'],
      ['작업', '응답서: 같은 request_id · status: done'], ['지휘', '핵심 수치 1개를 원천과 대조'], ['게이트', '요청 → 실행 → 검증 → 완료'],
      ['지식', 'result.md · 교훈 후보 → 매일 요약'], ['사용자', '결과 · 남은 것 · 교훈 보고'],
    ];
    const failSeq = base.slice(0, 6).concat([
      ['작업', '시간 초과 — 산출은 보존, status: partial'], ['지휘', '이어가기: 원인 + 바꾼 점 + 남은 항목'],
      ['디스패처', '새 request_id · 시간 한 단계 늘림'], ['작업', '남은 항목 수행 → status: done'],
    ], base.slice(7));
    const lanes = ['사용자', '지휘', '디스패처', '작업', '게이트', '지식'];
    const svg = svgEl('svg', { viewBox: '0 0 900 262', class: 'sim-svg life', role: 'img', 'aria-label': '요청 처리 타임라인' });
    lanes.forEach((l, k) => { svg.append(svgEl('text', { x: 8, y: 18 + k * 45, class: 'lane-l' }, l)); svg.append(svgEl('path', { d: `M96 ${18 + k * 45}H890`, class: 'lane' })); });
    const trail = svgEl('path', { class: 'sim-trail', d: '' });
    const dot = svgEl('circle', { r: 11, class: 'sim-token', cx: -30, cy: -30 });
    svg.append(trail, dot);
    view.append(svg);
    const mRun = metric(metrics, '재생'), mWho = metric(metrics, '지금 누가'), mState = metric(metrics, 'status');
    return slide => {
      let run = 0;
      const cycle = () => {
        const seq = run % 2 ? failSeq : base;
        $$('.sim-mark', svg).forEach(m => m.remove());
        trail.setAttribute('d', ''); const pts = [];
        setText(mRun, run % 2 ? '② 시간 초과' : '① 정상 흐름'); mState.textContent = '준비';
        seq.forEach(([who, what], k) => later(slide, 600 + k * 950, () => {
          const x = 116 + k * (760 / (seq.length - 1)), y = 18 + lanes.indexOf(who) * 45;
          pts.push([x, y]);
          trail.setAttribute('d', pts.map((p, j) => (j ? 'L' : 'M') + p[0].toFixed(0) + ' ' + p[1]).join(''));
          svg.insertBefore(svgEl('circle', { cx: x, cy: y, r: 6, class: 'sim-mark' + (what.includes('partial') ? ' bad' : '') }), dot);
          dot.setAttribute('cx', x); dot.setAttribute('cy', y);
          say.textContent = `${k + 1}. ${who} — ${what}`;
          setText(mWho, who);
          if (what.includes('partial')) setText(mState, 'partial'); else if (what.includes('done')) setText(mState, 'done'); else if (k === 5) setText(mState, '수행 중');
        }));
        run++;
        later(slide, 600 + seq.length * 950 + 2200, cycle);
      };
      cycle();
    };
  }

  const SIMS = { delegate: simDelegate, verdict: simVerdict, gate: simGate, shelf: simShelf, lifecycle: simLifecycle };
  function init() {
    $$('[data-sim]').forEach(root => { const f = SIMS[root.dataset.sim]; if (f) root.__sim = f(root); });
    if (!reduce) requestAnimationFrame(tick);
  }
  window.__motion = { init, enter, leave, builds };
})();
