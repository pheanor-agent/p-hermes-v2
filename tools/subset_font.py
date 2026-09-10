"""Create a content-derived font subset; optional asset build dependency.

Install requirements-assets.txt, run build_site.py, then this script. The
source Noto Sans KR and its OFL are retained at the original preview address.
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
from fontTools import subset
from fontTools import __version__ as fonttools_version
from fontTools.ttLib import TTFont

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'docs/lectures/course-preview/fonts/NotoSansKR-variable.ttf'
TARGET=ROOT/'docs/assets/HermesKR.woff2'

class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[]
    def handle_data(self,data):self.parts.append(data)
    def handle_starttag(self,tag,attrs):
        self.parts.extend(v for k,v in attrs if k in ('aria-label','alt','title') and v)

def codepoints():
    p=Text()
    paths=[ROOT/'docs/index.html',*sorted((ROOT/'docs/wiki').glob('*.html')),*sorted((ROOT/'docs/blog').glob('*.html')),*sorted((ROOT/'docs/learn').glob('*.html')),*sorted((ROOT/'docs/slides').rglob('*.html')),*sorted((ROOT/'docs/lectures').glob('*.html'))]
    for path in paths:p.feed(path.read_text(encoding='utf-8'))
    return set(map(ord,''.join(p.parts)))|set(range(32,127))

def main():
    font=TTFont(SOURCE,recalcTimestamp=False)
    points=codepoints()
    options=subset.Options();options.flavor='woff2';options.recalc_timestamp=False
    job=subset.Subsetter(options=options);job.populate(unicodes=points);job.subset(font)
    # OFL reserved-name hygiene: this derivative uses its own family name.
    for rec in font['name'].names:
        if rec.nameID in (1,4,6,16,17):
            value={1:'Hermes KR',4:'Hermes KR Regular',6:'HermesKR-Regular',16:'Hermes KR',17:'Regular'}[rec.nameID]
            rec.string=value.encode(rec.getEncoding(),errors='replace')
    font.flavor='woff2';font.save(TARGET)
    cmap=font.getBestCmap();required={v for v in points if 0xAC00<=v<=0xD7A3}
    missing=required-set(cmap)
    if missing:raise ValueError(f'missing Korean glyphs: {missing}')
    manifest={'source':'../lectures/course-preview/fonts/NotoSansKR-variable.ttf','source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(TARGET.read_bytes()).hexdigest(),'family':'Hermes KR','license':'SIL-OFL-1.1','bytes':TARGET.stat().st_size,'codepoints':sorted(cmap),'korean_characters_checked':len(required)}
    manifest['fonttools_version']=fonttools_version
    (TARGET.parent/'font-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Font: {manifest["bytes"]} bytes, {len(required)} Korean characters covered')

if __name__=='__main__':main()
