"""Check authored coverage, executable evidence, local assets and scene links."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import hashlib
import json
import re
from build_lecture_evidence import build

ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
SLUGS=['overview','tasks','knowledge','catalog','image','video']
class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.refs=[];self.text=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for key in ['src','href','poster']:
            if key in a:self.refs.append(a[key])
    def handle_data(self,text):self.text.append(text)

def main():
    bp=json.loads((ROOT/'design/course-blueprint.json').read_text(encoding='utf-8'))
    total=0;keywords=0;pages={}
    for slug,planned in zip(SLUGS,bp['courses']):
        c=json.loads((ROOT/f'content/slides/courses/{slug}.json').read_text(encoding='utf-8'))
        assert c['keywords']==planned['keywords'],slug
        actual={s['scene'] for s in c['slides'] if s['scene']!='QA'}
        assert actual=={s['id'] for s in planned['scenes']},slug
        for scene in planned['scenes']:
            assert sum(s['seconds'] for s in c['slides'] if s['scene']==scene['id'])==scene['duration_minutes']*60
        for slide in c['slides']:
            n=slide['notes'];assert all(n.get(k) for k in ['say','cues','question','answer','bridge','sources']),slide['id']
        assert len({s['id'] for s in c['slides']})==len(c['slides'])
        assert {s['title'] for s in c['slides'] if s['kind']=='definition'}=={k['term'] for k in c['keywords']}
        total+=len(c['slides']);keywords+=len(c['keywords'])
    assert keywords==38
    evidence=json.loads((ROOT/'content/slides/evidence.json').read_text(encoding='utf-8'))
    assert build()==evidence,'Executed evidence differs from recorded teaching values'
    paths=[DOCS/'lectures/index.html',DOCS/'lectures/guide.html',DOCS/'lectures/media.html',*(DOCS/f'lectures/{s}.html' for s in SLUGS),*(DOCS/f'slides/{s}/index.html' for s in SLUGS)]
    for path in paths:
        page=Page();page.feed(path.read_text(encoding='utf-8'));assert len(page.ids)==len(set(page.ids)),path;pages[path.resolve()]=page
    refs=0
    for path,page in pages.items():
        for ref in page.refs:
            u=urlsplit(ref)
            if u.scheme or u.netloc:continue
            target=(path.parent/unquote(u.path)).resolve() if u.path else path
            if target.is_dir():target/='index.html'
            assert target.is_relative_to(DOCS) and target.is_file(),(path.name,ref)
            if u.fragment and target.suffix=='.html':
                other=pages.get(target)
                if other is None:other=Page();other.feed(target.read_text(encoding='utf-8'))
                assert unquote(u.fragment).removeprefix('/') in other.ids,(path.name,ref)
            refs+=1
    manifest=json.loads((DOCS/'assets/font-manifest.json').read_text(encoding='utf-8'));chars=set(manifest['codepoints'])
    for path,page in pages.items():
        assert not ({ord(c) for c in ''.join(page.text) if '\uac00'<=c<='\ud7a3'}-chars),f'Korean glyph coverage: {path.name}'
    video=json.loads((ROOT/'content/slides/video-evidence.json').read_text(encoding='utf-8'))
    for name,value in video['variants'].items():
        assert hashlib.sha256((ROOT/'site/slides/media'/name).read_bytes()).hexdigest()==value['probe']['sha256']
        assert sum(value['durations'])==value['probe']['duration_seconds']==12
    for asset in (ROOT/'site/slides/media').iterdir():
        assert asset.read_bytes()==(DOCS/'slides/assets/media'/asset.name).read_bytes(),asset.name
    assert video['variants']['edit-a.mp4']['source_sha256']==video['variants']['edit-b.mp4']['source_sha256']
    provenance=json.loads((ROOT/'content/slides/media-provenance.json').read_text(encoding='utf-8'))
    for asset in provenance['assets']:
        assert hashlib.sha256((ROOT/'site/slides/media'/asset['file']).read_bytes()).hexdigest()==asset['sha256']
    mapping=json.loads((ROOT/'content/slides/asset-map.json').read_text(encoding='utf-8'))
    assert {a['id'] for a in mapping['assets']}=={f'A{i:02}' for i in range(1,14)}
    for asset in mapping['assets']:
        assert all((ROOT/f).is_file() for f in asset['files']),asset['id']
    print(json.dumps({'result':'PASS','courses':6,'scenes':72,'keywords':keywords,'slides':total,'local_links':refs,'executed_evidence':'matched'},ensure_ascii=False))

if __name__=='__main__':main()
