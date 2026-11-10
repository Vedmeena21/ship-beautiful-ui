#!/usr/bin/env python3
"""Check a DESIGN.md file: structure, token references and color contrast.

Checks
  structure   front matter present, `name` and `colors` present, no duplicate keys
  sections    `##` sections in the expected order, no duplicates
  colors      every color value is a valid CSS color
  refs        every "{group.token}" reference points to a real token
  components  only known component properties
  contrast    WCAG contrast for text pairs: component text/background,
              ink/base, muted/base, muted/surface, on-accent/accent

Usage:
  python3 scripts/lint_design.py DESIGN.md
  python3 scripts/lint_design.py DESIGN.md --json

Exit code 1 when there are errors. Standard library only.
"""
import argparse
import json
import re
import sys

SECTION_ORDER = [
    ("overview", {"overview", "brand & style"}),
    ("colors", {"colors"}),
    ("typography", {"typography"}),
    ("layout", {"layout", "layout & spacing"}),
    ("elevation", {"elevation & depth", "elevation"}),
    ("shapes", {"shapes"}),
    ("components", {"components"}),
    ("dos", {"do's and don'ts", "dos and don'ts"}),
]
COMPONENT_PROPS = {"backgroundColor", "textColor", "typography", "rounded", "padding", "size", "height", "width"}
NAMED = {"black": "#000000", "white": "#FFFFFF", "transparent": None, "currentcolor": None}


# --- tiny YAML subset: nested maps by indentation, scalars, quoted strings, comments ---
def parse_yaml(text, findings):
    root, stack = {}, [(-1, None)]
    stack[0] = (-1, root)
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.split(" #")[0].rstrip() if not raw.lstrip().startswith(("'", '"')) else raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        m = re.match(r"\s*([^:]+?)\s*:\s*(.*)$", line)
        if not m:
            findings.append(("error", "structure", f"front matter line {n} is not 'key: value': {raw.strip()}"))
            continue
        key, val = m.group(1).strip().strip("'\""), m.group(2).strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if key in parent:
            findings.append(("error", "structure", f"duplicate key '{key}' (line {n})"))
        if val == "":
            parent[key] = {}
            stack.append((indent, parent[key]))
        else:
            if (val[0] == val[-1]) and val[0] in "'\"" and len(val) >= 2:
                val = val[1:-1]
            parent[key] = val
    return root


def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h[:3])
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def luminance(h):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in hex_to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def as_hex(value):
    v = value.strip().lower()
    if re.fullmatch(r"#[0-9a-f]{3,4}|#[0-9a-f]{6}|#[0-9a-f]{8}", v):
        return "#" + (v[1:7] if len(v) >= 7 else "".join(c * 2 for c in v[1:4]))
    return NAMED.get(v)


def valid_color(value):
    v = value.strip().lower()
    return bool(re.fullmatch(r"#[0-9a-f]{3,4}|#[0-9a-f]{6}|#[0-9a-f]{8}", v)
                or re.fullmatch(r"(rgb|rgba|hsl|hsla|oklch|oklab|lab|lch|color)\(.+\)", v)
                or re.fullmatch(r"[a-z]+", v))


def resolve(tokens, value):
    m = re.fullmatch(r"\{([\w-]+)\.([\w-]+)\}", value.strip())
    if not m:
        return value
    group = tokens.get(m.group(1))
    if not isinstance(group, dict) or m.group(2) not in group:
        return None
    return group[m.group(2)]


def lint(text):
    f = []
    m = re.match(r"﻿?---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return [("error", "structure", "no YAML front matter between '---' lines at the top")], {}
    tokens = parse_yaml(m.group(1), f)
    body = m.group(2)

    for key in ("name", "colors"):
        if key not in tokens:
            f.append(("error", "structure", f"missing '{key}'"))
    colors = tokens.get("colors", {}) if isinstance(tokens.get("colors"), dict) else {}

    for k, v in colors.items():
        if not isinstance(v, str) or not valid_color(v):
            f.append(("error", "colors", f"colors.{k} is not a valid CSS color: {v!r}"))

    # references anywhere in tokens
    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + [k])
        elif isinstance(node, str) and node.strip().startswith("{"):
            if resolve(tokens, node) is None:
                f.append(("error", "refs", f"{'.'.join(path)} points to missing token {node}"))
    walk(tokens, [])

    comps = tokens.get("components", {}) if isinstance(tokens.get("components"), dict) else {}
    for name, props in comps.items():
        if not isinstance(props, dict):
            f.append(("error", "components", f"components.{name} should be a map of properties"))
            continue
        for p in props:
            if p not in COMPONENT_PROPS:
                f.append(("warning", "components", f"components.{name}.{p} is not a known property ({', '.join(sorted(COMPONENT_PROPS))})"))
        bg, fg = props.get("backgroundColor"), props.get("textColor")
        if bg and fg:
            bgh, fgh = as_hex(resolve(tokens, bg) or ""), as_hex(resolve(tokens, fg) or "")
            if bgh and fgh:
                r = contrast(bgh, fgh)
                if r < 4.5:
                    f.append(("error", "contrast", f"components.{name}: text on background is {r:.2f}:1, needs 4.5:1"))

    pairs = [("ink", "base", 4.5), ("muted", "base", 4.5), ("muted", "surface", 4.5), ("ink", "surface", 4.5), ("on-accent", "accent", 4.5)]
    for a, b, need in pairs:
        if a in colors and b in colors:
            ha, hb = as_hex(colors[a]), as_hex(colors[b])
            if ha and hb:
                r = contrast(ha, hb)
                if r < need:
                    f.append(("error", "contrast", f"{a} on {b} is {r:.2f}:1, needs {need}:1"))
    if "accent" in colors and "base" in colors:
        ha, hb = as_hex(colors["accent"]), as_hex(colors["base"])
        if ha and hb and contrast(ha, hb) < 3:
            f.append(("warning", "contrast", f"accent on base is {contrast(ha, hb):.2f}:1; links and controls need 3:1"))

    heads = [h.strip().lower() for h in re.findall(r"^##\s+(.+?)\s*$", body, re.M)]
    seen, last = set(), -1
    for h in heads:
        idx = next((i for i, (_, names) in enumerate(SECTION_ORDER) if h in names), None)
        if h in seen:
            f.append(("error", "sections", f"duplicate section '## {h}'"))
        seen.add(h)
        if idx is None:
            continue
        if idx < last:
            f.append(("warning", "sections", f"'## {h}' is out of order (expected: Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts)"))
        last = max(last, idx)
    if "overview" not in seen and "brand & style" not in seen:
        f.append(("warning", "sections", "no '## Overview' section: put the brief there"))
    if re.search(r"Replace (with|every|Display|Body)|Subject: \.\.\.", text):
        f.append(("info", "structure", "template placeholders are still present"))
    return f, tokens


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    with open(a.path, encoding="utf-8") as fh:
        findings, _ = lint(fh.read())
    summary = {s: sum(1 for x in findings if x[0] == s) for s in ("error", "warning", "info")}
    if a.json:
        print(json.dumps({"findings": [{"severity": s, "check": c, "message": m} for s, c, m in findings], "summary": summary}, indent=2))
    else:
        for s, c, m in findings:
            print(f"{s.upper():8} {c:11} {m}")
        print(f"\n{summary['error']} errors, {summary['warning']} warnings, {summary['info']} info")
    return 1 if summary["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
