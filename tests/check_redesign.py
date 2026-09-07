"""Public, CPU-only educational fixture checks; no operational imports."""
import copy
import json
from html.parser import HTMLParser
from pathlib import Path
import subprocess
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / 'docs/lectures/redesign'


def validate_fixture(value):
    fixture = value if isinstance(value, dict) else {}
    errors = []
    count = fixture.get('selected_count')
    if isinstance(count, bool) or not isinstance(count, (int, float)) or count != 1:
        errors.append('COUNT')
    for field in ('template_id', 'variant_id', 'release_id'):
        item = fixture.get(field)
        if not isinstance(item, str) or not item.strip():
            errors.append(field.upper())
    variant = fixture.get('variant')
    if fixture.get('required_text_space') is True:
        if not isinstance(variant, dict) or variant.get('text_space') is not True:
            errors.append('TEXT_SPACE')
    return {'ok': not errors, 'errors': errors}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f"Duplicate id: {attrs['id']}"
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.refs.append(attrs[key])


def main():
    data = json.loads((DECK / 'fixtures.json').read_text())
    assert len(data['nodes']) == 5
    assert {n['id'] for n in data['nodes']} == {'task', 'knowledge', 'catalog', 'image', 'video'}
    vectors = copy.deepcopy(data['testVectors'])
    default = data['defaultFixture']
    for field, value in [('selected_count', True), ('selected_count', 0),
                         ('template_id', '   '), ('release_id', 12), ('variant', None)]:
        item = copy.deepcopy(default)
        item[field] = value
        vectors.append({'name': f'{field}-{value!r}', 'input': item})
    originals = copy.deepcopy(vectors)
    py_results = []
    for test in vectors:
        actual = validate_fixture(test['input'])
        if 'expected' in test:
            assert actual == test['expected'], (test['name'], actual)
        py_results.append(actual)
    assert vectors == originals
    js = "const fs=require('fs');const {validateFixture}=require(process.argv[1]);const v=JSON.parse(fs.readFileSync(0,'utf8'));console.log(JSON.stringify(v.map(x=>validateFixture(x.input))));"
    result = subprocess.run(['node', '-e', js, str(DECK / 'assets/demo.js')],
                            input=json.dumps(vectors), text=True, check=True, capture_output=True)
    assert json.loads(result.stdout) == py_results, 'Python/JavaScript mismatch'
    refs = 0
    for path in [DECK / 'index.html', DECK / 'guide.html']:
        doc = Page()
        doc.feed(path.read_text())
        for ref in doc.refs:
            url = urlsplit(ref)
            assert not url.scheme and not url.netloc, f'Unexpected external asset: {ref}'
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            assert target.is_relative_to(ROOT) and target.exists(), (path.name, ref)
            if url.fragment and target.suffix == '.html':
                other = Page()
                other.feed(target.read_text())
                assert url.fragment in other.ids, ref
            refs += 1
    ET.parse(DECK / 'assets/product.svg')
    json.loads((DECK / 'storyboard.json').read_text())
    claims = json.loads((ROOT / 'publication/redesign-claims.json').read_text())
    assert claims['real_media_generation'] == 'NOT_RUN'
    print(f'PASS: {len(vectors)} Python/JavaScript vectors; {refs} local references; SVG, JSON, five nodes')
    print('Scope: educational fixture only, not operational media or visual acceptance')


if __name__ == '__main__':
    main()
