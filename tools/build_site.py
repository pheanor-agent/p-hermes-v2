"""Build the public handbook and blog views from reviewed UTF-8 content.

Python 3.11+, standard library only. Output stays under docs; old preview
addresses remain available. No private environment inspection or network I/O.
"""
from pathlib import Path
import html
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'
REPO = 'https://github.com/pheanor-agent/p-hermes-v2'
DOMAINS = [('tasks','작업','일을 끝내는 구조'),('knowledge','지식','다시 쓰는 근거'),('catalog','카탈로그','자원을 고르는 기준'),('image','이미지','의도를 화면으로'),('video','영상','장면을 시간으로')]

def esc(value): return html.escape(str(value), quote=True)

def inline(value):
    s=esc(value)
    s=re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)

def link(href, label):
    if not isinstance(href,str) or href.startswith(('javascript:', 'data:')): raise ValueError('unsafe link')
    return f'<a href="{esc(href)}">{inline(label)}</a>'

def codeblock(code):
    if not code:return ''
    return f'<div class="code-wrap"><span class="code-label">{esc(code.get("language","code"))}</span><pre><code>{esc(code["text"])}</code></pre></div>'

def lamp(depth=1):
    base='../'*depth
    return f'<img class="lamp-photo" src="{base}assets/luma-left.png" alt="왼쪽의 청록색 램프와 오른쪽 문구 공간. 교육용 생성 이미지.">'


def visual(v, context=''):
    if not v:return ''
    kind=v.get('type','flow'); steps=v.get('steps',[])
    body=''
    if kind=='artifact': body=lamp()
    if kind=='timeline':
        durations=[float(s['duration']) for s in steps]
        if not durations or any(d<=0 for d in durations):raise ValueError('timeline needs positive durations')
        total=sum(durations);elapsed=0;bars=[]
        for step,duration in zip(steps,durations):
            end=elapsed+duration
            scene=step.get('detail',step['label']).split('·')[0].strip()
            bars.append(f'<div style="flex:{duration:g}"><span>{elapsed:g}–{end:g}s</span><strong>{inline(scene)}</strong></div>')
            elapsed=end
        body+='<div class="time-track" aria-label="시간에 비례한 샷 길이">'+''.join(bars)+f'</div><p class="time-total">전체 {total:g}초 · 막대 너비는 샷 길이에 비례합니다.</p>'
    rows=[]
    for i,step in enumerate(steps):
        rows.append(f'<li><span class="step-no">{i+1:02d}</span><strong>{inline(step["label"])}</strong><span>{inline(step.get("detail",""))}</span></li>')
    body+=f'<ol class="visual-steps">{"".join(rows)}</ol>'
    if kind=='relations':body+='<p class="relation-note">요청에 따라 필요한 분야를 함께 사용합니다.</p>'
    return f'<figure class="visual visual-{esc(kind)}"><figcaption>{inline(v.get("title",""))}</figcaption>{body}</figure>'

def shell(title, body, depth=1, kind='', description='Hermes의 작업·지식·카탈로그·이미지·영상 구조를 이해하고 공개 코드로 확인합니다.'):
    base='../'*depth
    navigation=''.join(link(base+href,label) for href,label in (
        ('system/index.html','전체 그림'),('scenarios/index.html','활용 장면'),
        ('components/index.html','구성 요소'),('blog/index.html','설계 이야기'),
        ('wiki/start.html','기술 명세'),('wiki/reference.html','시작하기')))
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(description)}"><meta name="color-scheme" content="light"><title>{esc(title)} · p-hermes</title><link rel="icon" href="{base}assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}assets/site.css"><script defer src="{base}assets/site.js"></script></head><body class="{kind}"><a class="skip" href="#main">본문으로 건너뛰기</a><header class="site-header"><a class="brand" href="{base}index.html"><span class="brand-mark">p<span>h</span></span>p-hermes<span class="version">v2</span></a><nav aria-label="주 메뉴">{navigation}</nav></header>{body}<footer class="site-footer"><a class="brand" href="{base}index.html">p-hermes</a><p>개념을 읽고, 구조를 따라가고, 코드로 확인합니다.</p><a href="{base}wiki/reference.html">구현과 출처</a><a href="{REPO}/blob/main/LICENSE">라이선스 ↗</a></footer></body></html>'''

def write(name,text):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8',newline='\n')

