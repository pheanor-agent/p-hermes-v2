"""CPU-only local prototype checks. No production imports or network."""
import json
from html import unescape
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.slides = []
        self.refs = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if 'slide' in a.get('class', '').split():
            self.slides.append(a.get('id'))
        self.refs.extend(a[k] for k in ('src', 'href') if a.get(k))


def validate_contract(data):
    return (all(isinstance(data.get(k), str) and data[k].strip()
                for k in ('template_id', 'variant_id', 'release_id'))
            and type(data.get('selected_count')) is int
            and data['selected_count'] == 1)


def main():
    deck = ROOT / 'docs/lectures/prototype.html'
    page = Page(deck.read_text())
    expected = ['map', 'flow', 'timeline', 'compare', 'contract']
    assert page.slides == expected
    assert len(page.ids) == len(set(page.ids))
    assert {'prev', 'next', 'progress'} <= set(page.ids)
    required = {'objective', 'prev_bridge', 'claim', 'visual', 'doc_ref',
                'next_bridge', 'source_status', 'slide_id'}
    board = json.loads((ROOT / 'docs/lectures/storyboards/prototype.json').read_text())
    assert [x['slide_id'] for x in board] == expected
    assert all(required <= x.keys() for x in board)
    links = 0
    for f in ROOT.rglob('*.html'):
        p = Page(f.read_text())
        assert len(p.ids) == len(set(p.ids)), f.name
        for ref in p.refs:
            u = urlsplit(ref)
            assert not u.scheme and not u.netloc, 'External dependency/link requires review'
            target = (f.parent / unquote(u.path)).resolve() if u.path else f
            assert target.is_relative_to(ROOT), 'Path escape'
            assert target.exists(), ref
            if u.fragment and target.suffix == '.html':
                assert u.fragment in Page(target.read_text()).ids, ref
            links += 1
    for f in ROOT.rglob('*.md'):
        for ref in re.findall(r'\]\(([^)]+)\)', f.read_text()):
            u = urlsplit(ref)
            if not u.scheme:
                assert (f.parent / u.path).exists(), ref
    claims = json.loads((ROOT / 'publication/prototype-claims.json').read_text())
    assert [x['id'] for x in claims['claims']] == expected
    for item in claims['claims']:
        assert item['status'] in ('observed', 'proposed', 'demonstrated')
        assert (ROOT / item['evidence']).is_file()
    fixture = dict(template_id='sample-template', variant_id='sample-variant',
                   release_id='sample-release', selected_count=1)
    assert validate_contract(fixture)
    displayed = json.loads(unescape(re.search(r'<code>(.*?)</code>', deck.read_text(), re.S).group(1)))
    assert validate_contract(displayed), 'Displayed fixture failed'
    for bad in (0, 2, True, '1', None):
        assert not validate_contract(dict(fixture, selected_count=bad))
    for key in ('template_id', 'variant_id', 'release_id'):
        assert not validate_contract(dict(fixture, **{key: ''}))
    for f in ROOT.rglob('*'):
        if f.is_file() and f.suffix in ('.md', '.html', '.css', '.js', '.json'):
            text = f.read_text()
            assert not re.search(r'/home/|JOB-\d+|sk-[A-Za-z0-9]{20,}', text), 'Private-pattern hit'
    print(f'PASS: 5 slides, storyboard, claims, {links} HTML references, Markdown paths')
    print('PASS: synthetic contract positive + negative cases; private-pattern scan')
    print('NOT COVERED: real generation, rights clearance, protected-value scan, publication')

if __name__ == '__main__':
    main()
