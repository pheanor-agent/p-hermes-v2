"""Validate public site links, content coverage, font coverage, and disclosure.

The text scan is a review aid, not a proof that arbitrary inputs are public.
Its input is this repository's authored public source, never a home directory.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit
import json
import hashlib
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'

class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.refs=[];self.text=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        for attr in ('src','href'):
            if attr in a:self.refs.append(a[attr])
    def handle_data(self,data):self.text.append(data)

def main():
    errors=[];pages={}
    managed=[DOCS/'index.html',*sorted((DOCS/'wiki').glob('*.html')),*sorted((DOCS/'blog').glob('*.html')),*sorted((DOCS/'learn').glob('*.html'))]
    for path in managed:
        p=Page();p.feed(path.read_text(encoding='utf-8'));pages[path]=p
        if len(p.ids)!=len(set(p.ids)):errors.append(f'{path.relative_to(ROOT)} duplicate anchors')
    count=0
    for path,p in pages.items():
        for ref in p.refs:
            u=urlsplit(ref)
            if u.scheme or u.netloc:continue
            target=(path.parent/unquote(u.path)).resolve() if u.path else path
            if target.is_dir():target=target/'index.html'
            if not target.is_relative_to(DOCS):errors.append(f'{path.name}: escaping link {ref}');continue
            if not target.is_file():errors.append(f'{path.name}: missing link {ref}');continue
            count+=1
            if u.fragment and target.suffix=='.html':
                q=pages.get(target)
                if q is None:q=Page();q.feed(target.read_text(encoding='utf-8'))
                if unquote(u.fragment) not in q.ids:errors.append(f'{path.name}: missing anchor {ref}')
    wiki=json.loads((ROOT/'content/wiki/pages.json').read_text(encoding='utf-8-sig'))['pages']
    course=json.loads((ROOT/'content/blog/series.json').read_text(encoding='utf-8-sig'))['posts']
    expected={'start','tasks','knowledge','catalog','image','video','integration'}
    if not expected<=set(x['id'] for x in wiki):errors.append('wiki missing a required domain')
    if expected!=set(x['id'] for x in course):errors.append('blog domain coverage mismatch')
    for ch in course:
        if len(ch['sections'])<3:errors.append(f'{ch["id"]}: missing depth')
        for slide in ch['sections']:
            if not all(slide.get(k) for k in ('paragraphs','claim','visual','notes','links')):errors.append(f'{slide["id"]}: incomplete teaching content')
    # Deny specific secret and private operational formats, reporting only file/rule.
    rules={'private-home':r'/(?:home|Users)/[A-Za-z0-9_-]+/', 'windows-home':r'[A-Z]:[\\/]+Users[\\/]+[A-Za-z0-9_-]+', 'private-job':r'JOB-\d{4,}', 'private-key':r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', 'credential':r'\b(?:sk-proj-|ghp_|gho_)[A-Za-z0-9_-]{20,}', 'tailnet-address':r'\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d+\.\d+\b'}
    public_roots=['content','src','examples','site','tools','tests','publication','docs']
    checked=[]
    for folder in public_roots:
        checked.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in {'.json','.py','.md','.js','.css','.svg','.html'})
    checked.extend(p for p in ROOT.iterdir() if p.is_file() and p.suffix in {'.md','.json','.toml','.yml'})
    checked=list(set(checked))
    for path in checked:
        text=path.read_text(encoding='utf-8-sig')
        for rule,pattern in rules.items():
            if re.search(pattern,text):errors.append(f'{path.relative_to(ROOT)}: privacy rule {rule}')
    fm=DOCS/'assets/font-manifest.json'
    if fm.is_file():
        manifest=json.loads(fm.read_text());chars=set(manifest['codepoints'])
        font=fm.parent/'HermesKR.woff2'
        if not font.is_file():errors.append('font binary is missing')
        elif font.stat().st_size!=manifest['bytes'] or hashlib.sha256(font.read_bytes()).hexdigest()!=manifest['output_sha256']:errors.append('font binary does not match reviewed manifest')
        source=(fm.parent/manifest['source']).resolve()
        if not source.is_relative_to(DOCS) or not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest()!=manifest['source_sha256']:errors.append('font source does not match manifest')
        for path,p in pages.items():
            missing={ord(c) for c in ''.join(p.text) if '\uac00'<=c<='\ud7a3'}-chars
            if missing:errors.append(f'{path.name}: font subset missing {len(missing)} Korean characters')
    else:errors.append('font coverage manifest is missing')
    for css in (DOCS/'assets').glob('*.css'):
        for raw in re.findall(r'url\(([^)]+)\)',css.read_text(encoding='utf-8')):
            ref=raw.strip(' "\'')
            if urlsplit(ref).scheme:continue
            asset=(css.parent/ref).resolve()
            if not asset.is_relative_to(DOCS) or not asset.is_file():errors.append(f'{css.name}: missing CSS asset')
    if errors:
        print('\n'.join(errors));return 1
    print(json.dumps({'result':'PASS','pages':len(pages),'local_links':count,'wiki_pages':len(wiki),'blog_posts':len(course),'blog_sections':sum(len(x['sections']) for x in course),'privacy_files':len(checked)},ensure_ascii=False));return 0

if __name__=='__main__':sys.exit(main())