def lectures():
    slugs=['overview','tasks','knowledge','catalog','image','video']
    rows=[]
    for index,slug in enumerate(slugs):
        course=json.loads((ROOT/f'content/slides/courses/{slug}.json').read_text(encoding='utf-8'))
        total=course['teaching_minutes']+course['qa_minutes']
        terms=' · '.join(k['term'] for k in course['keywords'])
        rows.append(f'<a class="chapter-row" href="{slug}.html"><span class="chapter-number">{index:02}</span><div><h2>{esc(course["title"])}</h2><p>{esc(terms)}</p></div><span class="row-meta">{total}분<br>{len(course["slides"])}장 <b>↗</b></span></a>')
        definitions=''.join(f'<tr><th scope="row">{esc(k["term"])}</th><td>{esc(k["definition"])}</td></tr>' for k in course['keywords'])
        scenes=[];seen=set()
        for slide in course['slides']:
            if slide['scene']=='QA' or slide['scene'] in seen:continue
            seen.add(slide['scene'])
            minutes=sum(s['seconds'] for s in course['slides'] if s['scene']==slide['scene'])//60
            scenes.append(f'<a class="scene-row" href="../slides/{slug}/index.html#/{slide["id"]}"><span>{slide["scene"]}</span><strong>{esc(slide["title"]).replace(chr(10)," ")}</strong><span>{minutes}분 ↗</span></a>')
        blog_slug='start' if slug=='overview' else slug
        body=f'''<main id="main" class="course-index"><a href="index.html">← 전체 강의</a><div class="eyebrow lecture-kicker">LECTURE / {index:02}</div><h1>{esc(course['title'])}</h1><p class="lead">{course['teaching_minutes']}분의 설명과 적용, 10분의 질문.<br>관찰한 장면을 키워드로 이해하고 다음 판단에 적용합니다.</p><div class="hero-actions"><a class="primary-link" href="../slides/{slug}/index.html">슬라이드 시작 <span>→</span></a><a href="guide.html">발표 도구 안내 ↗</a></div><section class="lecture-outline"><h2>기억할 키워드</h2><table class="keyword-table">{definitions}</table></section><section class="lecture-outline"><h2>장면으로 바로 이동</h2>{''.join(scenes)}</section><div class="related"><a href="../blog/{blog_slug}.html">블로그로 다시 읽기</a><a href="../wiki/{blog_slug}.html">위키에서 구조 확인</a><a href="../wiki/reference.html">실행 예제 확인</a><a href="media.html">영상과 실행 기록 읽기</a></div></main>'''
        write(f'lectures/{slug}.html',shell(course['title']+' · 강의',body))
    body=f'''<main id="main" class="course-index"><div class="eyebrow">P-HERMES LECTURES</div><h1>큰 흐름 하나,<br>깊이 있는 다섯 강의</h1><p class="lead">큰 화면에서 차이를 발견하고, 핵심 개념으로 설명합니다.<br>전체 구조를 익힌 뒤 필요한 주제부터 깊게 들어가세요.</p><p class="scope-note">슬라이드의 단계 공개, 짧은 영상과 질문으로 진행합니다. 별도 발표자 창에서 설명과 답안, 진행 시간을 확인할 수 있습니다.</p><div class="hero-actions"><a class="primary-link" href="../slides/overview/index.html">전체 구조 강의 시작 <span>→</span></a><a href="guide.html">발표 도구 안내 ↗</a></div><div class="chapter-list">{''.join(rows)}</div><div class="related"><a href="../blog/index.html">읽기 자료는 블로그에서</a><a href="../wiki/start.html">개념과 구현은 위키에서</a></div><details class="archive-links"><summary>이전 시안 기록</summary><a href="prototype.html">첫 시안</a><a href="redesign/index.html">상호작용 시안</a><a href="course-preview/index.html">이전 읽기 시안</a></details></main>'''
    write('lectures/index.html',shell('강의',body))
    guide='''<main id="main" class="course-index"><a href="index.html">← 전체 강의</a><div class="eyebrow lecture-kicker">PRESENTER GUIDE</div><h1>발표의 흐름을<br>직접 조절합니다</h1><p class="lead">슬라이드를 연 뒤 전체화면으로 전환하세요.<br>키 입력 한 번으로 다음 근거를 공개하고, 질문에서는 잠시 멈춥니다.</p><table class="keyword-table"><tr><th>→ / Space</th><td>다음 공개 단계 또는 다음 슬라이드</td></tr><tr><th>←</th><td>이전 단계</td></tr><tr><th>S</th><td>발표자 노트 창 열기. 팝업 허용 필요</td></tr><tr><th>F</th><td>전체화면</td></tr><tr><th>V</th><td>현재 영상 재생·정지. 영상의 자체 제어도 사용 가능</td></tr><tr><th>Esc</th><td>슬라이드 전체 보기</td></tr><tr><th>H</th><td>키 안내</td></tr></table><section class="lecture-outline"><h2>청중에게는 핵심을, 발표자에게는 맥락을</h2><p>별도 창에 설명, 질문과 해설, 멈출 지점, 다음 장면 연결과 출처가 표시됩니다. 질문을 던진 뒤 답을 공개하기 전 15초 정도 관찰할 시간을 줍니다. 강의 시간은 참여와 실습을 포함한 계획값이며 현장 반응에 따라 조절합니다.</p><p>동작 줄이기 설정을 따르면 전환 이동을 생략합니다. 글자를 읽는 동안 불필요한 자동 동작을 반복하지 않습니다.</p></section><section class="lecture-outline"><h2>시연을 읽는 기준</h2><p>공개 코드는 독립적인 참고 구현입니다. 실제 실행 녹화는 합성 입력의 결과를 보여 줍니다. 램프 사진은 교육용 생성 자산이며, 12초 영상은 같은 사진을 별도 편집한 자료입니다. 공개 5초 시간선과 실제 2초 규격 검사 파일은 각각의 목적을 표시합니다.</p><p>네트워크가 불안정할 때에도 이미지와 영상은 같은 사이트의 자산을 사용합니다. 강의 중에는 핵심 슬라이드와 영상을 미리 열어 재생을 확인하세요.</p><p><a href="media.html">영상의 장면 설명과 실제 실행 기록을 텍스트로 읽기 →</a></p></section></main>'''
    write('lectures/guide.html',shell('발표 도구 안내',guide))
    transcripts=[]
    for key,title in [('cas','두 요청과 리비전'),('knowledge','검색과 기록의 퇴역'),('integration','파일과 DB 다시 열기'),('probe','실제 영상 규격 검사')]:
        receipt=json.loads((ROOT/f'content/slides/recording-{key}.json').read_text(encoding='utf-8'))
        steps=''.join(f'<h3>{i+1}. 실행과 반환값</h3><pre><code>{esc(step["command"])}</code></pre><pre><code>{esc(json.dumps(step["output"],ensure_ascii=False,indent=2))}</code></pre>' for i,step in enumerate(receipt['receipts']))
        transcripts.append(f'<section class="lecture-outline" id="{key}"><h2>{title}</h2><p>공개 함수에 합성 입력을 전달하고 반환 직후 녹화한 필드입니다. 아래 텍스트는 녹화의 실행 기록입니다.</p><img class="transcript-poster" src="../slides/assets/media/demo-{key}-poster.png" alt="{title} 녹화의 첫 화면">{steps}</section>')
    body='''<main id="main" class="course-index media-transcript"><a href="index.html">← 전체 강의</a><div class="eyebrow lecture-kicker">MEDIA READING</div><h1>영상에서 관찰한<br>차이를 다시 읽습니다</h1><p class="lead">모든 영상은 음성이 없는 교육 자료입니다.<br>화면의 문구와 실행 기록을 텍스트로 제공합니다.</p><div class="related"><a href="#editing">12초 편집 비교</a><a href="#cas">리비전</a><a href="#knowledge">지식</a><a href="#integration">통합 실행</a><a href="#probe">규격 검사</a></div><section class="lecture-outline" id="editing"><h2>같은 세 사진, 다른 시간 배분</h2><p>A는 전체 제품 4초, 갓 디테일 4초, 마무리 구도 4초입니다. B는 같은 사진을 같은 순서로 사용하며 2초, 6초, 4초로 길이만 바꿉니다. 둘 다 12초이며 움직이는 제품을 생성한 영상은 아닙니다.</p><p>A의 3.96초와 4.00초를 멈춰 보면 제품 전체에서 갓 디테일로 컷이 바뀝니다. 시선의 위치와 크기 변화를 관찰하고, 의도한 강조인지 확인합니다.</p><div class="boundary-reading"><figure><img src="../slides/assets/media/boundary-before.png" alt="3.96초: 왼쪽에 제품 전체가 보이는 샷"><figcaption>A · 3.96초</figcaption></figure><figure><img src="../slides/assets/media/boundary-after.png" alt="4.00초: 램프 갓을 확대한 디테일 샷"><figcaption>A · 4.00초</figcaption></figure></div><p>규격 검사에는 별도의 2초 색상 패턴 파일을 씁니다. 공개 데모가 만드는 5초 시간선 JSON은 인코딩한 영상 파일과 구분합니다.</p><a href="../slides/video/index.html#/V07-1">영상 강의에서 A/B 비교하기 ↗</a></section>'''+''.join(transcripts)+'''<div class="related"><a href="guide.html">발표 도구 안내</a><a href="../wiki/reference.html">공개 구현과 출처</a></div></main>'''
    write('lectures/media.html',shell('영상과 실행 기록',body))

