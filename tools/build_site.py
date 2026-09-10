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
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(description)}"><meta name="color-scheme" content="light"><title>{esc(title)} · p-hermes</title><link rel="icon" href="{base}assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}assets/site.css"><script defer src="{base}assets/site.js"></script></head><body class="{kind}"><a class="skip" href="#main">본문으로 건너뛰기</a><header class="site-header"><a class="brand" href="{base}index.html"><span class="brand-mark">p<span>h</span></span>p-hermes<span class="version">v2</span></a><nav aria-label="주 메뉴"><a href="{base}lectures/index.html">강의</a><a href="{base}wiki/start.html">위키</a><a href="{base}blog/index.html">블로그</a><a href="{base}wiki/reference.html">코드 시작하기</a><a class="github-link" href="{REPO}">GitHub ↗</a></nav></header>{body}<footer class="site-footer"><a class="brand" href="{base}index.html">p-hermes</a><p>개념을 읽고, 구조를 따라가고, 코드로 확인합니다.</p><a href="{base}wiki/reference.html">구현과 출처</a><a href="{REPO}/blob/main/LICENSE">라이선스 ↗</a></footer></body></html>'''

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

def home():
    rows=''.join(f'<a class="domain-row" href="wiki/{key}.html"><span class="domain-num">{i+1:02d}</span><h3>{title}</h3><span>{desc}</span><b>↗</b></a>' for i,(key,title,desc) in enumerate(DOMAINS))
    system=''.join(f'<a href="wiki/{key}.html" class="map-node node-{i}"><span>0{i+1}</span><strong>{title}</strong><small>{desc}</small></a>' for i,(key,title,desc) in enumerate(DOMAINS))
    body=f'''<main id="main"><section class="home-hero"><div><div class="eyebrow">AN OPEN GUIDE TO AGENT SYSTEMS</div><h1>에이전트가 일을<br><span>이어가는 구조</span></h1><p class="lead">에이전트가 일을 이어가는 구조를 탐구합니다.<br>작업·지식·카탈로그·이미지·영상을<br>하나의 연결된 시스템으로 읽어 보세요.</p><div class="hero-actions"><a class="primary-link" href="lectures/index.html">강의에서 시작하기 <span>→</span></a><a href="wiki/start.html">위키에서 살펴보기 ↗</a></div><p class="hero-note">Hermes 시스템 해설과 독립적으로 실행하는 공개 도구</p></div><div class="system-map"><div class="map-caption">FIVE DOMAINS / ONE SYSTEM</div><svg viewBox="0 0 560 430" aria-hidden="true"><path d="M115 135H440M280 135V275M115 275H440M115 135V275M440 135V275" fill="none" stroke="#aebdea" stroke-width="2" stroke-dasharray="5 7"/><circle cx="280" cy="205" r="28" fill="#3455ed"/><path d="M269 205H291M284 198L291 205L284 212" stroke="white" fill="none" stroke-width="2"/></svg>{system}<div class="map-foot">목표 · 근거 · 선택 · 산출물</div></div></section><section class="home-path"><div><span class="eyebrow">CHOOSE YOUR PATH</span><h2>어디서 시작할까요?</h2></div><a href="lectures/index.html"><span class="path-icon">01</span><h3>큰 화면에서 함께 배우기</h3><p>전체 구조와 다섯 주제의 강의에서<br>차이를 발견하고 개념을 적용합니다.</p><span>강의 보기 →</span></a><a href="wiki/reference.html"><span class="path-icon">02</span><h3>직접 확인하며 만들기</h3><p>실행 가능한 공개 코드와<br>입출력 계약을 살펴봅니다.</p><span>코드 시작하기 →</span></a></section><section class="home-domains"><div><span class="eyebrow">EXPLORE THE SYSTEM</span><h2>다섯 분야,<br>서로 다른 책임</h2><p>각 분야를 개념, 구조, 동작,<br>기술과 검증으로 나누어 설명합니다.</p></div><div>{rows}</div></section><section class="home-case"><div><span class="eyebrow">A SHARED EXAMPLE</span><h2>짧은 요청 하나에<br>어떤 판단이 담길까요?</h2><p>책상용 램프의 소개 자료를 만든다고 생각해 보세요. 제품의 특징을 확인하고, 구성을 선택하고, 장면을 연결하는 동안 시스템의 역할이 드러납니다.</p><a href="blog/start.html">LUMA 사례 따라가기 ↗</a></div><figure>{lamp(0)}<figcaption>교육용 생성 이미지 · 제품과 문구 공간의 배치</figcaption></figure></section></main>'''
    write('index.html',shell('에이전트 시스템의 구조와 기술',body,depth=0,kind='home'))

def main():
    (OUT/'assets').mkdir(parents=True,exist_ok=True)
    for filename in ('site.css','site.js','mark.svg'):
        shutil.copyfile(ROOT/'site'/filename,OUT/'assets'/filename)
    shutil.copyfile(ROOT/'site/slides/media/luma-left.png',OUT/'assets/luma-left.png')
    wp=ROOT/'content/wiki/pages.json';cp=ROOT/'content/blog/series.json'
    if wp.exists():wiki(json.loads(wp.read_text(encoding='utf-8-sig'))['pages'])
    if cp.exists():blog(json.loads(cp.read_text(encoding='utf-8-sig')))
    home()
    write('.nojekyll','')
    lectures()
    print('Built public website in docs/')

if __name__=='__main__':main()
