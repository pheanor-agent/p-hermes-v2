"""Assemble authored lessons and explicit keyword definitions into six courses.

The lesson files contain the teaching argument, visual data, answers and notes.
The blueprint supplies agreed coverage and timing, never presentation body copy.
"""
from copy import deepcopy
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
SLUGS=['overview','tasks','knowledge','catalog','image','video']
CODE={'overview':'__main__.py','tasks':'store.py','knowledge':'store.py','catalog':'catalog.py','image':'catalog.py','video':'media.py'}
TITLES=['에이전트가 일을 이어가는 구조','작업을 끝내는 조건','다시 쓸 수 있는 근거','실행 자원을 고르는 기준','의도를 화면으로 옮기기','장면을 시간으로 연결하기']

def main():
    blueprint=json.loads((ROOT/'design/course-blueprint.json').read_text(encoding='utf-8'))
    preview=json.loads((ROOT/'content/slides/courses/preview.json').read_text(encoding='utf-8'))
    prototypes={s['scene']:s for s in preview['slides']}
    for index,course in enumerate(blueprint['courses']):
        slug=SLUGS[index]
        path=ROOT/f'content/slides/lessons/{slug}.json'
        if not path.exists():continue
        lessons=json.loads(path.read_text(encoding='utf-8'))
        assert [x['scene'] for x in lessons]==[x['id'] for x in course['scenes']]
        definitions={k['term']:k for k in course['keywords']}
        seen=set();slides=[]
        sources=[{'label':'개념과 적용 범위','url':f'https://pheanor-agent.github.io/p-hermes-v2/wiki/{"start" if slug=="overview" else slug}.html'}, {'label':'실행 계약 구현','url':f'https://github.com/pheanor-agent/p-hermes-v2/blob/main/src/p_hermes/{CODE[slug]}'}]
        for scene,lesson in zip(course['scenes'],lessons):
            definitions_now=[k for k in lesson['keywords'] if k not in seen]
            seen.update(lesson['keywords'])
            parts=[]
            for part_index,part in enumerate(lesson['screens']):
                if part.get('prototype'):
                    part=deepcopy(prototypes[part['prototype']])
                    part.pop('notes',None)
                else:part=deepcopy(part)
                custom_notes=part.pop('notes',{})
                part['caption']=part.get('caption',lesson['scope'])
                part['notes']={'say':lesson['explain'] if part_index else lesson['explain'][:2],
                    'cues': [f'이 장면 전체 {scene["duration_minutes"]}분. 화면 {part_index+1}의 대상을 먼저 읽습니다.',lesson['cue'], '질문 뒤 15초 기다리고 관찰 근거를 한 가지 듣습니다. 공개 단계는 발표자가 진행합니다.'],
                    'question':lesson['question'],'answer':lesson['answer'],
                    'bridge': scene['bridge'] if part_index==len(lesson['screens'])-1 else '지금 관찰한 차이를 정의와 규칙으로 연결합니다.', 'sources':sources}
                part['notes'].update(custom_notes)
                parts.append(part)
                if part_index==0:
                    for term in definitions_now:
                        k=definitions[term]
                        parts.append({'kind':'definition','keyword':term,'title':term,'dark':True,
                            'data':{'definition':k['definition'],'terms':lesson.get('anchors',[]),'application':k['context'].replace('`','')},
                            'caption':f'{course["title"]}의 핵심 개념 · 다음 화면에서 이 정의를 적용합니다.',
                            'notes':{'say':[f'{term}: {k["definition"]}.',f'앞 화면에서 본 대상을 이 말로 부릅니다. 적용 맥락은 {k["context"]}입니다.',lesson['explain'][-1]],
                                'cues':['단어를 먼저 말하고 정의를 한 번 읽습니다.','청중이 앞 화면의 대상을 떠올린 뒤 다음 화면으로 진행합니다.'],
                                'question':f'앞에서 본 대상 중 {term}에 해당하는 것은 무엇인가요?', 'answer':k['context'].replace('`',''), 'bridge':scene['bridge'],'sources':sources}})
            weights=[0.7 if p['kind']=='definition' else 1.3 for p in parts]
            total=scene['duration_minutes']*60;elapsed=0
            for i,(part,weight) in enumerate(zip(parts,weights)):
                duration=round(total*weight/sum(weights)) if i<len(parts)-1 else total-elapsed
                elapsed+=duration
                part.update(id=f'{scene["id"]}-{i+1}',scene=scene['id'],seconds=duration)
                part.setdefault('keyword',f'{course["title"]} · '+ ' · '.join(lesson['keywords']))
                slides.append(part)
        assert seen==set(definitions), (slug,seen,set(definitions))
        assert sum(s['seconds'] for s in slides)==course['teaching_minutes']*60
        slides.append({'id':'questions','scene':'QA','kind':'recall','title':'내 작업에 적용한다면','keyword':course['title']+' · 질문과 적용','dark':True,'seconds':course['qa_minutes']*60,
            'data':{'questions':['내 작업의 어느 판단에 적용할까요?','직접 확인할 입력과 근거는 무엇인가요?'],'answer':'키워드 하나를 골라, 바꿀 행동과 확인 방법을 함께 설명합니다.'},'caption':'질문 10분 · 읽을 자료와 실행 예제는 강의 목록에서 이어집니다.',
            'notes':{'say':['청중의 실제 작업에서 나온 질문을 받습니다. 질문을 오늘 배운 키워드에 연결해 다시 표현합니다.','공개 코드가 확인하는 범위와 운영 환경에서 따로 확인할 사항을 구분하여 답합니다.','질문이 없으면 청중 한 명의 작업을 예로 들어 입력, 판단, 결과와 확인 방법을 함께 적습니다.'], 'cues':['질문 2분, 적용 사례 5분, 실행할 다음 행동 3분을 기준으로 조절합니다.'],'question':'다음에 바꿀 행동 한 가지는 무엇인가요?','answer':'각자의 작업에 따라 답은 달라집니다. 확인할 입력이나 결과를 구체적으로 지정하면 됩니다.','bridge':'강의 목록의 블로그와 위키에서 필요한 부분을 다시 읽습니다.','sources':sources}})
        result={'slug':slug,'title':TITLES[index],'course':course['title'],'status':'screen_reviewed','teaching_minutes':course['teaching_minutes'],'qa_minutes':course['qa_minutes'],'keywords':course['keywords'],'description':f'{course["title"]} 강의. {course["teaching_minutes"]}분 설명과 적용, 10분 질문.','slides':slides}
        out=ROOT/f'content/slides/courses/{slug}.json'
        out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(slug,len(slides),'slides,',course['teaching_minutes'],'teaching minutes')

if __name__=='__main__':main()