def sources(items):
    if not items:return ''
    return '<section class="sources"><h2>근거와 더 읽을 자료</h2><ul>'+''.join('<li>'+link(x.get('url',x.get('href','')),x['label'])+'</li>' for x in items)+'</ul></section>'

def wiki(pages):
    for page in pages:
        nav=''.join(f'<a {"aria-current=page" if p["id"]==page["id"] else ""} href="{esc(p["id"])}.html">{inline(p["title"])}</a>' for p in pages)
        toc=''.join(f'<a href="#{esc(s["id"])}">{inline(s["title"])}</a>' for s in page['sections'])
        sections=[]
        for s in page['sections']:
            content=''.join(f'<p>{inline(t)}</p>' for t in s.get('paragraphs',[]))
            content+=visual(s.get('visual'))
            if s.get('table'):
                t=s['table']; content+='<div class="table-wrap" role="region" tabindex="0" aria-label="'+esc(s['title'])+' 표"><table><thead><tr>'+''.join('<th scope="col">'+inline(x)+'</th>' for x in t['headers'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+inline(x)+'</td>' for x in row)+'</tr>' for row in t['rows'])+'</tbody></table></div>'
            content+=codeblock(s.get('code'))
            if s.get('callout'):
                c=s['callout'];content+=f'<aside class="callout"><strong>{inline(c.get("title",""))}</strong><p>{inline(c.get("text",""))}</p></aside>'
            if s.get('links'):content+='<div class="related">'+''.join(link(x['href'],x['label']) for x in s['links'])+'</div>'
            sections.append(f'<section class="wiki-section" id="{esc(s["id"])}"><h2>{inline(s["title"])}</h2>{content}</section>')
        lecture_slug=page['id'] if page['id'] in {'tasks','knowledge','catalog','image','video'} else 'overview'
        course_link=f'<div class="related"><a href="../lectures/{lecture_slug}.html">이 주제의 강의 보기</a></div>'
        body=f'<div class="wiki-layout"><aside class="sidebar"><details open><summary>위키 탐색</summary><nav>{nav}</nav></details></aside><main id="main" class="wiki-main"><div class="eyebrow">SYSTEM HANDBOOK</div><h1>{inline(page["title"])}</h1><p class="lead">{inline(page["summary"])}</p>{course_link}<nav class="on-page" aria-label="이 페이지에서">{toc}</nav>{"".join(sections)}{sources(page.get("sources",[]))}</main></div>'
        write(f'wiki/{page["id"]}.html',shell(page['title'],body,description=page['summary']))

