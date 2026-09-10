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

def lamp():
    return '''<svg class="lamp" viewBox="0 0 640 390" role="img" aria-label="교육용 램프 구성. 왼쪽은 램프의 위치, 오른쪽은 소개 문구를 위한 공간입니다."><defs><linearGradient id="light" x2="0" y2="1"><stop stop-color="#d1ef70" stop-opacity=".45"/><stop offset="1" stop-color="#d1ef70" stop-opacity="0"/></linearGradient></defs><path d="M0 330H640" stroke="#a6b3cd"/><g transform="translate(-240 0)"><path d="M385 129L295 327H600L463 129Z" fill="url(#light)"/><ellipse cx="449" cy="325" rx="83" ry="15" fill="#152440"/><path d="M449 315V168L420 136" fill="none" stroke="#254968" stroke-width="12"/><path d="M367 120Q416 73 470 120L470 140H367Z" fill="#286675"/><ellipse cx="419" cy="139" rx="52" ry="10" fill="#d9f597"/></g><g transform="translate(290 0)"><path d="M73 118H245M73 143H207M73 169H227" stroke="#476082" stroke-width="7"/><path d="M60 89H262V230H60Z" fill="none" stroke="#587fc3" stroke-dasharray="5 5"/><text x="60" y="66">文구를 위한 여백</text></g><text x="125" y="368">동일한 색과 형태</text><path d="M310 77V235M299 77H321M299 235H321" stroke="#a6b3cd"/></svg>'''.replace('文구','문구')

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
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(description)}"><meta name="color-scheme" content="light"><title>{esc(title)} · p-hermes</title><link rel="icon" href="{base}assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}assets/site.css"><script defer src="{base}assets/site.js"></script></head><body class="{kind}"><a class="skip" href="#main">본문으로 건너뛰기</a><header class="site-header"><a class="brand" href="{base}index.html"><span class="brand-mark">p<span>h</span></span>p-hermes<span class="version">v2</span></a><nav aria-label="주 메뉴"><a href="{base}wiki/start.html">위키</a><a href="{base}blog/index.html">블로그</a><a href="{base}wiki/reference.html">코드 시작하기</a><a class="github-link" href="{REPO}">GitHub ↗</a></nav></header>{body}<footer class="site-footer"><a class="brand" href="{base}index.html">p-hermes</a><p>개념을 읽고, 구조를 따라가고, 코드로 확인합니다.</p><a href="{base}wiki/reference.html">구현과 출처</a><a href="{REPO}/blob/main/LICENSE">라이선스 ↗</a></footer></body></html>'''

def write(name,text):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8',newline='\n')

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
        body=f'<div class="wiki-layout"><aside class="sidebar"><details open><summary>위키 탐색</summary><nav>{nav}</nav></details></aside><main id="main" class="wiki-main"><div class="eyebrow">SYSTEM HANDBOOK</div><h1>{inline(page["title"])}</h1><p class="lead">{inline(page["summary"])}</p><nav class="on-page" aria-label="이 페이지에서">{toc}</nav>{"".join(sections)}{sources(page.get("sources",[]))}</main></div>'
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
        body=f'''<div class="course-tools"><a href="../blog/index.html">← 블로그 전체 글</a><button id="print-page">인쇄</button></div><div class="course-layout"><aside class="sidebar"><details open><summary>연재 목록</summary><nav>{nav}</nav></details></aside><main id="main" class="course-main"><header class="chapter-intro"><span class="eyebrow">BLOG / {ci+1:02d}</span><h1>{inline(post['title'])}</h1><p class="lead">{inline(post['description'])}</p><nav class="on-page" aria-label="이 글에서">{contents}</nav></header>{"".join(sections)}{tail}</main></div>'''
        publish(f'{post["id"]}.html',shell(post['title']+' · 블로그',body,kind='blog',description=post['description']))
    rows=''.join(f'<a class="chapter-row" href="../blog/{esc(post["id"])}.html"><span class="chapter-number">{i+1:02d}</span><div><h2>{inline(post["title"])}</h2><p>{inline(post["description"])}</p></div><span class="row-meta">{len(post["sections"])}개 주제 <b>↗</b></span></a>' for i,post in enumerate(posts))
    body=f'<main id="main" class="course-index"><div class="eyebrow">P-HERMES BLOG</div><h1>시스템을 이해하는<br>일곱 편의 이야기</h1><p class="lead">한 요청을 따라 다섯 분야의 구조와 기술을 읽습니다.<br>도해와 코드 예제를 곁들인 연재입니다.</p><p class="scope-note">교육용 사례와 공개 코드의 동작을 사용합니다. 실제 Hermes의 구조는 위키에서 함께 확인하세요.</p><div class="chapter-list">{rows}</div>{sources(series.get("sources",[]))}</main>'
    publish('index.html',shell('블로그',body))

