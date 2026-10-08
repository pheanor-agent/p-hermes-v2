"""Lecture continuity contracts: original pages stay distinct from added evidence."""
from pathlib import Path
import re
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import deckify

class LectureFlowTests(unittest.TestCase):
    def sources(self):
        for fn,num,title in deckify.LECTURES:
            yield fn,num,title,deckify.parse((ROOT/'site/lectures'/fn).read_text(),num)

    def test_original_pages_survive_and_evidence_pages_follow_their_concept(self):
        original_counts={'00':11,'01':12,'02':12,'03':11,'04':8}
        predecessors={'00-example-input':'00-02','00-example-handoff':'00-04',
                      '01-example-contract':'01-03','01-example-request':'01-07','01-example-response':'01-10',
                      '02-example-transition':'02-02','02-example-records':'02-06','02-example-quality':'02-08',
                      '03-example-rule':'03-02','03-example-source':'03-06','03-example-lesson':'03-08','03-example-current':'03-11',
                      '04-example-proof':'04-02','04-example-transfer':'04-05'}
        total=0
        for fn,num,_,slides in self.sources():
            keys=[s['key'] for s in slides]
            self.assertEqual(len(keys),len(set(keys)),fn)
            originals=[k for k in keys if '-example-' not in k]
            self.assertEqual(originals,[f'{num}-{i:02d}' for i in range(1,original_counts[num]+1)])
            for key in keys:
                if key in predecessors:self.assertEqual(keys[keys.index(key)-1],predecessors[key],key)
            self.assertNotIn('lesson-flow',(ROOT/'site/lectures'/fn).read_text())
            total+=len(slides)
        self.assertEqual(total,54+len(predecessors))

    def test_automatic_examples_are_preserved_and_render_as_examples(self):
        kinds=[]
        for _,num,title,slides in self.sources():
            rendered=deckify.render(num,title,slides)
            self.assertEqual(rendered.count('class="dk-slide '),len(slides))
            for s in slides:
                if s['sim']:
                    kinds.append(deckify.attr(s['sim'],'data-sim'))
                    self.assertEqual(s['kind'],'sim')
                    self.assertIn('sim-static',rendered)
        self.assertCountEqual(kinds,['delegate','verdict','gate','shelf','lifecycle'])

    def test_added_slides_maintain_question_continuity(self):
        for fn,_,_,slides in self.sources():
            for i,s in enumerate(slides):
                if '-example-' in s['key']:
                    self.assertTrue(s['next'],s['key'])
                    if slides[i-1]['kind']!='interlude':self.assertTrue(slides[i-1]['next'],s['key'])
                    self.assertNotEqual(slides[i-1]['next'],s['next'],s['key'])
                    self.assertTrue(s['scene'],fn)

if __name__=='__main__':unittest.main()
