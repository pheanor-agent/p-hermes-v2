"""Meaning contracts of the example slides survive layout changes; browser checks cover actual motion."""
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import deckify


class VisualReviewContracts(unittest.TestCase):
    def slide(self, num, key):
        fn, _, _ = next(x for x in deckify.LECTURES if x[1] == num)
        return next(s for s in deckify.parse((ROOT / 'site/lectures' / fn).read_text(), num) if s['key'] == key)

    def render(self, num):
        fn, _, name = next(x for x in deckify.LECTURES if x[1] == num)
        return deckify.render(num, name, deckify.parse((ROOT / 'site/lectures' / fn).read_text(), num))

    def test_sample_scope_shows_what_the_model_did_not_read(self):
        s = str(self.slide('00', '00-ex'))
        for term in ['3행', '2/3', '200행', '40건', '20%']:
            self.assertIn(term, s)

    def test_completion_criteria_do_not_prescribe_results(self):
        request = self.slide('01', '01-ex')
        self.assertNotIn('20%', request['scene'])
        self.assertIn('원자료', request['scene'])
        self.assertIn('대조', request['scene'])

    def test_examples_keep_their_evidence(self):
        self.assertIn('검증', self.slide('02', '02-ex')['scene'])
        self.assertIn('출처', str(self.slide('03', '03-ex')))
        self.assertIn('20%', str(self.slide('04', '04-ex')))

    def test_nojs_retains_concrete_evidence(self):
        static = self.render('00').split('<noscript>')[-1]
        self.assertIn('배송 문의 2/3', static)
        self.assertIn('배송 40건', static)

    def test_mobile_relations_are_authored_and_do_not_require_panning(self):
        for num in ('00', '01', '02', '03', '04'):
            rendered = self.render(num)
            self.assertIn('mobile-relationship', rendered)
            self.assertNotIn('그림은 가로로 밀어', rendered)
            self.assertNotIn('mobile-scene-summary', rendered)


if __name__ == '__main__':
    unittest.main()