def home():
    rows=''.join(f'<a class="domain-row" href="wiki/{key}.html"><span class="domain-num">{i+1:02d}</span><h3>{title}</h3><span>{desc}</span><b>↗</b></a>' for i,(key,title,desc) in enumerate(DOMAINS))
    system=''.join(f'<a href="wiki/{key}.html" class="map-node node-{i}"><span>0{i+1}</span><strong>{title}</strong><small>{desc}</small></a>' for i,(key,title,desc) in enumerate(DOMAINS))
    body=f'''<main id="main"><section class="home-hero"><div><div class="eyebrow">AN OPEN GUIDE TO AGENT SYSTEMS</div><h1>에이전트가 일을<br><span>이어가는 구조</span></h1><p class="lead">에이전트가 일을 이어가는 구조를 탐구합니다.<br>작업·지식·카탈로그·이미지·영상을<br>하나의 연결된 시스템으로 읽어 보세요.</p><div class="hero-actions"><a class="primary-link" href="blog/start.html">첫 글 읽기 <span>→</span></a><a href="wiki/start.html">위키에서 살펴보기 ↗</a></div><p class="hero-note">Hermes 시스템 해설과 독립적으로 실행하는 공개 도구</p></div><div class="system-map"><div class="map-caption">FIVE DOMAINS / ONE SYSTEM</div><svg viewBox="0 0 560 430" aria-hidden="true"><path d="M115 135H440M280 135V275M115 275H440M115 135V275M440 135V275" fill="none" stroke="#aebdea" stroke-width="2" stroke-dasharray="5 7"/><circle cx="280" cy="205" r="28" fill="#3455ed"/><path d="M269 205H291M284 198L291 205L284 212" stroke="white" fill="none" stroke-width="2"/></svg>{system}<div class="map-foot">목표 · 근거 · 선택 · 산출물</div></div></section><section class="home-path"><div><span class="eyebrow">CHOOSE YOUR PATH</span><h2>어디서 시작할까요?</h2></div><a href="blog/index.html"><span class="path-icon">01</span><h3>흐름을 따라 배우기</h3><p>하나의 사례로 원리를 익히고<br>다섯 분야의 기술을 연결합니다.</p><span>블로그 읽기 →</span></a><a href="wiki/reference.html"><span class="path-icon">02</span><h3>직접 확인하며 만들기</h3><p>실행 가능한 공개 코드와<br>입출력 계약을 살펴봅니다.</p><span>코드 시작하기 →</span></a></section><section class="home-domains"><div><span class="eyebrow">EXPLORE THE SYSTEM</span><h2>다섯 분야,<br>서로 다른 책임</h2><p>각 분야를 개념, 구조, 동작,<br>기술과 검증으로 나누어 설명합니다.</p></div><div>{rows}</div></section><section class="home-case"><div><span class="eyebrow">A SHARED EXAMPLE</span><h2>짧은 요청 하나에<br>어떤 판단이 담길까요?</h2><p>책상용 램프의 소개 자료를 만든다고 생각해 보세요. 제품의 특징을 확인하고, 구성을 선택하고, 장면을 연결하는 동안 시스템의 역할이 드러납니다.</p><a href="blog/start.html">LUMA 사례 따라가기 ↗</a></div><figure>{lamp()}<figcaption>교육용으로 구성한 램프와 화면 배치</figcaption></figure></section></main>'''
    write('index.html',shell('에이전트 시스템의 구조와 기술',body,depth=0,kind='home'))

def main():
    (OUT/'assets').mkdir(parents=True,exist_ok=True)
    for filename in ('site.css','site.js','mark.svg'):
        shutil.copyfile(ROOT/'site'/filename,OUT/'assets'/filename)
    wp=ROOT/'content/wiki/pages.json';cp=ROOT/'content/blog/series.json'
    if wp.exists():wiki(json.loads(wp.read_text(encoding='utf-8-sig'))['pages'])
    if cp.exists():blog(json.loads(cp.read_text(encoding='utf-8-sig')))
    home()
    write('.nojekyll','')
    # Preserve archived preview deep links and give the old entry a clear path forward.
    write('lectures/index.html',shell('블로그 안내','<main id="main" class="course-index"><h1>p-hermes 블로그</h1><p class="lead">기존 해설 자료는 블로그 연재로 정리했습니다.</p><a class="primary-link" href="../blog/index.html">전체 블로그 읽기 →</a><details class="archive-links"><summary>이전 시안 기록</summary><a href="prototype.html">첫 시안</a><a href="redesign/index.html">상호작용 시안</a><a href="course-preview/index.html">읽기 시안</a></details></main>'))
    print('Built public website in docs/')

if __name__=='__main__':main()
