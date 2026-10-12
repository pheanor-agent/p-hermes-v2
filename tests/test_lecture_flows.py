"""Lecture continuity contracts: authored lectures follow the locked storyboard."""
from pathlib import Path
import re
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import deckify
import storyboard


def plain(s):
    return re.sub(r'<[^>]+>', '', s).strip()


class LectureFlowTests(unittest.TestCase):
    def sources(self):
        for fn, num, title in deckify.LECTURES:
            yield fn, num, title, deckify.parse((ROOT / 'site/lectures' / fn).read_text(), num)

    def boards(self):
        return {num: rows for num, _, _, rows in storyboard.LECTURES}

    def test_slides_match_storyboard_keys_and_titles(self):
        boards = self.boards()
        total = 0
        for fn, num, _, slides in self.sources():
            rows = boards[num]
            self.assertEqual([s['key'] for s in slides], [r[0] for r in rows], fn)
            for s, r in zip(slides, rows):
                self.assertEqual(plain(s['title']), r[1].removeprefix('(KEY) '), s['key'])
                self.assertEqual(s['kind'] == 'interlude', r[1].startswith('(KEY) '), s['key'])
            total += len(slides)
        self.assertEqual(total, sum(len(r) for r in boards.values()))

    def test_next_question_is_the_question_the_following_slide_answers(self):
        flat = [(s, r) for (_, num, _, slides) in self.sources() for s, r in zip(slides, self.boards()[num])]
        for i, (s, _) in enumerate(flat):
            if s['kind'] == 'interlude':
                continue
            following = next((r[2] for _, r in flat[i + 1:] if r[2]), '')
            self.assertEqual(plain(s['next']), following, s['key'])

    def test_one_example_per_lecture_with_scene(self):
        for fn, _, _, slides in self.sources():
            examples = [s for s in slides if s['key'].endswith('-ex')]
            self.assertEqual(len(examples), 1, fn)
            self.assertTrue(examples[0]['scene'] and examples[0]['next'], fn)

    def test_simulators_render_with_static_fallback(self):
        kinds = []
        for _, num, title, slides in self.sources():
            rendered = deckify.render(num, title, slides)
            self.assertEqual(rendered.count('class="dk-slide '), len(slides))
            for s in slides:
                if s['sim']:
                    kinds.append(deckify.attr(s['sim'], 'data-sim'))
                    self.assertEqual(s['kind'], 'sim')
                    self.assertIn('sim-static', rendered)
        self.assertCountEqual(kinds, ['delegate', 'verdict', 'gate'])

    def test_retired_terms_do_not_return(self):
        for fn, _, _, _ in self.sources():
            text = (ROOT / 'site/lectures' / fn).read_text()
            for word in ('작업 에이전트', '작업자', '분류기', '원장', '찾히'):
                self.assertNotIn(word, text, f'{fn}: {word}')


if __name__ == '__main__':
    unittest.main()
