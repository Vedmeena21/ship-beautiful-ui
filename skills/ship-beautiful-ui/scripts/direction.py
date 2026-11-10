#!/usr/bin/env python3
"""Deal design directions for a product kind, and optionally write a DESIGN.md draft.

Each direction = one palette + one type pairing + one layout pattern, taken from
data/ and matched to the product kind. The same brief always deals the same
options, so the agent and the user can talk about "option 2" reliably.

Usage:
  python3 scripts/direction.py --list
  python3 scripts/direction.py --kind fintech --brief "invoicing for photographers"
  python3 scripts/direction.py --kind food --brief "..." --mode light --options 3
  python3 scripts/direction.py --kind food --brief "..." --choose 2 --write DESIGN.md --name "Crumb"

Standard library only.
"""
import argparse
import hashlib
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
TEMPLATE = os.path.join(HERE, "..", "templates", "DESIGN.md")


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return json.load(f)


def kinds(palettes, pairings, layouts):
    ks = set()
    for coll in (palettes, pairings, layouts):
        for item in coll:
            ks.update(item["fits"])
    return sorted(ks)


def ranked(items, kind, rng):
    """Items that fit the kind first (shuffled), then the rest (shuffled)."""
    fit = [i for i in items if kind in i["fits"]]
    rest = [i for i in items if kind not in i["fits"]]
    rng.shuffle(fit)
    rng.shuffle(rest)
    return fit + rest


def deal(kind, brief, mode, n):
    palettes = load("palettes.json")["palettes"]
    pairings = load("type-pairings.json")["pairings"]
    layouts = load("layouts.json")["layouts"]
    if mode in ("light", "dark"):
        palettes = [p for p in palettes if p["mode"] == mode]
    seed = int(hashlib.sha256(f"{kind}|{brief}|{mode}".encode()).hexdigest()[:12], 16)
    rng = random.Random(seed)
    ps, ts, ls = ranked(palettes, kind, rng), ranked(pairings, kind, rng), ranked(layouts, kind, rng)
    options = []
    for i in range(n):
        options.append({
            "option": i + 1,
            "palette": ps[i % len(ps)],
            "type": ts[i % len(ts)],
            "layout": ls[i % len(ls)],
        })
    return options


def describe(opt):
    p, t, l = opt["palette"], opt["type"], opt["layout"]
    c = p["colors"]
    lines = [
        f"OPTION {opt['option']}",
        f"  Palette  {p['name']} ({p['mode']}): {p['mood']}",
        "           " + "  ".join(f"{k} {v}" for k, v in c.items()),
        f"  Type     {t['display']} / {t['body']}" + (f" / {t['mono']}" if t.get("mono") else "") + f": {t['mood']}",
        f"           {t['note']}",
        f"  Layout   {l['name']}: {l['summary']}",
    ]
    lines += ["           " + row for row in l["wireframe"]]
    return "\n".join(lines)


TYPE_SCALE = {
    "display": ("display", "56px", 700, "1.05", "-0.02em"),
    "h2": ("display", "32px", 650, "1.15", "-0.01em"),
    "body": ("body", "17px", 400, "1.55", None),
    "label": ("body", "14px", 600, "1.3", None),
}


