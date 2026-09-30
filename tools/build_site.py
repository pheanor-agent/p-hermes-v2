"""Build the public site from root-level reviewed artifacts without rewriting authored pages."""
from __future__ import annotations

from html import escape
from pathlib import Path
import shutil
import html
import re
import zipfile
import hashlib
import os
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs"
HOME = ROOT / "site" / "index.html"
EXAMPLE_NAMES = ("portable-worker", "image-pipeline", "knowledge-context-check", "integration-check")

CACHE_SUFFIXES = {".pyc", ".pyo", ".pyd"}


def is_cache_artifact(path: Path) -> bool:
    return "__pycache__" in path.parts or path.suffix.lower() in CACHE_SUFFIXES


def ignore_cache_artifacts(_directory: str, names: list[str]) -> set[str]:
    return {name for name in names if name == "__pycache__" or Path(name).suffix.lower() in CACHE_SUFFIXES}



def page(title: str, links: list[tuple[str, str]], body: str = "", depth: int = 1) -> str:
    items = "\n".join(f'<li><a href="{escape(href, quote=True)}">{escape(label)}</a></li>' for href, label in links)
    prefix = "../" * depth
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><link rel="stylesheet" href="{prefix}assets/design-system.css"></head><body><header class="topbar"><a href="{prefix}index.html">p-hermes</a></header><main><section class="hero"><h1>{escape(title)}</h1><nav aria-label="목차"><ul>{items}</ul></nav></section><article>{body}</article></main></body></html>'''

def render_markdown(text: str) -> str:
    out=[]; paragraph=[]; code=[]; in_code=False
    def flush():
        if paragraph:
            out.append('<p>'+html.escape(' '.join(x.strip() for x in paragraph))+'</p>'); paragraph.clear()
    for line in text.splitlines():
        if line.startswith('```'):
            if in_code:
                out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>'); code=[]; in_code=False
            else: flush(); in_code=True
            continue
        if in_code: code.append(line); continue
        if not line.strip(): flush(); continue
        m=re.match(r'^(#{1,4})\s+(.+)',line)
        if m: flush(); level=len(m.group(1)); out.append(f'<h{level}>{html.escape(m.group(2))}</h{level}>'); continue
        if line.startswith(('- ','* ')):
            flush(); out.append('<p>• '+html.escape(line[2:])+'</p>'); continue
        paragraph.append(line)
    flush()
    if code: out.append('<pre><code>'+html.escape('\n'.join(code))+'</code></pre>')
    return '\n'.join(out)


def build() -> None:
    """Build to a validated sibling directory, then atomically replace docs."""
    global OUT
    if not HOME.is_file():
        raise FileNotFoundError(f"authored landing page missing: {HOME}")
    authored_home = HOME.read_bytes()
    prior_out = OUT
    with tempfile.TemporaryDirectory(prefix=".docs-build-", dir=ROOT) as work:
        work_path = Path(work)
        candidate = work_path / "docs"
        OUT = candidate
        try:
            _build()
            if (candidate / "index.html").read_bytes() != authored_home:
                raise RuntimeError("generated landing page differs from current authored source")
            env = os.environ.copy()
            env["DOCS_PATH"] = str(candidate)
            result = subprocess.run(
                [sys.executable, "-B", str(ROOT / "tools" / "check_site.py")],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            if result.returncode:
                raise RuntimeError("candidate site validation failed:\n" + result.stdout + result.stderr)
            old = work_path / "old-docs"
            if prior_out.exists():
                os.replace(prior_out, old)
            try:
                os.replace(candidate, prior_out)
            except Exception:
                if old.exists() and not prior_out.exists():
                    os.replace(old, prior_out)
                raise
        finally:
            OUT = prior_out
    print(f"Built public site: {OUT}")


def _build() -> None:
    """Populate OUT, which is a fresh temporary directory owned by build()."""
    OUT.mkdir(parents=True)
    # Site HTML, CSS, JavaScript, SVG, and media are copied byte-for-byte.
    shutil.copytree(ROOT / "site", OUT, dirs_exist_ok=True, copy_function=shutil.copy2, ignore=ignore_cache_artifacts)
    for authored in OUT.rglob('*.html'):
        rel=authored.relative_to(OUT)
        text=authored.read_text(encoding='utf-8')
        if rel.parts and rel.parts[0]=='articles': text=text.replace('../../','../')
        for old,new in (('p-hermes · 미리보기','p-hermes'),('p-hermes · 검토용 미리보기','p-hermes 공개 문서'),('검토용 문서 미리보기','공개 문서'),('검토용 미리보기','공개 문서'),('미리보기 목차','목차'),('publish-ready preview','p-hermes 공개 자료')):
            text=text.replace(old,new)
        authored.write_text(text,encoding='utf-8',newline='\n')
    # Keep reviewed source materials reachable for offline use and auditing.
    for name in ("content", "reference", "tests", "publication"):
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, OUT / "downloads" / name, dirs_exist_ok=True, copy_function=shutil.copy2, ignore=ignore_cache_artifacts)
    example_root = ROOT / "examples"
    for name in EXAMPLE_NAMES[1:]:
        src = example_root / name
        if src.is_dir():
            shutil.copytree(src, OUT / "downloads" / "examples" / name, dirs_exist_ok=True, copy_function=shutil.copy2, ignore=ignore_cache_artifacts)
    # The portable-worker example consists of the standalone reference package and contract tests.
    portable = OUT / "downloads" / "examples" / "portable-worker"
    portable.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "reference", portable / "src", dirs_exist_ok=True, copy_function=shutil.copy2, ignore=ignore_cache_artifacts)
    shutil.copytree(ROOT / "tests", portable / "tests", dirs_exist_ok=True, copy_function=shutil.copy2, ignore=ignore_cache_artifacts)
    for d, title in (("lectures", "강의 목차"), ("wiki", "위키 목차"), ("examples", "예제 목차")):
        files = sorted(p for p in (ROOT / "site" / d).rglob("*.html") if p.name != "index.html")
        (OUT / d / "index.html").parent.mkdir(parents=True, exist_ok=True)
        links = [(p.relative_to(ROOT / "site" / d).as_posix(), p.stem) for p in files]
        if d == "lectures":
            from deckify import LECTURES
            links = [(name, f"{number} · {title}") for name, number, title in LECTURES]
        elif d == "wiki":
            links = []
            for source in files:
                heading = re.search(r"<h1[^>]*>(.*?)</h1>", source.read_text(encoding="utf-8"), re.S)
                label = html.unescape(re.sub(r"<[^>]+>", "", heading.group(1))).strip() if heading else source.stem
                links.append((source.relative_to(ROOT / "site" / d).as_posix(), label))
        elif d == "examples":
            links = [(f"{name}/README.html", label) for name, label in (
                ("portable-worker", "파일로 요청과 응답 연결하기"),
                ("image-pipeline", "이미지 파이프라인 구성 확인하기"),
                ("knowledge-context-check", "지식 후보의 출처와 상태 확인하기"),
                ("integration-check", "요청부터 결과까지 통합 흐름 확인하기"),
            )]
        (OUT / d / "index.html").write_text(page(title, links), encoding="utf-8", newline="\n")
    (OUT / "articles").mkdir(exist_ok=True)
    articles = sorted((ROOT / "site" / "articles").glob("*.html"))
    (OUT / "articles" / "index.html").write_text(page("읽을거리", [(p.name, p.stem) for p in articles]), encoding="utf-8", newline="\n")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    # Bundle the four offline examples with the portable reference package.
    archive = OUT / "downloads" / "examples.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        def add_deterministic(path: Path, arcname: Path) -> None:
            info = zipfile.ZipInfo(arcname.as_posix(), date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, path.read_bytes())
        for name in EXAMPLE_NAMES[1:]:
            for p in sorted((ROOT / "examples" / name).rglob("*")):
                if p.is_file() and not is_cache_artifact(p):
                    add_deterministic(p, p.relative_to(ROOT / "examples"))
        for p in sorted((ROOT / "reference").rglob("*")):
            if p.is_file() and not is_cache_artifact(p):
                add_deterministic(p, Path("portable-worker/src") / p.relative_to(ROOT / "reference"))
        for p in sorted((ROOT / "tests").rglob("*")):
            if p.is_file() and not is_cache_artifact(p):
                add_deterministic(p, Path("portable-worker/tests") / p.relative_to(ROOT / "tests"))
        portable_readme = ROOT / "examples" / "portable-worker" / "README.md"
        if portable_readme.is_file():
            add_deterministic(portable_readme, Path("portable-worker/README.md"))
    # Render offline example guides and escaped source views; ship their originals too.
    code_rows=[]
    inputs=[]
    for base in (ROOT/'reference', ROOT/'tests', ROOT/'examples'):
        inputs.extend(p for p in base.rglob('*') if p.is_file() and not is_cache_artifact(p))
    for src in sorted(inputs):
        rel=src.relative_to(ROOT)
        (OUT/'downloads'/rel).parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(src,OUT/'downloads'/rel)
        if src.suffix in {'.py','.json','.md','.txt','.toml'}:
            view=OUT/'code'/Path(str(rel)+'.html'); view.parent.mkdir(parents=True,exist_ok=True)
            depth=len(view.relative_to(OUT).parts)-1
            base='../'*depth
            body=f'<p><a href="{base}code/index.html">코드 목록</a> · <a href="{base}downloads/{rel.as_posix()}">원본 내려받기</a></p><h1>{escape(rel.as_posix())}</h1><pre><code>{html.escape(src.read_text(encoding="utf-8"))}</code></pre>'
            view.write_text(f'<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(rel.as_posix())}</title><link rel="stylesheet" href="{base}assets/design-system.css"><body><main>{body}</main></body></html>',encoding='utf-8',newline='\n')
            code_rows.append((f'{rel.as_posix()}.html',rel.as_posix()))
    code_index=OUT/'code/index.html'; code_index.parent.mkdir(parents=True,exist_ok=True)
    code_index.write_text(page('코드·예제·테스트',code_rows),encoding='utf-8',newline='\n')
    for name in EXAMPLE_NAMES[1:]:
        src=ROOT/'examples'/name
        for doc in ('README','PROMPT'):
            md=src/f'{doc}.md'
            if md.is_file():
                target=OUT/'examples'/name/f'{doc}.html'; target.parent.mkdir(parents=True,exist_ok=True)
                rendered=page(f'{name} · {doc}',[(f'../../downloads/examples/{name}/{md.name}','원본 Markdown 내려받기')],body=render_markdown(md.read_text(encoding='utf-8')),depth=2)
                rendered=rendered.replace('href="../assets/', 'href="../../assets/').replace('href="../index.html"', 'href="../../index.html"')
                target.write_text(rendered,encoding='utf-8',newline='\n')
    # Reuse the authored example navigation and rendered documentation pages.
    shutil.copytree(ROOT/'site/examples', OUT/'examples', dirs_exist_ok=True, copy_function=shutil.copy2, ignore=ignore_cache_artifacts)
    for authored in (OUT/'examples').rglob('*.html'):
        rel=authored.relative_to(OUT/'examples')
        text=authored.read_text(encoding='utf-8')
        prefix='../' * len(rel.parts)
        text=text.replace('../../assets/',prefix+'assets/').replace('../../index.html',prefix+'index.html')
        authored.write_text(text,encoding='utf-8',newline='\n')
    # Compile the six authored lecture sources with the retained deckify renderer.
    import sys
    sys.path.insert(0, str(ROOT / 'tools'))
    import deckify
    deckify.build(ROOT / 'site' / 'lectures', OUT / 'lectures')
    # Apply the existing wiki lookup layout to the generated public wiki pages.
    import wikify
    wikify.build(OUT / 'wiki')
    # Preserve the supplied homepage exactly and make it the root landing page last.
    shutil.copy2(ROOT / "site" / "index.html", OUT / "index.html")
    actual = hashlib.sha256((OUT / "index.html").read_bytes()).hexdigest()
    source = hashlib.sha256((HOME).read_bytes()).hexdigest()
    if actual != source:
        raise RuntimeError(f"landing page verification failed: {actual} != {source}")


if __name__ == "__main__":
    build()
