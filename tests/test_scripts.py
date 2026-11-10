"""Tests for the ship-beautiful-ui scripts. Run: python3 -m unittest discover tests"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "ship-beautiful-ui")
SCRIPTS = os.path.join(SKILL, "scripts")
FIX = os.path.join(ROOT, "tests", "fixtures")
sys.path.insert(0, SCRIPTS)

import derive  # noqa: E402
import lint_design  # noqa: E402


def run(script, *args):
    p = subprocess.run([sys.executable, "-I", os.path.join(SCRIPTS, script), *args], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def rules(path):
    code, out, _ = run("detect.py", path, "--json")
    return code, {f["rule"] for f in json.loads(out)["findings"]}


class DataTests(unittest.TestCase):
    def load(self, name):
        with open(os.path.join(SKILL, "data", name), encoding="utf-8") as f:
            return json.load(f)

    def test_palettes_pass_contrast(self):
        pal = self.load("palettes.json")["palettes"]
        self.assertGreaterEqual(len(pal), 60)
        ids = [p["id"] for p in pal]
        self.assertEqual(len(ids), len(set(ids)), "duplicate palette ids")
        for p in pal:
            c = p["colors"]
            self.assertGreaterEqual(derive.contrast(c["ink"], c["base"]), 12, p["id"])
            self.assertGreaterEqual(derive.contrast(c["muted"], c["base"]), 4.5, p["id"])
            self.assertGreaterEqual(derive.contrast(c["on-accent"], c["accent"]), 4.5, p["id"])
            self.assertGreaterEqual(derive.contrast(c["accent"], c["base"]), 3, p["id"])

    def test_library_sizes(self):
        self.assertGreaterEqual(len(self.load("type-pairings.json")["pairings"]), 40)
        self.assertGreaterEqual(len(self.load("layouts.json")["layouts"]), 20)
        self.assertGreaterEqual(len(self.load("materials.json")["materials"]), 75)


class DeriveTests(unittest.TestCase):
    def test_words_match_materials(self):
        chosen = derive.match("darkroom safelight, contact sheet, grey card", derive.load_materials())
        self.assertEqual([m["id"] for m in chosen], ["safelight-red", "contact-sheet", "grey-card"])

    def test_derived_palettes_pass(self):
        mats = {m["id"]: m for m in derive.load_materials()}
        for ids in (["crust", "flour", "espresso"], ["moss", "snow"], ["arcade-magenta", "vinyl"], ["pollen", "chalk"]):
            for mode in ("light", "dark"):
                colors, checks = derive.build([mats[i] for i in ids], mode)
                self.assertGreaterEqual(checks["ink/base"], 12, (ids, mode))
                self.assertGreaterEqual(checks["muted/base"], 4.5, (ids, mode))
                self.assertGreaterEqual(checks["on-accent/accent"], 4.5, (ids, mode))
                self.assertGreaterEqual(checks["accent/base"], 3, (ids, mode))


class DirectionTests(unittest.TestCase):
    def test_deal_is_deterministic(self):
        a = run("direction.py", "--kind", "food", "--brief", "bakery", "--json")[1]
        b = run("direction.py", "--kind", "food", "--brief", "bakery", "--json")[1]
        self.assertEqual(a, b)

    def test_written_design_md_lints_clean(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "DESIGN.md")
            code, _, err = run("direction.py", "--kind", "fintech", "--brief", "x", "--choose", "2", "--write", path)
            self.assertEqual(code, 0, err)
            code, out, _ = run("lint_design.py", path)
            self.assertEqual(code, 0, out)


class LintTests(unittest.TestCase):
    def test_template_has_no_errors(self):
        code, out, _ = run("lint_design.py", os.path.join(SKILL, "templates", "DESIGN.md"))
        self.assertEqual(code, 0, out)

    def test_bad_file_errors(self):
        bad = '---\nname: Bad\ncolors:\n  base: "#FFFFFF"\n  ink: "#BBBBBB"\ncomponents:\n  link:\n    textColor: "{colors.missing}"\n---\n## Colors\n## Colors\n'
        findings, _ = lint_design.lint(bad)
        checks = {c for s, c, m in findings if s == "error"}
        self.assertIn("refs", checks)
        self.assertIn("contrast", checks)
        self.assertIn("sections", checks)


class DetectTests(unittest.TestCase):
    def test_slop_page_is_caught(self):
        code, found = rules(os.path.join(FIX, "slop.html"))
        self.assertEqual(code, 1)
        for r in ("SBU001", "SBU002", "SBU007", "SBU008", "SBU010", "SBU011", "SBU013", "SBU019"):
            self.assertIn(r, found)

    def test_a11y_page_is_caught(self):
        _, found = rules(os.path.join(FIX, "slop-a11y.html"))
        for r in ("SBU024", "SBU025", "SBU031", "SBU040"):
            self.assertIn(r, found)

    def test_clean_page_passes(self):
        code, found = rules(os.path.join(FIX, "clean.html"))
        self.assertEqual(code, 0)
        self.assertEqual(found, set())

    def test_forty_rules(self):
        _, out, _ = run("detect.py", "--list-rules")
        self.assertEqual(out.count("SBU0"), 40)


if __name__ == "__main__":
    unittest.main()
