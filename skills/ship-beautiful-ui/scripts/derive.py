#!/usr/bin/env python3
"""Derive a palette from the subject's own world instead of picking a template.

Give it words from the subject (or material ids from data/materials.json). It
matches them to materials, assigns roles (base, ink, accent, accent-2), builds
the supporting colors, then fixes contrast so the result passes WCAG AA.

Usage:
  python3 scripts/derive.py --suggest photography      # materials that fit a kind
  python3 scripts/derive.py --words "darkroom safelight, contact sheet, grey card, film edge"
  python3 scripts/derive.py --materials safelight-red,contact-sheet,grey-card --mode dark
  python3 scripts/derive.py --words "bakery, crust, flour" --yaml   # colors block for DESIGN.md

Standard library only.
"""
import argparse
import colorsys
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


# ---------- color helpers ----------
def to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def to_hex(rgb):
    return "#" + "".join(f"{round(max(0, min(1, c)) * 255):02X}" for c in rgb)


def lum(h):
    def ch(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)


def hls(h):
    return colorsys.rgb_to_hls(*to_rgb(h))


def from_hls(h, l, s):
    return to_hex(colorsys.hls_to_rgb(h, max(0, min(1, l)), max(0, min(1, s))))


def mix(a, b, t):
    ra, rb = to_rgb(a), to_rgb(b)
    return to_hex(tuple(x + (y - x) * t for x, y in zip(ra, rb)))


def push_contrast(fg, bg, target, max_steps=120):
    """Move fg lightness away from bg until contrast >= target."""
    h, l, s = hls(fg)
    step = -0.01 if lum(bg) > 0.35 else 0.01
    n = 0
    while contrast(from_hls(h, l, s), bg) < target and n < max_steps:
        l += step
        n += 1
    return from_hls(h, l, s)


# ---------- matching ----------
def load_materials():
    with open(os.path.join(DATA, "materials.json"), encoding="utf-8") as f:
        return json.load(f)["materials"]


def tokens(s):
    return set(re.findall(r"[a-z]+", s.lower())) - {"the", "a", "of", "and", "an", "for", "with", "s"}


def match(words, mats):
    """Score each material against each phrase by shared tokens (id, note, family)."""
    chosen = []
    for phrase in [p.strip() for p in re.split(r"[,;\n]", words) if p.strip()]:
        pt = tokens(phrase)
        best, score = None, 0
        for m in mats:
            mt = tokens(m["id"].replace("-", " ")) | tokens(m["note"])
            sc = len(pt & mt) * 2 + (1 if m["family"] in pt else 0)
            if sc > score and m not in chosen:
                best, score = m, sc
        if best:
            chosen.append(best)
    return chosen


# ---------- palette ----------
def build(mats, mode):
    by_role = {r: [m for m in mats if m["role"] == r] for r in ("base", "ink", "accent", "neutral")}
    accents = by_role["accent"] or [m for m in mats if m["role"] == "neutral"]
    if not accents:
        raise SystemExit("Need at least one accent or neutral material. Add a colorful word (a material, a sign, a food).")
    accent = accents[0]["color"]
    accent2 = accents[1]["color"] if len(accents) > 1 else None
    ink_src = by_role["ink"][0]["color"] if by_role["ink"] else None
    base_src = by_role["base"][0]["color"] if by_role["base"] else None
    neutral = by_role["neutral"][0]["color"] if by_role["neutral"] else None
    ah, al, as_ = hls(accent)

    if mode == "dark":
        base = ink_src or from_hls(ah, 0.07, min(as_, 0.25))
        h, l, s = hls(base)
        base = from_hls(h, min(l, 0.09), min(s, 0.3))
        ink = base_src or from_hls(ah, 0.93, 0.15)
        surface = mix(base, ink, 0.05)
    else:
        base = base_src or (from_hls(hls(neutral)[0], 0.96, 0.18) if neutral else from_hls(ah, 0.97, 0.12))
        h, l, s = hls(base)
        base = from_hls(h, max(l, 0.93), min(s, 0.35))
        ink = ink_src or from_hls(ah, 0.12, min(as_, 0.35))
        surface = mix(base, "#FFFFFF", 0.6)

    ink = push_contrast(ink, base, 12)
    muted = push_contrast(mix(ink, base, 0.42), base, 4.6)
    muted = push_contrast(muted, surface, 4.6)
    line = mix(base, ink, 0.14)
    on_accent = "#FFFFFF" if contrast("#FFFFFF", accent) >= contrast("#111111", accent) else "#111111"
    if contrast(on_accent, accent) < 4.6:
        accent = push_contrast(accent, on_accent, 4.6)
    if contrast(accent, base) < 3:
        accent = push_contrast(accent, base, 3)
    colors = {"base": base, "surface": surface, "ink": ink, "muted": muted, "line": line, "accent": accent, "on-accent": on_accent}
    if accent2:
        colors["accent-2"] = push_contrast(accent2, base, 3)
    checks = {
        "ink/base": contrast(ink, base), "muted/base": contrast(muted, base),
        "muted/surface": contrast(muted, surface), "on-accent/accent": contrast(on_accent, accent),
        "accent/base": contrast(accent, base),
    }
    return colors, {k: round(v, 2) for k, v in checks.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--words", help="comma-separated words from the subject's world")
    ap.add_argument("--materials", help="comma-separated material ids")
    ap.add_argument("--mode", default="light", choices=["light", "dark"])
    ap.add_argument("--suggest", metavar="KIND", help="list materials that fit a product kind")
    ap.add_argument("--yaml", action="store_true", help="print a colors: block for DESIGN.md")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    mats = load_materials()

    if a.suggest:
        fit = [m for m in mats if a.suggest in m["fits"]] or mats
        for m in fit:
            print(f"{m['id']:18} {m['role']:8} {m['color']}  {m['note']}")
        return 0
    if a.materials:
        ids = [x.strip() for x in a.materials.split(",") if x.strip()]
        lookup = {m["id"]: m for m in mats}
        missing = [i for i in ids if i not in lookup]
        if missing:
            ap.error("unknown material ids: " + ", ".join(missing) + " (see data/materials.json)")
        chosen = [lookup[i] for i in ids]
    elif a.words:
        chosen = match(a.words, mats)
        if not chosen:
            ap.error("no materials matched; try concrete nouns (paper, brass, moss, espresso) or --suggest KIND")
    else:
        ap.error("give --words, --materials or --suggest")

    colors, checks = build(chosen, a.mode)
    if a.json:
        print(json.dumps({"materials": [m["id"] for m in chosen], "mode": a.mode, "colors": colors, "contrast": checks}, indent=2))
    elif a.yaml:
        print("colors:")
        for k, v in colors.items():
            print(f'  {k}: "{v}"')
    else:
        print("From: " + ", ".join(f"{m['id']} ({m['role']})" for m in chosen) + f"   mode: {a.mode}\n")
        for k, v in colors.items():
            print(f"  {k:10} {v}")
        print("\nContrast: " + "  ".join(f"{k} {v}" for k, v in checks.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
