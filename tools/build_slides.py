"""Build independent, offline-ready HTML lecture decks from authored content."""
from pathlib import Path
import html
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/slides'
WIKI = 'https://pheanor-agent.github.io/p-hermes-v2/wiki/'


def e(value):
    return html.escape(str(value), quote=True)


def lines(value):
    return e(value).replace('\n', '<br>')


def fragment(content, index=0, extra=''):
    return f'<span class="fragment {extra}" data-fragment-index="{index}">{content}</span>'


def notes_html(slide):
    n = slide['notes']
    paragraphs = ''.join(f'<p>{lines(p)}</p>' for p in n.get('say', []))
    cues = ''.join(f'<li>{e(p)}</li>' for p in n.get('cues', []))
    sources = ''.join(f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["label"])}</a></li>' for s in n.get('sources', []))
    return (f'<h2>설명</h2>{paragraphs}<h2>진행</h2><ul>{cues}</ul>'
            f'<h2>청중에게</h2><p>{lines(n.get("question", ""))}</p>'
            f'<h2>해설</h2><p>{lines(n.get("answer", ""))}</p>'
            f'<h2>다음 연결</h2><p>{lines(n.get("bridge", ""))}</p><h2>근거</h2><ul>{sources}</ul>')


def body(slide, evidence):
    kind = slide['kind']
    d = slide.get('data', {})
    if kind == 'demo':
        return f'<div class="demo-stage"><video controls playsinline preload="metadata" poster="../assets/media/{e(d["poster"])}" aria-label="{e(d["alt"])}"><source src="../assets/media/{e(d["video"])}" type="video/webm"></video></div>'
    if kind == 'definition':
        return f'<p class="definition">{lines(d["definition"])}</p><div class="keyword-strip">'+''.join(f'<span>{e(t)}</span>' for t in d.get('terms',[]))+f'</div><p class="takeaway fragment" data-fragment-index="0">{lines(d.get("application",""))}</p>'
    if kind == 'compare':
        cells=[]
        for i,side in enumerate(d['sides']):
            cls='fragment' if i and d.get('reveal',True) else ''
            cells.append(f'<div class="{cls}" data-fragment-index="0"><p class="compare-label">{e(side[0])}</p><p class="compare-value">{lines(side[1])}</p><p class="compare-detail">{lines(side[2])}</p></div>')
        return '<div class="comparison">'+''.join(cells)+f'</div><p class="takeaway fragment" data-fragment-index="1">{lines(d.get("takeaway",""))}</p>'
    if kind == 'flow':
        nodes=[]
        for i,(label,detail) in enumerate(d['nodes']):
            cls='fragment' if i else ''
            nodes.append(f'<div class="{cls}" data-fragment-index="{max(0,i-1)}"><span class="flow-index">{i+1:02}</span><strong>{lines(label)}</strong><p>{lines(detail)}</p></div>')
        return '<div class="flow-map">'+''.join(nodes)+f'</div><p class="takeaway">{lines(d.get("takeaway",""))}</p>'
    if kind == 'code':
        output=d.get('output','')
        return f'<div class="code-stage"><div><p class="subhead">{e(d.get("label","公開 참고 코드").replace("公開","공개"))}</p><pre><code>{e(d["code"])}</code></pre></div><div class="fragment" data-fragment-index="0"><p class="subhead">{e(d.get("output_label","실행 결과"))}</p><pre class="result-code"><code>{e(output)}</code></pre></div></div><p class="code-meaning fragment" data-fragment-index="1">{lines(d.get("takeaway",""))}</p>'
    if kind == 'table':
        head=''.join(f'<th>{e(t)}</th>' for t in d['headers'])
        rows=''.join('<tr>'+''.join(f'<td>{lines(c)}</td>' for c in row)+'</tr>' for row in d['rows'])
        return f'<table class="lesson-table"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table><p class="takeaway fragment" data-fragment-index="0">{lines(d.get("takeaway",""))}</p>'
    if kind == 'recall':
        questions=''.join(f'<p><span>{i+1:02}</span>{lines(q)}</p>' for i,q in enumerate(d['questions']))
        return f'<div class="recall-questions">{questions}</div><div class="recall-answers fragment" data-fragment-index="0">{lines(d["answer"])}</div>'
    if kind == 'image-pair':
        sides=''.join(f'<div><img src="../assets/media/{e(s[0])}" alt="{e(s[1])}"><p>{e(s[1])}</p></div>' for s in d['images'])
        return f'<div class="image-pair">{sides}</div><p class="takeaway fragment" data-fragment-index="0">{lines(d["takeaway"])}</p>'
    if kind in {'media','timeline'}:
        timeline=''
        if kind=='timeline':
            cursor=0;bars=[]
            for i,duration in enumerate(d['segments']):
                bars.append(f'<div style="flex:{duration}"><b>{chr(65+i)}</b><span>{cursor}–{cursor+duration}s</span></div>');cursor+=duration
            timeline='<div class="live-timeline">'+''.join(bars)+'<span class="playhead" data-cursor></span></div><p class="playback-time" data-playback-time>0.00s</p>'
        return f'<div class="video-stage"><video controls playsinline preload="metadata" poster="../assets/media/{e(d.get("poster","luma-left.png"))}" aria-label="{e(d["alt"])}"><source src="../assets/media/{e(d["video"])}" type="video/mp4"></video><div><p class="media-duration">{e(d["duration"])}</p><p>{lines(d["observe"])}</p></div></div>{timeline}<p class="takeaway">{lines(d.get("takeaway",""))}</p>'
    if kind == 'binding':
        rows=''.join(f'<div><code>{e(field)}</code><span class="binding-line fragment" data-fragment-index="{i}"></span><code class="fragment" data-fragment-index="{i}">{e(node)}.inputs.{e(name)}</code></div>' for i,(field,(node,name)) in enumerate(evidence['catalog']['bindings'].items()))
        return f'<div class="bindings">{rows}</div><p class="takeaway">선언한 네 입력을 정해진 슬롯에 전달합니다.</p>'
    if kind == 'roles':
        top = ''.join(f'<div><strong>{e(a)}</strong><span>{e(b)}</span></div>' for a, b in [('작업','진행과 상태'),('지식','재사용할 근거'),('카탈로그','실행할 자원')])
        bottom = '<div><strong>이미지</strong><span>구도와 실행 입력</span></div><div><strong>영상</strong><span>샷과 시간</span></div>'
        return f'<div class="roles"><div class="role-top">{top}</div><p class="role-bridge">제작을 지원하는 공통 기반</p><div class="role-bottom fragment" data-fragment-index="0">{bottom}</div></div>'
    if kind == 'cas':
        before = evidence['task']['read_revision']; after = evidence['task']['after_first_update']
        return (f'<div class="cas"><div class="cas-requests"><p class="subhead">두 요청이 읽은 번호</p>'
                f'<div class="cas-row"><b>A</b><code>{before}</code>{fragment("반영",0,"accent result")}</div>'
                f'<div class="cas-row"><b>B</b><code>{before}</code>{fragment("거부",2,"difference result")}</div></div>'
                f'<div class="current-state"><p>현재 리비전</p><div class="current-number">{fragment(str(before),0,"fade-out")}{fragment(str(after),0,"accent")}</div>'
                '<p class="actual-label">공개 Store에서 실행한 값</p></div></div>'
                f'<p class="prompt-line">{fragment("B의 수정은 반영될까요?",1)}</p>')
    if kind == 'retirement':
        knowledge = evidence['knowledge']
        state = f'<span class="inline-swap">{fragment("active",0,"fade-out")}{fragment("retired",0,"difference")}</span>'
        records = f'<div class="record-row"><code>guide-v1</code><span class="record-state">{state}</span></div><div class="record-row"><code>guide-v2</code><span class="record-state">active</span></div>'
        search = f'<p class="fragment fade-out" data-fragment-index="0"><code>{e(knowledge["before"][0])}</code></p><p><code>{e(knowledge["after"][0])}</code></p>'
        return f'<div class="two-up"><div><p class="subhead">보존된 기록</p>{records}</div><div><p class="subhead">검색어: {e(knowledge["query"])}</p><div class="search-result">{search}</div></div></div><p class="meaning fragment" data-fragment-index="1">기록을 남기고, 현재 재사용 대상에서 제외합니다.</p>'
    if kind == 'hash':
        catalog = evidence['catalog']
        def side(changed):
            runtime = catalog['changed_runtime' if changed else 'original_runtime']
            sha = catalog['changed_digest' if changed else 'original_digest']
            cls = 'difference' if changed else ''
            return f'<div><p class="big-value">v{e(catalog["version"])}</p><div class="field fragment" data-fragment-index="0">runtime<code class="{cls}">{e(runtime)}</code></div><p class="hash-value fragment {cls}" data-fragment-index="1"><code>{sha[:12]}…</code></p></div>'
        return f'<div class="two-up version-pair">{side(False)}{side(True)}</div><p class="meaning fragment" data-fragment-index="1">버전은 판본을, 해시는 내용 변경을 확인합니다.</p>'
    if kind == 'photo':
        return f'<img class="photo" src="../assets/media/{e(d["image"])}" alt="{e(d["alt"])}"><div class="photo-copy"><p class="eyebrow">{e(slide["keyword"])}</p><h1>{lines(slide["title"])}</h1><p>{lines(d["copy"])}</p></div><div class="photo-guide fragment" data-fragment-index="0" aria-label="문구 공간 안내선"></div>'
    if kind == 'boundary':
        photos = ''.join(f'<div><img src="../assets/media/{e(path)}" alt="{e(label)}"><p class="film-label">{e(label)}</p></div>' for path,label in [(d['left'],'샷 A의 마지막 프레임'),(d['right'],'샷 B의 첫 프레임')])
        cuts = '<div style="flex:4">샷 A</div><div style="flex:4">샷 B</div><div style="flex:4">샷 C</div>'
        return f'<div class="film-frames">{photos}</div><div class="timeline">{cuts}<span class="boundary-mark fragment" data-fragment-index="0"></span></div><div class="time-ticks"><span>0</span><span>4</span><span>8</span><span>12초</span></div><p class="boundary-caption fragment" data-fragment-index="1">샷 경계에서 위치와 빛의 연결을 확인합니다.</p>'
    raise ValueError(f'Unknown slide composition: {kind}')