def blog(series):
    posts=series['posts']
    def publish(name,page):
        canonical=f'https://pheanor-agent.github.io/p-hermes-v2/blog/{name}'
        page=page.replace('</head>',f'<link rel="canonical" href="{canonical}"></head>')
        write(f'blog/{name}',page)
        # Keep old section hashes and readable no-JS content at previous addresses.
        alias=page.replace('<body ',f'<body data-blog-url="../blog/{name}" ',1)
        write(f'learn/{name}',alias)
    for ci,post in enumerate(posts):
        sections=[]
        for si,section in enumerate(post['sections']):
            paragraphs=''.join(f'<p>{inline(t)}</p>' for t in section.get('paragraphs',[]))
            checkpoints='<ul class="checkpoints">'+''.join('<li>'+inline(x)+'</li>' for x in section.get('checkpoints',[]))+'</ul>' if section.get('checkpoints') else ''
            related='<div class="related">'+''.join(link(x['href'],x['label']) for x in section.get('links',[]))+'</div>'
            sections.append(f'''<section class="lesson-slide" id="{esc(section['id'])}" aria-label="{esc(section['title'])}"><div class="slide-heading"><h2>{inline(section['title'])}</h2><p class="claim">{inline(section['claim'])}</p></div><div class="slide-evidence">{visual(section.get('visual'),post['id'])}{codeblock(section.get('code'))}</div><div class="reading-body">{paragraphs}{checkpoints}{related}<p class="transition">{inline(section.get('transition',''))}</p></div><details class="speaker-notes"><summary>덧붙이는 설명</summary><p>{inline(section.get('notes',''))}</p></details></section>''')
        nav=''.join(f'<a {"aria-current=page" if x["id"]==post["id"] else ""} href="../blog/{esc(x["id"])}.html">{i+1:02d} {inline(x["title"])}</a>' for i,x in enumerate(posts))
        contents=''.join(f'<a href="#{esc(x["id"])}">{inline(x["title"])}</a>' for x in post['sections'])
        if ci+1<len(posts):
            next_post=posts[ci+1]
            tail=f'<a class="next-chapter" href="../blog/{next_post["id"]}.html"><span>다음 글</span><strong>{inline(next_post["title"])} →</strong></a>'
        else:tail='<a class="next-chapter" href="../blog/index.html"><strong>전체 글 보기 →</strong></a>'
        lecture_slug=post['id'] if post['id'] in {'tasks','knowledge','catalog','image','video'} else 'overview'
        course_link=f'<div class="related"><a href="../lectures/{lecture_slug}.html">이 주제의 강의 보기</a></div>'
        body=f'''<div class="course-tools"><a href="../blog/index.html">← 블로그 전체 글</a><button id="print-page">인쇄</button></div><div class="course-layout"><aside class="sidebar"><details open><summary>연재 목록</summary><nav>{nav}</nav></details></aside><main id="main" class="course-main"><header class="chapter-intro"><span class="eyebrow">BLOG / {ci+1:02d}</span><h1>{inline(post['title'])}</h1><p class="lead">{inline(post['description'])}</p>{course_link}<nav class="on-page" aria-label="이 글에서">{contents}</nav></header>{"".join(sections)}{tail}</main></div>'''
        publish(f'{post["id"]}.html',shell(post['title']+' · 블로그',body,kind='blog',description=post['description']))
    rows=''.join(f'<a class="chapter-row" href="../blog/{esc(post["id"])}.html"><span class="chapter-number">{i+1:02d}</span><div><h2>{inline(post["title"])}</h2><p>{inline(post["description"])}</p></div><span class="row-meta">{len(post["sections"])}개 주제 <b>↗</b></span></a>' for i,post in enumerate(posts))
    body=f'<main id="main" class="course-index"><div class="eyebrow">P-HERMES BLOG</div><h1>시스템을 이해하는<br>일곱 편의 이야기</h1><p class="lead">한 요청을 따라 다섯 분야의 구조와 기술을 읽습니다.<br>도해와 코드 예제를 곁들인 연재입니다.</p><p class="scope-note">교육용 사례와 공개 코드의 동작을 사용합니다. 실제 Hermes의 구조는 위키에서 함께 확인하세요.</p><div class="chapter-list">{rows}</div>{sources(series.get("sources",[]))}</main>'
    publish('index.html',shell('블로그',body))

