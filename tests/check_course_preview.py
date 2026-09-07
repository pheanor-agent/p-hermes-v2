"""Run with Python 3, standard library only. Checks content, local links and release hashes.
These checks do not establish visual quality or learning effectiveness.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / 'docs/lectures/course-preview'
IDS = ['request-gap', 'system-role', 'five-responsibilities', 'brief']


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.sections = []
        self.paragraphs = []
        self.refs = []
        self.scripts = 0
        self.collect = False
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.append(a['id'])
        if tag == 'section' and 'lesson' in a.get('class', '').split():
            self.sections.append(a.get('id'))
        if tag == 'p' and a.get('class') == 'prose':
            self.collect = True
            self.paragraphs.append('')
        if tag == 'script':
            self.scripts += 1
        self.refs.extend(a[k] for k in ['href', 'src'] if k in a)

    def handle_data(self, data):
        if self.collect:
            self.paragraphs[-1] += data

    def handle_endtag(self, tag):
        if tag == 'p':
            self.collect = False


def check_page(text, manuscript, path):
    p = Page(text)
    assert len(p.ids) == len(set(p.ids)), 'duplicate id'
    assert p.sections == IDS, 'section order'
    assert p.paragraphs == [t for s in manuscript['sections'] for t in s['paragraphs']], 'prose parity'
    for ref in p.refs:
        u = urlsplit(ref)
        assert not u.scheme and not u.netloc, 'runtime external resource'
        dest = (path.parent / unquote(u.path)).resolve() if u.path else path
        assert dest.is_relative_to(COURSE) and dest.is_file(), 'missing local file'
        if u.fragment:
            if dest.suffix == '.svg':
                assert u.fragment in Page(dest.read_text()).ids
            else:
                assert u.fragment in Page(dest.read_text()).ids
    return p


def main():
    m = json.loads((COURSE / 'manuscript.json').read_text())
    assert [s['id'] for s in m['sections']] == IDS
    assert m['scope']['total_sections'] == 16
    for filename in ['index.html', 'reading.html']:
        path = COURSE / filename
        p = check_page(path.read_text(), m, path)
        assert p.scripts == (1 if filename == 'index.html' else 0)
    css = (COURSE / 'course.css').read_text()
    for ref in re.findall(r'url\(([^)]+)\)', css):
        assert (COURSE / ref.strip(chr(34) + chr(39))).is_file()
    assert 'font-synthesis:none' in css and 'font-weight:100 900' in css
    assert 'font-display:swap' in css and '@media print' in css
    manifest = json.loads((ROOT / 'publication/course-preview-manifest.json').read_text())
    paths = [e['path'] for e in manifest['files']]
    assert len(paths) == len(set(paths)) == 14
    assert 'publication/course-preview-manifest.json' not in paths
    for entry in manifest['files']:
        path = ROOT / entry['path']
        assert not path.is_symlink() and path.resolve().is_relative_to(ROOT)
        data = path.read_bytes()
        assert len(data) == entry['bytes']
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], entry['path']
    # Negative tests: content loss, duplicate IDs and section reordering must fail.
    original = (COURSE / 'index.html').read_text()
    altered = [original.replace(m['sections'][0]['paragraphs'][0], '', 1),
               original.replace('id="main"', 'id="request-gap"', 1),
               original.replace('id="system-role"', 'id="other-section"', 1)]
    for bad in altered:
        try:
            check_page(bad, m, COURSE / 'index.html')
        except AssertionError:
            continue
        raise AssertionError('negative example escaped validation')
    print('PASS: 4 ordered sections, complete prose parity in both pages, local references, 14 release hashes and 3 negative cases')


if __name__ == '__main__':
    main()
