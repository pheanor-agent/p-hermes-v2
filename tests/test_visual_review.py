"""Regression contracts from Astra's real-screen review, not learning-outcome tests."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import deckify


class VisualReviewContracts(unittest.TestCase):
    def render(self, name):
        filename, number, title = next(x for x in deckify.LECTURES if x[1] == name)
        slides = deckify.parse((ROOT / 'site/lectures' / filename).read_text(), number)
        return deckify.render(number, title, slides)

    def test_nojs_is_visible_and_retains_authored_steps_and_documents(self):
        rendered = self.render('03')
        static = rendered.split('<noscript>')[-1]
        self.assertIn('dk-static', static)
        self.assertIn('lesson-beats', static)
        self.assertIn('procedure-comparison', static)
        self.assertIn('recall-answer', self.render('04').split('<noscript>')[-1])
        self.assertIn('.dk-viewport,.dk-controls{display:none!important}', rendered)

    def test_caption_semantics_and_distinct_slide_navigation_labels(self):
        rendered = self.render('01')
        self.assertIn('<figcaption>', rendered)
        self.assertIn('aria-label="다음 장"', rendered)
        self.assertNotIn('다음 (단계 또는 슬라이드)', rendered)

    def test_native_details_is_not_deck_navigation(self):
        player = (ROOT / 'site/assets/deck.js').read_text()
        self.assertIn('summary,details', player)
        self.assertIn('s.inert = k !== current', player)

    def test_classification_questions_do_not_publish_their_own_answers(self):
        source = (ROOT / 'site/lectures/03-knowledge.html').read_text()
        self.assertIn('data-question', source)
        self.assertNotIn('data-title="독자 판단" data-focus="절차"', source)
        self.assertNotIn('data-title="독자 판단" data-focus="교훈"', source)

    def test_skill_before_after_is_three_real_lines(self):
        source = (ROOT / 'site/lectures/03-knowledge.html').read_text()
        for line in ('입력 파일을 읽는다.', '한 번에 집계한다.', '보고서를 쓴다.',
                     '입력 파일의 전체 건수를 확인한다.', '양이 많으면 범위를 나누어 집계한다.',
                     '합계와 원자료를 대조하고 보고서를 쓴다.'):
            self.assertIn(line, source)

    def test_semantic_playback_stops_at_questions(self):
        motion = (ROOT / 'site/assets/motion.js').read_text()
        self.assertIn("hasAttribute('data-question')", motion)
        self.assertIn('ensureBeatVisible', motion)

    def test_diagrams_have_a_mobile_reading_surface(self):
        rendered = self.render('00')
        self.assertIn('class="scene-diagram" data-diagram', rendered)
        self.assertIn('그림은 가로로 밀어 읽을 수 있습니다.', rendered)

    def test_astra_fixes_keep_definitions_sources_and_example_results_distinct(self):
        flow = (ROOT / 'site/lectures/02-workflow.html').read_text()
        intro = (ROOT / 'site/lectures/00-overview.html').read_text()
        worker = (ROOT / 'site/lectures/01-orchestrator-worker.html').read_text()
        knowledge = (ROOT / 'site/lectures/03-knowledge.html').read_text()
        integration = (ROOT / 'site/lectures/04-integration.html').read_text()
        self.assertIn('전이: 상태가 바뀌는 일', flow)
        self.assertIn('전이 조건: 넘어갈 기준', flow)
        self.assertIn('교육용 합성 발췌 · 문의.csv', intro)
        self.assertIn('분류 기준: 배송 문의는', knowledge)
        self.assertIn('교육용 합성 카드 · 2026-10-01', knowledge)
        self.assertIn('같은 문의.csv 200건·배송 40건이라면', knowledge)
        self.assertIn('요청서의 완성 기준:', worker)
        self.assertIn('교육용 계산 결과 보기 · 기준값 아님', worker)
        self.assertIn('배송 40건/전체 200건이라면 계산 결과는 20%', worker)
        self.assertIn('class="recall-blank recall-mobile"', integration)
        recall = integration.split('class="recall-blank recall-mobile"', 1)[1].split('</div>', 1)[0]
        self.assertEqual(recall.count('<p>'), 3)

    def test_mobile_step_scroll_and_answer_toggle_recheck_current_evidence(self):
        motion = (ROOT / 'site/assets/motion.js').read_text()
        self.assertIn("matchMedia('(max-width: 760px)')", motion)
        self.assertIn('viewport.scrollTop += br.bottom - safeBottom', motion)
        self.assertIn("disclosure.addEventListener('toggle'", motion)
        self.assertIn('requestAnimationFrame(() => {', motion)
        step_body = motion.split('function step(flow, direction, keepPlayback = false) {', 1)[1].split('function initLessons()', 1)[0]
        self.assertLess(step_body.index('caption.textContent ='), step_body.index('ensureBeatVisible(flow, beat)'))


if __name__ == '__main__':
    unittest.main()