def system_index():
    # Public hubs own orientation and routes, not the detailed technical contracts.
    body='''<main id="main" class="course-index">
<header class="chapter-intro"><p class="eyebrow">하나의 요청, 이어지는 일</p><h1>전체 시스템 지도</h1><p class="lead">요청부터 실행, 검토와 재사용까지 p-hermes의 전체 흐름을 3분으로 이해합니다.</p></header>
<nav class="on-page" aria-label="이 페이지에서"><a href="#problem">해결하려는 문제</a><a href="#journey">요청의 흐름</a><a href="#cooperation">협력 지도</a><a href="#continuity">중단과 재개</a><a href="#next">더 깊게</a></nav>
<section id="problem" class="wiki-section"><h2>답변은 시작이고, 완료까지는 여러 단계입니다.</h2>
<p>좋은 답을 얻어도 자료 확인, 실제 제작, 검토와 전달은 남아 있습니다. 대화가 길어지거나 담당자가 바뀌면 어디까지 했는지, 무엇을 확인해야 하는지 다시 짚어야 합니다.</p><p>p-hermes는 이 사이를 연결하는 AI 작업 시스템입니다. 단순히 답변을 더 길게 쓰는 것이 아니라, 요청의 목표와 진행, 근거와 결과를 함께 다룹니다. 이 페이지는 약 3분 안에 그 전체 흐름을 살펴보는 지도입니다.</p>
</section>
<section id="journey" class="wiki-section"><h2>사람의 요청에서 다음 행동까지</h2>
<figure class="visual visual-flow"><figcaption>사람 / 외부 채널 → p-hermes → 완료 결과 / 다음 행동 / 재사용 지식</figcaption><ol class="visual-steps"><li><span class="step-no">01</span><strong>요청을 이해</strong><span>사람이나 외부 채널의 요청에서 목표와 완료 조건을 확인합니다.</span></li><li><span class="step-no">02</span><strong>진행을 관리</strong><span>해야 할 일과 지금 할 일을 구분하고 검토 지점을 정합니다.</span></li><li><span class="step-no">03</span><strong>지식·자원 탐색</strong><span>기존 자료의 근거와 필요한 도구·모델을 찾습니다.</span></li><li><span class="step-no">04</span><strong>실행·생성</strong><span>문서와 코드, 이미지와 영상 등 필요한 결과를 만듭니다.</span></li><li><span class="step-no">05</span><strong>검수·기록</strong><span>목표에 맞는지 살피고 결과와 판단 근거를 남깁니다.</span></li></ol></figure><p>새 요청이 오면 남겨 둔 기록을 다시 확인합니다. 앞선 결과를 그대로 반복하는 대신, 유효한 근거와 필요한 작업을 골라 이어갑니다.</p>
</section>
<section id="cooperation" class="wiki-section"><h2>다섯 능력이 같은 작업 안에서 협력합니다.</h2>
<ul class="checkpoints"><li><strong>진행</strong>은 지금 필요한 행동을 정리하고 지식과 자원 탐색으로 연결합니다.</li><li><strong>지식</strong>은 왜 그렇게 판단하는지 설명할 자료와 출처를 제공합니다.</li><li><strong>자원</strong>은 그 일을 수행할 도구, 모델과 템플릿 선택을 돕습니다.</li><li><strong>생성</strong>은 그 선택을 실제 이미지와 영상 같은 산출물로 바꿉니다.</li><li><strong>통합</strong>은 산출물끼리 맥락이 맞는지 살피고 진행 기록으로 돌려보냅니다.</li></ul><p>문서·코드 실행과 미디어 생성은 같은 목표에서 갈라졌다가 검토에서 다시 만납니다. 따라서 여러 기능이 있어도 방문자가 따라갈 중심은 하나의 요청입니다.</p><div class="related"><a href="../components/index.html">공개 이름과 내부 구성 요소 연결하기 →</a></div>
</section>
<section id="continuity" class="wiki-section"><h2>멈추더라도, 확인하고 이어갑니다.</h2>
<ul class="checkpoints"><li><strong>중단:</strong> 완료하지 못한 단계와 확인할 사항을 남깁니다.</li><li><strong>재개:</strong> 이전 기록과 실제 결과를 확인한 뒤 다음 행동을 정합니다.</li><li><strong>검토:</strong> 중요한 변경은 사람이 판단할 지점을 마련합니다.</li><li><strong>재사용:</strong> 결과뿐 아니라 선택 이유와 출처도 다음 작업에 연결합니다.</li></ul><p>모든 일을 무조건 자동으로 끝낸다는 뜻은 아닙니다. 확인이 필요한 순간을 드러내고, 그 판단 이후의 일을 이어가려는 구조입니다.</p>
</section>
<section id="next" class="wiki-section"><h2>이제 요청 하나를 따라가 보세요.</h2>
<div class="related"><a href="../scenarios/index.html#project-package">프로젝트 소개 패키지 만들기</a><a href="../lectures/overview.html">쉽게 이해하기 · 강의</a><a href="../blog/start.html">설계 이유 · 블로그</a><a href="../wiki/start.html">정확한 명세 · 위키</a></div>
</section>

</main>'''
    write('system/index.html',shell('전체 시스템 지도',body,description='요청부터 실행, 검토와 재사용까지 p-hermes의 전체 흐름을 3분으로 이해합니다.'))

def scenarios_index():
    body='''<main id="main" class="course-index">
<header class="chapter-intro"><p class="eyebrow">하나의 요청, 이어지는 일</p><h1>활용 장면</h1><p class="lead">프로젝트 소개 패키지라는 하나의 요청에서 다섯 능력이 협력하는 과정을 따라갑니다.</p></header>
<nav class="on-page" aria-label="이 페이지에서"><a href="#project-package">대표 시나리오</a><a href="#journey">작업 여정</a><a href="#review">검토와 전달</a><a href="#reuse">다음 작업</a></nav>
<section id="project-package" class="wiki-section"><h2>프로젝트 소개 패키지 만들기</h2>
<p>“프로젝트를 외부에 소개할 문서·이미지·짧은 영상을 준비해줘.”</p><p>이것은 시스템의 협력을 보여주는 설명용 시나리오입니다. 실제 생성 결과나 실행 완료를 주장하는 사례가 아닙니다. 조사와 문서화, 프로젝트 실행, 콘텐츠 제작이 한 요청 안에서 만나는 과정을 따라갑니다.</p><p>먼저 누구에게 소개할지, 무엇을 전달할지, 어떤 결과가 있으면 완료로 볼지 확인합니다. 문서 한 장, 대표 이미지, 짧은 소개 영상이 필요한지부터 사람과 맞춥니다.</p>
</section>
<section id="journey" class="wiki-section"><h2>한 요청이 각 능력을 거치는 과정</h2>
<figure class="visual visual-flow"><figcaption>요청 → 진행 → 근거 → 자원</figcaption><ol class="visual-steps"><li><span class="step-no">01</span><strong>목표와 완료 조건</strong><span>진행 관리 · Tasks: 요청을 작업으로 정리하고 현재 단계와 다음 검토를 남깁니다.</span></li><li><span class="step-no">02</span><strong>기존 근거 찾기</strong><span>지식 · Knowledge: 프로젝트 문서, 기존 결정, 참고자료를 찾아 설명의 바탕을 모읍니다.</span></li><li><span class="step-no">03</span><strong>필요한 자원 선택</strong><span>자원 · Catalog: 목적에 맞는 도구, 모델, 템플릿과 리퍼런스를 고릅니다.</span></li></ol></figure><div class="visual visual-comparison"><ul class="visual-steps"><li><h3>문서·코드 작업</h3><p>핵심 소개 문구와 문서를 구성하고, 필요하다면 소개 페이지용 코드도 준비합니다.</p></li><li><h3>이미지·영상 생성</h3><p>Image / Video가 같은 자료와 방향을 바탕으로 대표 이미지와 짧은 영상을 만듭니다.</p></li></ul></div><p>두 작업의 형식은 다르지만 대상 독자와 핵심 메시지는 같습니다. 결과가 모이면 하나의 패키지로 검토합니다.</p>
</section>
<section id="review" class="wiki-section"><h2>만들었다고 곧바로 완료하지 않습니다.</h2>
<p><strong>통합 · Integration</strong>은 문서의 주장, 이미지의 표현, 영상의 설명이 서로 맞는지 살피는 연결 지점입니다. 같은 프로젝트를 다르게 소개하고 있지 않은지, 빠진 자료는 없는지 확인합니다.</p><p>검토할 사람에게 결과와 확인 사항을 함께 제시합니다. 수정이 필요하면 해당 작업으로 돌아가고, 목표에 맞는지 검토·승인한 뒤 전달합니다. 생성 자체와 승인된 완료를 구분하는 이유입니다.</p>
</section>
<section id="reuse" class="wiki-section"><h2>완료 결과와 근거를 다음 작업에 남깁니다.</h2>
<p><strong>Tasks + Knowledge</strong>에 완료 상태, 결과를 찾을 위치, 검토에서 결정한 내용과 재사용할 근거를 연결합니다. 다음에 “다른 독자에게 맞춰 소개해줘”라는 요청이 오면, 무엇을 유지하고 바꿀지 이 기록부터 확인합니다.</p><p>진행 관리만으로는 자료를 만들 수 없고, 생성만으로는 완료 여부를 설명하기 어렵습니다. 다섯 능력이 한 시스템에 있는 이유는 요청부터 다음 작업까지 이 연결을 유지하기 위해서입니다.</p><div class="related"><a href="../components/tasks.html">진행을 이어가는 역할 보기</a><a href="../components/index.html">구성 요소 전체 보기</a><a href="../blog/integration.html">왜 결과를 함께 검토하는가</a><a href="../system/index.html">전체 지도 다시 보기</a></div>
</section>

</main>'''
    write('scenarios/index.html',shell('활용 장면',body,description='프로젝트 소개 패키지라는 하나의 요청에서 다섯 능력이 협력하는 과정을 따라갑니다.'))

