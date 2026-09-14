"""Regression coverage for source-built public entry pages (standard library only)."""
import importlib.util
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_site", ROOT / "tools/build_site.py")
build_site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_site)

ENTRY_PAGES = (
    "index.html", "system/index.html", "scenarios/index.html",
    "components/index.html", "components/tasks.html",
)
NAV = (
    ("system/index.html", "전체 그림"),
    ("scenarios/index.html", "활용 장면"),
    ("components/index.html", "구성 요소"),
    ("blog/index.html", "설계 이야기"),
    ("wiki/start.html", "기술 명세"),
    ("wiki/reference.html", "시작하기"),
)


class BuildSiteTests(unittest.TestCase):
    def test_lecture_index_starts_with_system(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            with patch.object(build_site, "OUT", output):
                build_site.lectures()
            page = (output / "lectures/index.html").read_text(encoding="utf-8")
            rows = re.findall(r'<a class="chapter-row" href="([^"]+)"><span class="chapter-number">(\d+)</span><div><h2>(.*?)</h2><p>(.*?)</p>', page)
            self.assertEqual(rows[0], (
                "../slides/system/index.html", "00",
                "전체 그림 — p-hermes는 무엇을 하는가",
                "한 문장 · 시스템 지도 · 다섯 능력 · 강의 지도",
            ))
            self.assertEqual([row[0] for row in rows[1:]],
                             [f"{slug}.html" for slug in
                              ("overview", "tasks", "knowledge", "catalog", "image", "video")])
            self.assertEqual([row[1] for row in rows],
                             [f"{i:02}" for i in range(7)])
            self.assertIn("LECTURE / 01", (output / "lectures/overview.html").read_text(encoding="utf-8"))

    def test_clean_build_generates_public_entries_and_is_repeatable(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "docs"
            with patch.object(build_site, "OUT", output):
                build_site.main()
                for name in ENTRY_PAGES:
                    with self.subTest(page=name):
                        self.assertTrue((output / name).is_file(), f"not built: {name}")
                before = {p.relative_to(output): p.read_bytes()
                          for p in output.rglob("*") if p.is_file()}
                build_site.main()
                after = {p.relative_to(output): p.read_bytes()
                         for p in output.rglob("*") if p.is_file()}
                self.assertEqual(before, after)

    def test_home_structure_and_shared_navigation(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            with patch.object(build_site, "OUT", output):
                build_site.home()
            home = (output / "index.html").read_text(encoding="utf-8")
            self.assertIn("<h1>AI가 답하고 끝나지 않도록.</h1>", home)
            for section, count in (("system", 5), ("components", 5),
                                   ("scenarios", 3), ("depth", 4)):
                with self.subTest(section=section):
                    match = re.search(r'<section[^>]*id="' + section + r'"[^>]*>(.*?)</section>', home, re.S)
                    self.assertIsNotNone(match)
                    self.assertEqual(len(re.findall(r"<li(?:\s|>)", match.group(1))), count)
                    self.assertIn(f'href="#{section}"', home)
            for depth in (0, 1, 2):
                page = build_site.shell("test", '<main id="main"></main>', depth=depth)
                nav = re.search(r'<nav aria-label="주 메뉴">(.*?)</nav>', page).group(1)
                self.assertEqual(re.findall(r'<a href="([^"]+)">([^<]+)</a>', nav),
                                 [("../" * depth + href, label) for href, label in NAV])


if __name__ == "__main__":
    unittest.main()
