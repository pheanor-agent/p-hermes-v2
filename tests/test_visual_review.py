"""Meaning contracts survive layout restoration; browser checks cover actual motion."""
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import deckify

class VisualReviewContracts(unittest.TestCase):
    def slide(self,num,key):
        fn,_,_=next(x for x in deckify.LECTURES if x[1]==num)
        return next(s for s in deckify.parse((ROOT/'site/lectures'/fn).read_text(),num) if s['key']==key)

    def render(self,num):
        fn,_,name=next(x for x in deckify.LECTURES if x[1]==num)
        return deckify.render(num,name,deckify.parse((ROOT/'site/lectures'/fn).read_text(),num))

    def test_definitions_distinguish_state_change_and_condition(self):
        s=self.slide('02','02-example-transition')['scene']
        for term in ['현재 상태','다음 상태','전이 조건','필수 기준 충족','대조 기록 존재']:self.assertIn(term,s)

    def test_sample_scope_and_completion_criteria_do_not_prescribe_results(self):
        s=self.slide('00','00-example-input')
        self.assertIn('3행',str(s));self.assertIn('전체',str(s));self.assertIn('2/3',s['scene'])
        request=self.slide('01','01-example-request')
        self.assertNotIn('20%',request['scene'])
        self.assertIn('원자료',request['scene']);self.assertIn('대조',request['scene'])

    def test_candidates_and_current_files_are_checked_against_same_raw_data(self):
        s=self.slide('03','03-example-current')
        for term in ['20%','25%','200건','40건']:self.assertIn(term,str(s))
        self.assertIn('25%도 20%',str(s))

    def test_exercise_answer_is_hidden_in_presentation_and_readable_without_js(self):
        s=self.slide('04','04-example-transfer')['scene']
        self.assertIn('data-quiz-answer hidden',s)
        self.assertIn('2 ÷ 10 = 20%',s)
        static=self.render('04').split('<noscript>')[-1]
        self.assertIn('2 ÷ 10 = 20%',static)
        self.assertNotIn('data-quiz-answer hidden',static)

    def test_nojs_retains_concrete_evidence_and_example_fallbacks(self):
        static=self.render('00').split('<noscript>')[-1]
        self.assertIn('배송 문의 2/3',static)
        self.assertIn('결제 문의 1/3',static)
        self.assertIn('검사는 통과했지만 화면이 깨짐',self.render('03').split('<noscript>')[-1])

    def test_mobile_relations_are_authored_and_do_not_require_panning(self):
        rendered=self.render('00')
        self.assertIn('mobile-relationship',rendered)
        self.assertNotIn('그림은 가로로 밀어',rendered)
        self.assertNotIn('mobile-scene-summary',rendered)

if __name__=='__main__':unittest.main()