def components_index():
    body='''<main id="main" class="course-index">
<header class="chapter-intro"><p class="eyebrow">하나의 요청, 이어지는 일</p><h1>구성 요소 지도</h1><p class="lead">진행·지식·자원·생성·통합, 하나의 요청을 이어가는 다섯 공개 그룹을 살펴봅니다.</p></header>
<nav class="on-page" aria-label="공개 그룹"><a href="#progress">진행</a><a href="#knowledge">지식</a><a href="#resources">자원</a><a href="#generation">생성</a><a href="#integration">통합</a></nav>
<p>공개 지도에서는 다섯 그룹으로 읽습니다. 내부 구성 요소를 합치거나 이름을 바꾼 것이 아니라, 전체 흐름에서 맡는 역할로 묶었습니다.</p>
<section id="progress" class="wiki-section"><h2>진행</h2>
<h3>진행을 이어가기</h3><small>Tasks</small><p>작업의 현재 상태와 다음 행동을 관리합니다.</p><div class="related"><a href="tasks.html">역할과 보장 · Tasks 허브</a><a href="../lectures/tasks.html">쉽게 이해하기 · 강의</a><a href="../blog/tasks.html">설계 이유 · 블로그</a><a href="../wiki/tasks.html">정확한 명세 · 위키</a></div>
</section>
<section id="knowledge" class="wiki-section"><h2>지식</h2>
<h3>근거를 기억하기</h3><small>Knowledge</small><p>자료와 출처, 판단 근거를 찾고 다시 씁니다.</p><div class="related"><a href="../lectures/knowledge.html">쉽게 이해하기 · 강의</a><a href="../blog/knowledge.html">설계 이유 · 블로그</a><a href="../wiki/knowledge.html">정확한 명세 · 위키</a></div>
</section>
<section id="resources" class="wiki-section"><h2>자원</h2>
<h3>필요한 자원을 고르기</h3><small>Catalog</small><p>도구와 모델, 템플릿과 리퍼런스를 고릅니다.</p><div class="related"><a href="../lectures/catalog.html">쉽게 이해하기 · 강의</a><a href="../blog/catalog.html">설계 이유 · 블로그</a><a href="../wiki/catalog.html">정확한 명세 · 위키</a></div>
</section>
<section id="generation" class="wiki-section"><h2>생성</h2>
<p>결과물을 만들기 — Image와 Video를 하나의 생성 그룹에서 봅니다. 문서·코드 등 다른 실행 결과와 함께 같은 요청의 산출물로 연결됩니다.</p><h3>결과물을 만들기 · 이미지</h3><small>Image</small><p>선택한 자원으로 이미지 산출물을 만듭니다.</p><div class="related"><a href="../lectures/image.html">쉽게 이해하기 · 강의</a><a href="../blog/image.html">설계 이유 · 블로그</a><a href="../wiki/image.html">정확한 명세 · 위키</a></div><h3>결과물을 만들기 · 영상</h3><small>Video</small><p>선택한 자원으로 영상 산출물을 만듭니다.</p><div class="related"><a href="../lectures/video.html">쉽게 이해하기 · 강의</a><a href="../blog/video.html">설계 이유 · 블로그</a><a href="../wiki/video.html">정확한 명세 · 위키</a></div>
</section>
<section id="integration" class="wiki-section"><h2>통합</h2>
<h3>결과를 연결하고 검수하기</h3><small>Integration</small><p>여러 산출물의 맥락을 맞추고 검토를 연결합니다.</p><div class="related"><a href="../blog/integration.html">설계 이유 · 블로그</a><a href="../wiki/integration.html">정확한 명세 · 위키</a></div><p>통합 전용 강의 페이지 대신 기존 설계 이야기와 기술 명세로 연결합니다.</p>
</section>
<div class="related"><a href="../scenarios/index.html#project-package">이 구성 요소가 협력하는 시나리오 →</a></div>
</main>'''
    write('components/index.html',shell('구성 요소 지도',body,description='진행·지식·자원·생성·통합, 하나의 요청을 이어가는 다섯 공개 그룹을 살펴봅니다.'))

