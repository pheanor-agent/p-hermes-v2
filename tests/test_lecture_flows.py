from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import deckify


class LectureFlowTests(unittest.TestCase):
    def test_all_five_sources_keep_the_established_54_slide_map(self):
        counts = deckify.slide_counts(ROOT / 'site' / 'lectures')
        self.assertEqual(list(counts.values()), [11, 12, 12, 11, 8])
        self.assertEqual(sum(counts.values()), 54)

    def test_semantic_stories_render_without_losing_their_static_text(self):
        total_flows = 0
        expected = {
            '00-overview.html': 1,
            '01-orchestrator-worker.html': 4,
            '02-workflow.html': 2,
            '03-knowledge.html': 2,
            '04-integration.html': 2,
        }
        for filename, number, title in deckify.LECTURES:
            slides = deckify.parse((ROOT / 'site' / 'lectures' / filename).read_text(), number)
            rendered = deckify.render(number, title, slides)
            flows = rendered.count('data-lesson-flow')
            self.assertEqual(flows, expected.get(filename, 0), filename)
            total_flows += flows
            self.assertIn('data-step="1"', rendered) if flows else None
            self.assertIn('<details class="lesson-answer"><summary>', rendered) if flows else None
            self.assertIn('</summary><p>', rendered) if flows else None
        self.assertEqual(total_flows, 11)

    def test_player_owns_step_keys_and_honors_reduced_motion(self):
        deck = (ROOT / 'site' / 'assets' / 'deck.js').read_text()
        motion = (ROOT / 'site' / 'assets' / 'motion.js').read_text()
        self.assertIn("window.__motion.step(flow, 1)", deck)
        self.assertIn("e.target.closest('a,button,summary,details,[data-lesson-flow],[data-diagram]')", deck)
        self.assertIn('if (reduce) { const auto', motion)
        self.assertIn('step(flow, 1, true)', motion)
        self.assertIn('$$(\'[data-lesson-flow]\', slide).forEach(clearLessonTimer)', motion)
        self.assertNotIn('const SPEED = reduce ? 0.15 : 1', motion)

    def test_priority_document_pairs_are_distinct_and_integrated_recall_is_hidden_until_revealed(self):
        sources = ROOT / 'site' / 'lectures'
        targets = {
            '00-overview.html': {'00-02','00-03','00-04','00-07','00-08','00-11'},
            '01-orchestrator-worker.html': {'01-03','01-09','01-10'},
            '02-workflow.html': {'02-06','02-07'},
            '03-knowledge.html': {'03-02','03-03','03-06','03-07','03-08','03-10'},
            '04-integration.html': {'04-02','04-06'},
        }
        import re
        for filename, ids in targets.items():
            source = (sources / filename).read_text()
            sections = re.findall(r'<section class="slide"[^>]*>.*?</section>', source, re.S)
            for sid in ids:
                number, index = sid.split('-')
                section = sections[int(index)-1]
                pair = re.search(r'<div class="case-pair"[^>]*>(.*?)</div>\s*<figcaption>', section, re.S)
                self.assertIsNotNone(pair, sid)
                values = re.findall(r'<div class="case-doc"><b>.*?</b><span>(.*?)</span></div>', pair.group(1), re.S)
                self.assertEqual(len(values), 2, sid)
                self.assertNotEqual(values[0].strip(), values[1].strip(), sid)

        integration = (sources / '04-integration.html').read_text()
        sections = re.findall(r'<section class="slide"[^>]*>.*?</section>', integration, re.S)
        self.assertIn('role-map', sections[2])
        self.assertIn('게이트', sections[2])
        self.assertIn('지식', sections[2])
        recall = sections[7]
        self.assertIn('recall-blank', recall)
        answer = recall.index('답 공개 · 관계 지도 보기')
        answer_map = recall.index('recall-answer-map')
        self.assertLess(answer, answer_map)
        details_open = recall.index('<details class="lesson-answer recall-answer">')
        self.assertLess(details_open, answer_map)


if __name__ == '__main__':
    unittest.main()