def design_md(opt, name, description):
    p, t, l = opt["palette"], opt["type"], opt["layout"]
    c = p["colors"]
    out = ["---", "version: alpha", f"name: {name}", f"description: {description}", "colors:"]
    for k, v in c.items():
        out.append(f'  {k}: "{v}"')
    out.append("typography:")
    fams = {"display": t["display"], "body": t["body"]}
    for tok, (fam, size, weight, lh, ls) in TYPE_SCALE.items():
        out += [f"  {tok}:", f"    fontFamily: {fams[fam]}", f"    fontSize: {size}", f"    fontWeight: {weight}", f"    lineHeight: {lh}"]
        if ls:
            out.append(f"    letterSpacing: {ls}")
    if t.get("mono"):
        out += ["  mono:", f"    fontFamily: {t['mono']}", "    fontSize: 14px", "    fontWeight: 400", "    lineHeight: 1.5"]
    out += ["rounded:", "  sm: 6px", "  md: 12px", "  lg: 20px",
            "spacing:", "  xs: 4px", "  sm: 8px", "  md: 16px", "  lg: 32px", "  xl: 64px",
            "components:",
            "  button-primary:", '    backgroundColor: "{colors.accent}"', '    textColor: "{colors.on-accent}"',
            '    typography: "{typography.label}"', '    rounded: "{rounded.sm}"', "    padding: 12px",
            "  button-primary-hover:", '    backgroundColor: "{colors.ink}"', '    textColor: "{colors.base}"',
            "  surface:", '    backgroundColor: "{colors.surface}"', '    textColor: "{colors.ink}"', '    rounded: "{rounded.md}"', "    padding: 24px",
            "---", ""]
    out += [
        "## Overview", "",
        "Subject: ...", "Audience: ...", "Job: ...", "World: five nouns from the subject's world.", "",
        f"Direction: {p['name']} palette ({p['mood']}), {t['display']} with {t['body']} ({t['mood']}), {l['name'].lower()} layout.", "",
        "## Colors", "",
    ]
    roles = {"base": "page background", "surface": "raised areas only", "ink": "headings and body text",
             "muted": "secondary text, never on colored backgrounds", "line": "dividers and input borders",
             "accent": "the one interactive color: primary actions and links", "on-accent": "text on accent",
             "accent-2": "sparingly, for one secondary highlight"}
    for k, v in c.items():
        out.append(f"- **{k} ({v}):** {roles.get(k, '')}")
    out += ["", "## Typography", "", f"{t['display']} for display and h2 only. {t['body']} for everything else. {t['note']}",
            "Sentence case. Body never below 16px. Line length under 80 characters.", "",
            "## Layout", "", f"{l['name']}: {l['summary']}", "", "```"] + l["wireframe"] + ["```", "",
            "## Elevation & Depth", "", "Say which elements float and how (shadow, border or tone). Most things should not float.", "",
            "## Shapes", "", "Small radius for controls, medium for containers, large only for the one hero surface.", "",
            "## Components", "", "Describe the primary button, inputs, navigation and states (hover, focus, disabled, loading, error).", "",
            "## Do's and Don'ts", "",
            "- Do: spend boldness on one element per screen.",
            "- Do: use only tokens from this file in code.",
            "- Don't: list the generic defaults you rejected here, so nobody drifts back to them.",
            "- Don't: add motion the user did not trigger, beyond one moment per screen.", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kind", help="product kind, see --list")
    ap.add_argument("--brief", default="", help="one-line brief; seeds the deal")
    ap.add_argument("--mode", default="any", choices=["any", "light", "dark"])
    ap.add_argument("--options", type=int, default=3)
    ap.add_argument("--choose", type=int, help="option number to use with --write")
    ap.add_argument("--write", help="write a DESIGN.md draft for the chosen option to this path")
    ap.add_argument("--name", default="Untitled product")
    ap.add_argument("--description", default="Replace with one line on what this is and who it is for.")
    ap.add_argument("--json", action="store_true", help="print options as JSON")
    ap.add_argument("--list", action="store_true", help="list product kinds")
    a = ap.parse_args()

    if a.list:
        print("\n".join(kinds(load("palettes.json")["palettes"], load("type-pairings.json")["pairings"], load("layouts.json")["layouts"])))
        return 0
    if not a.kind:
        ap.error("--kind is required (see --list)")
    opts = deal(a.kind, a.brief, a.mode, max(1, a.options))
    if a.write:
        n = a.choose or 1
        if not 1 <= n <= len(opts):
            ap.error(f"--choose must be between 1 and {len(opts)}")
        if os.path.exists(a.write):
            print(f"{a.write} already exists; not overwriting. Remove it or pick another path.", file=sys.stderr)
            return 2
        with open(a.write, "w", encoding="utf-8") as f:
            f.write(design_md(opts[n - 1], a.name, a.description))
        print(f"Wrote {a.write} from option {n}. Fill in Overview, then run scripts/lint_design.py {a.write}")
        return 0
    if a.json:
        print(json.dumps(opts, indent=2))
    else:
        print(f"Directions for '{a.kind}'" + (f" ({a.mode})" if a.mode != "any" else "") + "\n")
        print("\n\n".join(describe(o) for o in opts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