def component_tasks():
    body='''<main id="main" class="course-index">
<header class="chapter-intro"><p class="eyebrow">하나의 요청, 이어지는 일</p><h1>진행을 이어가기</h1><p class="lead">현재 상태와 다음 행동의 근거를 남겨, 복잡한 요청을 중단 이후에도 확인하고 이어갑니다.</p></header>
<p class="hero-note">Tasks · 시스템이 “지금 어디까지 왔는지” 잊지 않는 방법</p><nav class="on-page" aria-label="이 페이지에서"><a href="#role">왜 필요한가</a><a href="#position">시스템에서의 위치</a><a href="#guarantees">다섯 가지 보장 목표</a><a href="#depth">더 깊게</a></nav>
<section id="role" class="wiki-section"><h2>왜 진행 관리가 필요한가</h2>
<p>조사하고 계획한 뒤 검토를 기다리거나, 실행 중 예상하지 못한 결과를 만나면 다음 행동이 달라집니다. 대화 내용만으로는 지금 어디까지 왔는지 다시 확인하기 어렵습니다.</p><p>Tasks는 현재 진행과 다음 행동의 근거를 보존하는 영역입니다. 결과를 직접 만드는 모든 기능을 대신하지 않고, 각 기능의 일을 같은 요청의 진행으로 연결합니다.</p>
</section>
<section id="position" class="wiki-section"><h2>실행 앞뒤에서 진행을 연결합니다.</h2>
<figure class="visual visual-flow"><figcaption>요청 → 진행 관리 → 근거·자원 → 실행 → 진행 기록</figcaption><ol class="visual-steps"><li><span class="step-no">01</span><strong>요청 → 진행 관리</strong><span>목표와 현재 단계를 정리하고 필요한 확인을 드러냅니다.</span></li><li><span class="step-no">02</span><strong>근거·자원 요청</strong><span>Knowledge에서 자료를, Catalog에서 도구와 자원을 찾습니다.</span></li><li><span class="step-no">03</span><strong>실행 / 생성</strong><span>선택한 근거와 자원으로 실제 결과를 준비합니다.</span></li><li><span class="step-no">04</span><strong>다시 진행 관리</strong><span>결과와 검수 내용을 확인하고 다음 단계 또는 완료를 기록합니다.</span></li></ol></figure><div class="related"><a href="index.html#knowledge">근거를 기억하기</a><a href="index.html#resources">필요한 자원을 고르기</a><a href="../scenarios/index.html#project-package">대표 시나리오에서 위치 보기</a></div>
</section>
<section id="guarantees" class="wiki-section"><h2>무엇을 보장하려는가</h2>
<p>진행 관리가 지키려는 다섯 가지 목표입니다. 적용 범위와 정확한 동작 조건은 기술 명세에서 확인합니다.</p><ol class="checkpoints"><li><strong>현재 상태를 알 수 있다.</strong> 진행 중인 일과 남은 일을 구분합니다.</li><li><strong>다음 행동의 근거를 알 수 있다.</strong> 왜 그 일을 하는지 기록과 연결합니다.</li><li><strong>중요한 전환에 검토를 요구할 수 있다.</strong> 사람이 판단할 지점을 둡니다.</li><li><strong>중단된 작업을 확인 후 재개할 수 있다.</strong> 실제 결과를 확인하고 이어갈 일을 정합니다.</li><li><strong>여러 실행이 서로 덮어쓰는 것을 막는다.</strong> 앞선 진행을 잃지 않도록 변경을 다룹니다.</li></ol>
</section>
<section id="depth" class="wiki-section"><h2>원하는 깊이로 선택하세요.</h2>
<div class="visual visual-comparison"><ul class="visual-steps"><li><h3>쉽게 이해하기</h3><p>그림과 사례로 진행 관리의 역할을 봅니다.</p><div class="related"><a href="../lectures/tasks.html">Tasks 강의 →</a></div></li><li><h3>왜 이렇게 만들었나</h3><p>진행을 지키는 설계 선택의 이유를 읽습니다.</p><div class="related"><a href="../blog/tasks.html">Tasks 블로그 →</a></div></li><li><h3>정확한 명세</h3><p>정의와 동작 조건, 구현 근거를 확인합니다.</p><div class="related"><a href="../wiki/tasks.html">Tasks 위키 →</a></div></li></ul></div>
</section>

</main>'''
    write('components/tasks.html',shell('진행을 이어가기',body,description='현재 상태와 다음 행동의 근거를 남겨, 복잡한 요청을 중단 이후에도 확인하고 이어갑니다.'))