def render(course, evidence):
    slides = []
    metadata = {'title': course['title'], 'slides': []}
    for index, slide in enumerate(course['slides']):
        notes = notes_html(slide)
        metadata['slides'].append({'title':slide['title'].replace('\n',' '), 'scene':slide['scene'], 'notes_html':notes})
        classes = [f'layout-{slide["kind"]}', 'photo-slide' if slide['kind']=='photo' else '', 'dark' if slide.get('dark') else '']
        heading = '' if slide['kind']=='photo' else f'<p class="eyebrow">{e(slide["keyword"])}</p><h1>{lines(slide["title"])}</h1>'
        foot = f'<div class="slide-foot"><span>{e(slide["caption"])}</span><span>{e(slide["scene"])} · {index+1:02}</span></div>'
        slides.append(f'<section id="{e(slide["id"])}" data-scene="{e(slide["scene"])}" data-timing="{slide.get("seconds",120)}" class="{" ".join(classes)}">{heading}{body(slide,evidence)}{foot}<aside class="notes">{notes}</aside></section>')
    encoded = json.dumps(metadata, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(course['title'])} · p-hermes</title><meta name="description" content="{e(course.get('description','p-hermes 강의 슬라이드'))}"><link rel="stylesheet" href="../assets/vendor/reveal/reveal.css"><link rel="stylesheet" href="../assets/deck.css"></head>
