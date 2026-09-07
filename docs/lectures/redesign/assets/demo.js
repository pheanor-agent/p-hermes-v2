/* Original educational demo. No generation API or operational catalogue is invoked. */
(function (root) {
  'use strict';
  function validateFixture(value) {
    const fixture = value && typeof value === 'object' && !Array.isArray(value) ? value : {};
    const errors = [];
    if (fixture.selected_count !== 1) errors.push('COUNT');
    for (const [field, code] of [['template_id', 'TEMPLATE_ID'], ['variant_id', 'VARIANT_ID'], ['release_id', 'RELEASE_ID']]) {
      if (typeof fixture[field] !== 'string' || fixture[field].trim().length === 0) errors.push(code);
    }
    if (fixture.required_text_space === true && (!fixture.variant || fixture.variant.text_space !== true)) errors.push('TEXT_SPACE');
    return {ok: errors.length === 0, errors};
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {validateFixture};
  if (root) root.validateFixture = validateFixture;
  if (typeof document === 'undefined') return;

  const clone = value => JSON.parse(JSON.stringify(value));
  const byId = id => document.getElementById(id);
  async function initialize() {
    if (!byId('fixture-json')) return;
    const status = byId('load-status');
    try {
      const url = new URL('fixtures.json', document.baseURI);
      if (url.origin !== window.location.origin || !['http:', 'https:'].includes(url.protocol)) throw new Error('SAME_ORIGIN_HTTP_REQUIRED');
      const response = await fetch(url.href, {credentials: 'same-origin', mode: 'same-origin'});
      if (!response.ok) throw new Error('FIXTURE_HTTP_' + response.status);
      const data = await response.json();
      if (!data.defaultFixture || !Array.isArray(data.nodes) || data.nodes.length !== 5 || !Array.isArray(data.variants)) throw new Error('FIXTURE_SCHEMA');
      let fixture = clone(data.defaultFixture);
      let nodeId = 'task';
      const slides = ['outcome', 'inside', 'proof'];
      const errorsText = {
        COUNT: '선택 수는 숫자 1이어야 합니다.',
        TEMPLATE_ID: 'template_id는 비어 있지 않은 문자열이어야 합니다.',
        VARIANT_ID: 'variant_id는 비어 있지 않은 문자열이어야 합니다.',
        RELEASE_ID: 'release_id는 비어 있지 않은 문자열이어야 합니다.',
        TEXT_SPACE: '문구 공간이 필수인데 선택한 구성에 공간이 없습니다.'
      };
      function variant() { return data.variants.find(item => item.variant_id === fixture.variant_id); }
      function renderNode() {
        const node = data.nodes.find(item => item.id === nodeId);
        const current = variant();
        document.querySelectorAll('[data-node]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.node === nodeId)));
        byId('node-label').textContent = String(data.nodes.indexOf(node) + 1).padStart(2, '0') + ' / ' + node.title;
        byId('node-question').textContent = node.question;
        byId('node-input').textContent = node.input;
        byId('node-process').textContent = node.process;
        let output = node.output;
        if (nodeId === 'catalog') output = [fixture.template_id, fixture.variant_id, fixture.release_id || '(누락)'].join(' / ') + ' · text_space=' + fixture.variant.text_space;
        if (nodeId === 'image') output = current.composition + ' 교육용 구도이며 실제 생성물 아님.';
        if (nodeId === 'video') output += ' 기준 구성: ' + fixture.variant_id + '.';
        if (nodeId === 'image' || nodeId === 'video') byId('node-input').textContent += ' · ' + fixture.variant_id;
        byId('node-output').textContent = output;
      }
      function render() {
        const current = variant();
        byId('variant-select').value = fixture.variant_id;
        byId('selection-note').textContent = '선택 ' + current.key + ' · ' + fixture.variant_id + ' · 문구 공간 ' + (fixture.variant.text_space ? '있음' : '없음');
        document.querySelectorAll('[data-variant]').forEach(button => {
          const selected = button.dataset.variant === fixture.variant_id;
          button.setAttribute('aria-pressed', String(selected));
          button.querySelector('.choice-state').textContent = selected ? '✓ 선택됨' : '선택하기';
        });
        byId('fault-count').setAttribute('aria-pressed', String(fixture.selected_count !== 1));
        byId('fault-id').setAttribute('aria-pressed', String(!fixture.release_id));
        // The visible JSON and validation always consume this exact same object.
        byId('fixture-json').textContent = JSON.stringify(fixture, null, 2).replace(/"variant": \{\n\s+"text_space": (true|false)\n\s+\}/, '"variant": { "text_space": $1 }');
        const result = validateFixture(fixture);
        const panel = byId('validation-result');
        panel.dataset.status = result.ok ? 'pass' : 'fail';
        panel.dataset.errors = result.errors.join(',');
        byId('result-label').textContent = result.ok ? '✓ PASS · fixture 검사 통과' : '✕ FAIL · ' + result.errors.join(' + ');
        byId('result-detail').textContent = result.ok ? '선택 1개, 식별자 3개, 문구 공간 조건이 맞습니다.' : result.errors.map(code => errorsText[code]).join(' ');
        renderNode();
      }
      function selectVariant(id) {
        const next = data.variants.find(item => item.variant_id === id);
        if (!next) return;
        const missingRelease = !fixture.release_id;
        fixture.template_id = next.template_id;
        fixture.variant_id = next.variant_id;
        fixture.release_id = next.release_id;
        fixture.variant = clone(next.variant);
        if (missingRelease) delete fixture.release_id;
        render();
      }
      function navigate() {
        const candidate = window.location.hash.slice(1);
        const id = slides.includes(candidate) ? candidate : 'outcome';
        document.querySelectorAll('.scene').forEach(scene => {
          const active = scene.id === id;
          scene.classList.toggle('active', active);
          scene.setAttribute('aria-hidden', String(!active));
        });
        document.querySelectorAll('[data-nav]').forEach(link => {
          if (link.dataset.nav === id) link.setAttribute('aria-current', 'page');
          else link.removeAttribute('aria-current');
        });
        document.body.dataset.scene = id;
        window.scrollTo(0, 0);
      }
      document.querySelectorAll('[data-node]').forEach(button => button.addEventListener('click', () => {nodeId = button.dataset.node; renderNode();}));
      document.querySelectorAll('[data-variant]').forEach(button => button.addEventListener('click', () => selectVariant(button.dataset.variant)));
      byId('variant-select').addEventListener('change', event => selectVariant(event.target.value));
      byId('fault-count').addEventListener('click', () => {fixture.selected_count = fixture.selected_count === 1 ? 2 : 1; render();});
      byId('fault-id').addEventListener('click', () => {if (fixture.release_id) delete fixture.release_id; else fixture.release_id = variant().release_id; render();});
      byId('reset').addEventListener('click', () => {fixture = clone(data.defaultFixture); render();});
      window.addEventListener('hashchange', navigate);
      document.addEventListener('keydown', event => {
        if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || /INPUT|SELECT|TEXTAREA/.test(event.target.tagName)) return;
        if ((event.key === 'ArrowRight' || event.key === 'ArrowLeft') && event.target.matches('[data-node]')) {
          const buttons = Array.from(document.querySelectorAll('[data-node]'));
          const next = (buttons.indexOf(event.target) + (event.key === 'ArrowRight' ? 1 : buttons.length - 1)) % buttons.length;
          buttons[next].focus(); event.preventDefault();
        }
        if (event.key === 'PageDown' || event.key === 'PageUp') {
          const next = slides.indexOf(document.body.dataset.scene) + (event.key === 'PageDown' ? 1 : -1);
          if (slides[next]) {event.preventDefault(); window.location.hash = slides[next];}
        }
      });
      // Printing must reveal complete linear content, including the initially closed details.
      let detailsWasOpen = false;
      window.addEventListener('beforeprint', () => {
        const details = document.querySelector('.fallback-nodes'); detailsWasOpen = details.open; details.open = true;
        document.querySelectorAll('.scene').forEach(scene => scene.removeAttribute('aria-hidden'));
      });
      window.addEventListener('afterprint', () => {document.querySelector('.fallback-nodes').open = detailsWasOpen; navigate();});
      root.getLectureState = () => ({fixture: clone(fixture), selectedNode: nodeId, result: validateFixture(fixture)});
      render();
      document.body.classList.add('enhanced');
      navigate();
      document.body.dataset.ready = 'true';
      status.textContent = '교육용 fixture 로딩 완료. 표시한 JSON을 브라우저에서 검사했습니다.';
    } catch (error) {
      status.textContent = '상호작용을 불러오지 못했습니다. 세 화면의 정적 설명은 아래 순서대로 읽을 수 있습니다. 원인: ' + error.message;
      document.querySelectorAll('button, select').forEach(control => {control.disabled = true;});
      document.querySelector('.fallback-nodes').open = true;
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, {once: true});
  else initialize();
})(typeof window !== 'undefined' ? window : null);