def home():
    body='''<main id="main" class="course-index">
<section class="chapter-intro"><p class="eyebrow">하나의 요청, 이어지는 일</p><h1>AI가 답하고 끝나지 않도록.</h1><p class="lead">p-hermes는 작업의 상태, 지식, 자원, 생성 결과와 검토 근거를 연결해 복잡한 일을 여러 단계에 걸쳐 이어가는 AI 작업 시스템입니다.</p><div class="hero-actions"><a class="primary-link" href="system/index.html">전체 그림 보기 <span>→</span></a><a href="scenarios/index.html#project-package">실제 작업 흐름 보기 →</a></div><p class="hero-note">아래 활용 장면은 시스템의 협력을 설명하는 시나리오이며, 실제 실행 완료를 주장하는 사례가 아닙니다.</p></section>
<nav class="on-page" aria-label="이 페이지에서"><a href="#system">한 요청의 흐름</a><a href="#scenarios">활용 장면</a><a href="#components">다섯 능력</a><a href="#depth">깊이 선택</a></nav>
<section id="system" class="wiki-section"><h2>한 요청이 들어오면</h2><figure class="visual visual-flow"><figcaption>요청 → 진행관리 → 지식·자원 → 실행·생성 → 검수·기록 → 이어짐</figcaption><ol class="visual-steps">
<li><span class="step-no">01</span><strong>요청</strong><span>목표와 완료 조건을 확인합니다.</span></li>
<li><span class="step-no">02</span><strong>진행관리</strong><span>현재 상태와 다음 행동, 검토할 지점을 정합니다.</span></li>
<li><span class="step-no">03</span><strong>지식·자원</strong><span>판단의 근거와 필요한 도구·모델을 찾습니다.</span></li>
<li><span class="step-no">04</span><strong>실행·생성</strong><span>문서와 코드, 이미지와 영상으로 결과를 만듭니다.</span></li>
<li><span class="step-no">05</span><strong>검수·기록</strong><span>목표에 맞는지 살피고 결과와 판단 근거를 남깁니다.</span></li>
</ol></figure><p><strong>다음 작업으로 이어짐 →</strong> 중단된 작업도 실제 결과와 기록을 확인한 뒤 재개하고, 남긴 근거를 다음 요청에 다시 씁니다.</p><div class="related"><a href="system/index.html">전체 시스템 지도 보기 →</a></div></section>
<section id="components" class="wiki-section"><h2>하나의 시스템을 이루는 능력</h2><p>진행·지식·자원·생성·통합이 같은 요청 안에서 협력합니다. 이미지와 영상은 하나의 생성 그룹으로 읽습니다.</p><ul class="visual-steps">
<li><h3><a href="components/tasks.html">진행을 이어가기</a></h3><small>Tasks</small><p>작업의 현재 상태와 다음 행동을 잃지 않도록 관리합니다.</p><a href="wiki/tasks.html">기술 명세 →</a></li>
<li><h3><a href="components/index.html#knowledge">근거를 기억하기</a></h3><small>Knowledge</small><p>자료와 출처, 판단 근거를 찾고 다시 씁니다.</p><a href="wiki/knowledge.html">기술 명세 →</a></li>
<li><h3><a href="components/index.html#resources">필요한 자원을 고르기</a></h3><small>Catalog</small><p>도구와 모델, 템플릿과 리퍼런스를 고릅니다.</p><a href="wiki/catalog.html">기술 명세 →</a></li>
<li><h3><a href="components/index.html#generation">결과물을 만들기</a></h3><small>Image / Video</small><p>같은 목표와 자료를 바탕으로 이미지와 영상 산출물을 만듭니다.</p><div class="related"><a href="wiki/image.html">이미지 명세 →</a><a href="wiki/video.html">영상 명세 →</a></div></li>
<li><h3><a href="components/index.html#integration">결과를 연결하고 검수하기</a></h3><small>Integration</small><p>여러 산출물의 맥락을 맞추고 검토 결과를 진행 기록으로 연결합니다.</p><a href="wiki/integration.html">기술 명세 →</a></li>
</ul></section>
<section id="scenarios" class="wiki-section"><h2>활용 장면</h2><p>프로젝트 소개 패키지 만들기라는 하나의 설명용 시나리오에서 세 가지 장면을 따라갑니다.</p><ul class="visual-steps">
<li><h3>조사·문서화</h3><p>프로젝트 자료와 출처를 확인하고, 소개 문서의 주장과 근거를 정리합니다.</p><a href="scenarios/index.html#journey">근거에서 문서로 →</a></li>
<li><h3>프로젝트 실행</h3><p>완료 조건과 현재 단계를 정하고, 필요한 실행과 검토·승인을 거쳐 전달합니다.</p><a href="scenarios/index.html#review">실행에서 검토로 →</a></li>
<li><h3>콘텐츠 제작</h3><p>제품의 특징과 핵심 메시지에 맞춰 이미지와 짧은 영상을 하나의 패키지로 준비합니다.</p><a href="scenarios/index.html#project-package">소개 패키지 흐름 보기 →</a></li>
</ul></section>
<section id="depth" class="wiki-section"><h2>얼마나 깊게 볼까요?</h2><ul class="visual-steps">
<li><h3>처음 보는 사람</h3><p>큰 흐름을 먼저 보고, 강의에서 차이를 발견하고 개념을 적용합니다.</p><div class="related"><a href="system/index.html">전체 그림 →</a><a href="lectures/index.html">강의 →</a></div></li>
<li><h3>설계 이유가 궁금한 사람</h3><p>한 요청을 따라 구조와 선택의 이유를 읽습니다.</p><a href="blog/index.html">설계 이야기 · 블로그 →</a></li>
<li><h3>정확한 구현이 필요한 사람</h3><p>기술 명세와 실행 가능한 공개 코드의 입출력 계약을 확인합니다.</p><a href="wiki/start.html">기술 명세 · 위키 →</a></li>
<li><h3>순서대로 보고 싶은 사람</h3><p>기존 읽기 경로에서 전체 구조부터 통합 실행까지 차례로 살펴봅니다.</p><a href="learn/index.html">순서대로 배우기 · Guided Path →</a></li>
</ul></section>
</main>'''
    write('index.html',shell('여러 단계의 일을 이어가는 AI 작업 시스템',body,depth=0,kind='home',description='작업의 상태, 지식, 자원, 생성 결과와 검토 근거를 연결해 복잡한 일을 이어가는 p-hermes.'))

def main():
    (OUT/'assets').mkdir(parents=True,exist_ok=True)
    for filename in ('site.css','site.js','mark.svg'):
        shutil.copyfile(ROOT/'site'/filename,OUT/'assets'/filename)
    shutil.copyfile(ROOT/'site/slides/media/luma-left.png',OUT/'assets/luma-left.png')
    wp=ROOT/'content/wiki/pages.json';cp=ROOT/'content/blog/series.json'
    if wp.exists():wiki(json.loads(wp.read_text(encoding='utf-8-sig'))['pages'])
    if cp.exists():blog(json.loads(cp.read_text(encoding='utf-8-sig')))
    home()
    system_index()
    scenarios_index()
    components_index()
    component_tasks()
    write('.nojekyll','')
    lectures()
    print('Built public website in docs/')

if __name__=='__main__':main()