<body><div class="reveal"><div class="slides">{''.join(slides)}</div></div>
<nav class="deck-tools" aria-label="발표 도구"><a href="../../index.html">p-hermes</a><a href="../../system/index.html">전체 그림</a><a href="../../components/index.html">구성 요소</a><button data-deck="prev" aria-label="이전 단계">←</button><span class="count" id="slide-count"></span><button data-deck="next" aria-label="다음 단계">→</button><button data-deck="speaker">발표자 노트</button><button data-deck="fullscreen">전체화면</button><button data-deck="help">키 안내</button></nav>
<div class="deck-help" role="dialog" aria-label="발표 키 안내" hidden><strong>발표 키</strong><p>→ / Space: 다음 단계<br>←: 이전 단계<br>S: 발표자 노트<br>F: 전체화면<br>Esc: 전체 보기<br>V: 현재 영상 재생·정지<br>H: 이 안내</p><p>발표자 노트는 별도 창에 표시됩니다. 팝업을 허용하면 오프라인에서도 사용할 수 있습니다.</p><button data-close-help>닫기</button></div>
<script type="application/json" id="course-data">{encoded}</script><script src="../assets/vendor/reveal/reveal.js"></script><script src="../assets/deck.js"></script></body></html>'''


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    shutil.copytree(ROOT/'site/slides',OUT/'assets',dirs_exist_ok=True)
    evidence=json.loads((ROOT/'content/slides/evidence.json').read_text(encoding='utf-8'))
    courses=sorted((ROOT/'content/slides/courses').glob('*.json'))
    for path in courses:
        course=json.loads(path.read_text(encoding='utf-8'))
        destination=OUT/course['slug'];destination.mkdir(exist_ok=True)
        (destination/'index.html').write_text(render(course,evidence),encoding='utf-8',newline='\n')
        print(course['slug'],len(course['slides']),'slides')


if __name__=='__main__':main()
