"""Standard-library checks of pinned font files, variable axes and glyph coverage.
Run: python3 tests/check_course_fonts.py. Browser glyph-face checks are separate.
"""
from pathlib import Path
import hashlib
import json
import struct

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / 'docs/lectures/course-preview/fonts'


def tables(data):
    assert data[:4] == b'\x00\x01\x00\x00'
    count = struct.unpack_from('>H', data, 4)[0]
    result = {}
    for i in range(count):
        tag, _, offset, length = struct.unpack_from('>4sIII', data, 12 + 16 * i)
        assert offset + length <= len(data)
        result[tag.decode('ascii')] = data[offset:offset + length]
    return result


def cmap_glyph(cmap, code):
    count = struct.unpack_from('>H', cmap, 2)[0]
    for i in range(count):
        _, _, off = struct.unpack_from('>HHI', cmap, 4 + i * 8)
        if struct.unpack_from('>H', cmap, off)[0] != 12:
            continue
        groups = struct.unpack_from('>I', cmap, off + 12)[0]
        for n in range(groups):
            start, end, glyph = struct.unpack_from('>III', cmap, off + 16 + 12 * n)
            if start <= code <= end:
                return glyph + code - start
    return 0


def main():
    source = json.loads((FONTS / 'SOURCE.json').read_text())
    for name, expected in source['files'].items():
        data = (FONTS / name).read_bytes()
        assert len(data) == expected['bytes']
        assert hashlib.sha256(data).hexdigest() == expected['sha256'], name
    t = tables((FONTS / 'NotoSansKR-variable.ttf').read_bytes())
    fvar = t['fvar']
    axis_offset, _, axis_count, axis_size = struct.unpack_from('>HHHH', fvar, 4)
    axes = []
    for i in range(axis_count):
        tag, minimum, default, maximum = struct.unpack_from('>4siii', fvar, axis_offset + axis_size * i)
        axes.append((tag.decode(), minimum / 65536, maximum / 65536))
    assert axes == [('wght', 100.0, 900.0)]
    assert struct.unpack_from('>H', t['maxp'], 4)[0] == source['glyph_count']
    assert (FONTS / 'NotoSansKR-variable.woff2').read_bytes()[:4] == b'wOF2'
    manuscript = json.loads((FONTS.parent / 'manuscript.json').read_text())
    text = ''.join(s['title'] + ''.join(s['paragraphs']) for s in manuscript['sections'])
    chars = {c for c in text if '\uac00' <= c <= '\ud7a3'}
    assert chars and all(cmap_glyph(t['cmap'], ord(c)) for c in chars)
    assert 'SIL OPEN FONT LICENSE' in (FONTS / 'OFL.txt').read_text()
    assert 'OFL-1.1' == source['license']
    assert 'Noto Sans KR' in (ROOT / 'THIRD_PARTY_NOTICES.md').read_text()
    print(f'PASS: 3 pinned hashes, variable weight100–900, {len(chars)} manuscript Hangul characters, full glyph count and OFL notice')


if __name__ == '__main__':
    main()
