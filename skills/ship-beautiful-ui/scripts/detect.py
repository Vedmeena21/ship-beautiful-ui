#!/usr/bin/env python3
"""Scan front-end source for patterns that make UI look AI-generated, plus quality-floor gaps.

Rules are numbered (SBU001...) and described in references/anti-patterns.md.
It reads files only; it does not render pages.

Usage:
  python3 scripts/detect.py src/
  python3 scripts/detect.py index.html styles.css --json
  python3 scripts/detect.py . --list-rules

Exit code 1 when any finding has severity "error". Standard library only.
"""
import argparse
import colorsys
import json
import os
import re
import sys
from collections import Counter

EXTS = {".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro", ".mdx"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", ".svelte-kit", "coverage", "vendor", ".turbo", "out"}

RULES = {
    "SBU001": ("warning", "One generic sans for everything", "Only Inter (or the system stack) is used. Pair a display face with a body face that fit the subject."),
    "SBU002": ("warning", "Purple-to-blue gradient", "Purple/violet to blue/indigo gradients are the most common AI decoration. Use a flat accent from DESIGN.md."),
    "SBU003": ("info", "Gradient text", "background-clip:text gradients on headings read as templated. Let type size and weight do the work."),
    "SBU004": ("warning", "Same soft shadow everywhere", "The same low-opacity black shadow appears on many elements. Use shadow only for things that float."),
    "SBU005": ("warning", "All-caps tracked eyebrows", "Many uppercase, letter-spaced labels. Keep labels only where they carry information, in sentence case."),
    "SBU006": ("info", "Numbered markers", "01 / 02 / 03 markers. Use them only for real sequences."),
    "SBU007": ("error", "Lorem ipsum", "Placeholder Latin. Write realistic copy in the subject's vocabulary."),
    "SBU008": ("warning", "Filler marketing copy", "Phrases like 'unlock the power', 'seamless', 'revolutionize'. Say what the product does, plainly."),
    "SBU009": ("warning", "Animating layout properties", "Transitions on width/height/top/left/margin cause layout work. Animate transform and opacity."),
    "SBU010": ("error", "Motion without reduced-motion support", "Animations or transitions exist but nothing handles prefers-reduced-motion."),
    "SBU011": ("error", "Focus outline removed", "outline: none/0 without a :focus-visible style. Keyboard users lose their place."),
    "SBU012": ("warning", "Raw colors in components", "Many hard-coded hex colors in component files. Use DESIGN.md tokens (CSS variables or theme)."),
    "SBU013": ("warning", "Cream page + terracotta accent", "The most common 'tasteful' AI default. Fine if the brief asked for it; otherwise choose for the subject."),
    "SBU014": ("warning", "Near-black + neon accent", "Near-black background with an acid green or neon accent: a common AI default."),
    "SBU015": ("info", "One radius on everything", "Almost every rounded corner uses the same value. Vary radius by hierarchy."),
    "SBU016": ("info", "Arrow appended to every link", "'→' added to many links or buttons. Let the label say what happens."),
    "SBU017": ("info", "Middle-dot meta strings", "Many 'A · B · C' strings. Use structure (lists, columns) when the items matter."),
    "SBU018": ("warning", "Fade-up on everything", "Many scroll-reveal / fade-in-up animations. Keep one ambient motion moment per screen."),
    "SBU019": ("error", "Image without alt", "<img> without an alt attribute. Describe it, or use alt=\"\" if decorative."),
    "SBU020": ("warning", "Tiny text", "font-size below 12px. Body text should be 16px or larger; labels at least 12px."),
    "SBU021": ("warning", "Emoji as icons", "Emoji in headings or buttons stand in for real icons. Use one consistent icon set or none."),
    "SBU022": ("warning", "Skipped heading level", "Heading levels jump (for example h1 to h3). Screen readers use them to navigate."),
    "SBU023": ("warning", "More than one h1", "A page should have one h1 that says what it is."),
    "SBU024": ("error", "Icon button without a name", "A <button> with no text and no aria-label. Give it a name."),
    "SBU025": ("error", "Input without a label", "Form fields need a <label for> or aria-label; placeholder text is not a label."),
    "SBU026": ("warning", "Generic link text", "'Click here', 'learn more', 'read more' say nothing out of context. Name the destination."),
    "SBU027": ("info", "Justified text", "text-align: justify makes uneven word gaps on the web. Left-align body text."),
    "SBU028": ("warning", "Tight body line height", "Body line-height under 1.3 is hard to read. Use 1.4-1.6 for body text."),
    "SBU029": ("warning", "Placeholder people and companies", "John Doe, Jane Doe, Acme Inc. Use real names with permission, or none."),
    "SBU030": ("info", "Unsourced big numbers", "'10x', '99.9%', '10,000+ users' need a source. Remove numbers you can't back up."),
    "SBU031": ("error", "Zoom disabled", "user-scalable=no or maximum-scale=1 blocks pinch zoom for low-vision users."),
    "SBU032": ("warning", "Autoplaying media", "Video or audio that autoplays with sound, or without controls. Mute it and give controls."),
    "SBU033": ("info", "Lots of !important", "Many !important rules usually mean fighting specificity. Fix the selectors instead."),
    "SBU034": ("info", "Extreme z-index", "z-index of 9999 and up. Define a small z-index scale in DESIGN.md."),
    "SBU035": ("info", "Glass on everything", "backdrop-filter blur on many elements. Frosted glass works for one layer, not every card."),
    "SBU036": ("warning", "Framework default palette", "Many default framework color classes (bg-indigo-500, text-blue-600). Map colors to DESIGN.md tokens."),
    "SBU037": ("info", "Icon tile above every heading", "A tinted rounded square with an icon above each heading is template chrome. Use icons only where they help scanning."),
    "SBU038": ("warning", "Emoji bullets", "Rows of emoji used as bullets (rocket, sparkles, check). Use plain lists or real icons."),
    "SBU039": ("warning", "Content only on hover", "Content hidden until :hover is unreachable by keyboard and touch. Add :focus-within or show it."),
    "SBU040": ("error", "Missing page language", "<html> without a lang attribute. Screen readers need it to pronounce text."),
}

FILLER = ["unlock the power", "seamless", "revolutionize", "revolutionise", "supercharge", "elevate your", "next-level",
          "cutting-edge", "game-changer", "game changer", "effortlessly", "harness the power", "in today's fast-paced",
          "take your .{0,20} to the next level", "unleash"]


def hue_of(hexc):
    h = hexc.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    hh, l, s = colorsys.rgb_to_hls(r, g, b)
    return hh * 360, l, s


def is_purple(hexc):
    h, l, s = hue_of(hexc)
    return 255 <= h <= 300 and s > 0.35 and 0.25 < l < 0.8


def is_blue(hexc):
    h, l, s = hue_of(hexc)
    return 195 <= h < 255 and s > 0.35 and 0.25 < l < 0.8


def gather(paths):
    files = []
    for p in paths:
        if os.path.isfile(p):
            files.append(p)
            continue
        for root, dirs, names in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            for n in names:
                if os.path.splitext(n)[1].lower() in EXTS:
                    files.append(os.path.join(root, n))
    return sorted(set(files))


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def scan(files):
    findings = []
    texts = {}
    for f in files:
        try:
            with open(f, encoding="utf-8", errors="ignore") as fh:
                texts[f] = fh.read()
        except OSError:
            continue
    allt = "\n".join(texts.values())
    low_all = allt.lower()

    def add(rule, f, line, detail):
        findings.append({"rule": rule, "severity": RULES[rule][0], "title": RULES[rule][1], "file": f, "line": line, "detail": detail})

    # project-wide checks
    fams = [m.group(1).lower() for m in re.finditer(r"font-family\s*:\s*([^;}\n]+)", allt)]
    fams += [m.group(1).lower() for m in re.finditer(r"fontFamily\s*[:=]\s*['\"`]?([^'\"`;\n}]+)", allt)]
    fams += ["inter" for _ in re.finditer(r"\bfont-sans\b", allt)] if "inter" in low_all else []
    if fams:
        firsts = {re.split(r"[,'\"]", x.strip().strip("'\""))[0].strip().strip("'\"") for x in fams if x.strip()}
        firsts.discard("")
        generic = {"inter", "-apple-system", "system-ui", "ui-sans-serif", "sans-serif", "helvetica", "arial", "inherit", "var(--font-sans)"}
        mono = {"ui-monospace", "monospace", "menlo", "sfmono-regular", "consolas", "jetbrains mono"}
        nonmono = {x for x in firsts if x not in mono}
        if nonmono and nonmono <= generic and "inter" in nonmono:
            add("SBU001", "(project)", 0, "font families found: " + ", ".join(sorted(nonmono)))

    motion = re.search(r"@keyframes|animation\s*:|transition\s*:|\banimate-|\btransition-|framer-motion|motion\.|gsap|data-aos", allt)
    if motion and "prefers-reduced-motion" not in low_all and "usereducedmotion" not in low_all and "motion-reduce" not in low_all:
        add("SBU010", "(project)", 0, "motion found, no prefers-reduced-motion / motion-reduce handling")

    for f, t in texts.items():
        low = t.lower()
        # SBU002 purple-blue gradients (CSS) and Tailwind gradient classes
        for m in re.finditer(r"(linear|radial|conic)-gradient\(([^;]*?)\)\s*[;\"'}]", t, re.S):
            hexes = re.findall(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", m.group(2))
            if any(is_purple(h) for h in hexes) and any(is_blue(h) for h in hexes):
                add("SBU002", f, line_of(t, m.start()), m.group(0)[:80])
        for m in re.finditer(r"from-(purple|violet|fuchsia|indigo)-\d{3}[^\"'`]*?to-(blue|indigo|cyan|sky|purple|violet)-\d{3}|from-(blue|indigo|cyan)-\d{3}[^\"'`]*?to-(purple|violet|fuchsia)-\d{3}", t):
            add("SBU002", f, line_of(t, m.start()), m.group(0)[:80])
        for m in re.finditer(r"background-clip\s*:\s*text|bg-clip-text", t):
            add("SBU003", f, line_of(t, m.start()), "gradient text")
        # SBU004 same soft shadow
        shadows = re.findall(r"box-shadow\s*:\s*([^;}\n]+)", t)
        soft = [s for s in shadows if re.search(r"rgba\(\s*0\s*,\s*0\s*,\s*0\s*,\s*0?\.(0[5-9]|1|12|15)\s*\)", s)]
        tw = re.findall(r"\bshadow-(sm|md|lg)\b", t)
        if len(soft) >= 3 or len(tw) >= 6:
            add("SBU004", f, 0, f"{len(soft)} soft black shadows, {len(tw)} shadow utility classes")
        # SBU005 eyebrows
        caps = len(re.findall(r"text-transform\s*:\s*uppercase[^}]*letter-spacing\s*:\s*0?\.(0[8-9]|[1-9])", t, re.S))
        caps += len(re.findall(r"\buppercase\b[^\"'`]*\btracking-(wide|wider|widest)\b|\btracking-(wider|widest)\b[^\"'`]*\buppercase\b", t))
        if caps >= 3:
            add("SBU005", f, 0, f"{caps} uppercase tracked labels")
        nums = re.findall(r">\s*0[1-9]\s*[<.]", t)
        if len(nums) >= 3:
            add("SBU006", f, 0, f"{len(nums)} numbered markers")
        for m in re.finditer(r"lorem ipsum|dolor sit amet", low):
            add("SBU007", f, line_of(t, m.start()), "lorem ipsum")
        for pat in FILLER:
            for m in re.finditer(pat, low):
                add("SBU008", f, line_of(t, m.start()), t[m.start():m.end()])
        for m in re.finditer(r"transition(-property)?\s*:\s*([^;}\n]+)", t):
            props = m.group(2).lower()
            if re.search(r"\b(width|height|top|left|right|bottom|margin|padding)\b", props):
                add("SBU009", f, line_of(t, m.start()), m.group(0)[:80])
        for m in re.finditer(r"transition-\[(width|height|top|left|margin|padding)", t):
            add("SBU009", f, line_of(t, m.start()), m.group(0))
        if re.search(r"outline\s*:\s*(none|0)\b|\boutline-none\b", t) and not re.search(r":focus-visible|focus-visible:", allt):
            m = re.search(r"outline\s*:\s*(none|0)\b|\boutline-none\b", t)
            add("SBU011", f, line_of(t, m.start()), m.group(0))
        if os.path.splitext(f)[1].lower() in {".jsx", ".tsx", ".vue", ".svelte", ".astro"}:
            hexes = set(h.lower() for h in re.findall(r"#[0-9a-fA-F]{6}\b", t))
            if len(hexes) >= 5:
                add("SBU012", f, 0, f"{len(hexes)} distinct hard-coded hex colors")
        cream = re.search(r"#(f[4-9a-f]f[0-9a-f]e[0-9a-f]|faf[4-9a-f]f[0-9a-f])\b", low) or re.search(r"#f4f1ea|#f5f0e8|#faf7f2|#f7f3ec", low)
        terracotta = re.search(r"#d9775[0-9a-f]|#c96442|#cc785c|#d97757|#c4613f|#e07a5f", low)
        if cream and terracotta:
            add("SBU013", f, line_of(t, terracotta.start()), "cream background with terracotta accent")
        nearblack = re.search(r"#(0b0b0b|0a0a0a|111111|111|0d0d0d|0c0c0c)\b", low)
        neon = re.search(r"#(39ff14|a3e635|bef264|00ff9[0-9a-f]|ccff00|d4ff00|b6ff00|84cc16)\b", low)
        if nearblack and neon:
            add("SBU014", f, line_of(t, neon.start()), "near-black with neon accent")
        radii = re.findall(r"border-radius\s*:\s*([^;}\n]+)", t) + re.findall(r"\brounded-(?:[a-z]{1,2}-)?(none|sm|md|lg|xl|2xl|3xl|full)\b", t)
        if len(radii) >= 8:
            top, c = Counter(r.strip() for r in radii).most_common(1)[0]
            if c / len(radii) >= 0.8:
                add("SBU015", f, 0, f"{c} of {len(radii)} radii are '{top}'")
        arrows = re.findall(r"(→|&rarr;|-&gt;)\s*</(a|button)>|(→|&rarr;)\s*['\"`]?\s*\}?\s*</(a|button|Link|Button)>", t)
        if len(arrows) >= 3:
            add("SBU016", f, 0, f"{len(arrows)} links or buttons end with an arrow")
        dots = re.findall(r"\w[^<>\n]{0,40} · [^<>\n]{0,40} · ", t)
        if len(dots) >= 3:
            add("SBU017", f, 0, f"{len(dots)} middle-dot meta strings")
        fades = re.findall(r"fade-?in-?up|fadeinup|slide-?up|data-aos=|reveal-on-scroll|animate-fade", low)
        if len(fades) >= 4:
            add("SBU018", f, 0, f"{len(fades)} scroll-reveal / fade-up uses")
        for m in re.finditer(r"<img\b(?![^>]*\balt\s*=)[^>]*>", t, re.I):
            add("SBU019", f, line_of(t, m.start()), m.group(0)[:70])
        for m in re.finditer(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", t):
            if float(m.group(1)) < 12:
                add("SBU020", f, line_of(t, m.start()), m.group(0))
        for m in re.finditer(r"text-\[(\d+(?:\.\d+)?)px\]", t):
            if float(m.group(1)) < 12:
                add("SBU020", f, line_of(t, m.start()), m.group(0))
        # --- rules 021-040 ---
        is_markup = os.path.splitext(f)[1].lower() in {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro", ".mdx"}
        EMOJI = r"[\U0001F300-\U0001FAFF\u2600-\u27BF]"
        if is_markup:
            em = re.findall(r"<(h[1-3]|button)\b[^>]*>[^<]*" + EMOJI, t)
            if len(em) >= 3:
                add("SBU021", f, 0, f"{len(em)} headings or buttons with emoji")
            levels = [int(x) for x in re.findall(r"<h([1-6])\b", t, re.I)]
            for a_, b_ in zip(levels, levels[1:]):
                if b_ > a_ + 1:
                    add("SBU022", f, 0, f"h{a_} followed by h{b_}")
                    break
            if levels.count(1) > 1:
                add("SBU023", f, 0, f"{levels.count(1)} h1 elements")
            for m in re.finditer(r"<button\b([^>]*)>(.*?)</button>", t, re.S | re.I):
                attrs, inner = m.group(1), m.group(2)
                text = re.sub(r"<[^>]+>", "", inner).strip()
                if not text and not re.search(r"aria-label(ledby)?\s*=|title\s*=", attrs):
                    add("SBU024", f, line_of(t, m.start()), m.group(0)[:70])
            labels_for = set(re.findall(r"<label\b[^>]*\b(?:for|htmlFor)\s*=\s*[\"']([^\"']+)", t))
            for m in re.finditer(r"<(input|select|textarea)\b([^>]*)>", t, re.I):
                attrs = m.group(2)
                if re.search(r"type\s*=\s*[\"'](hidden|submit|button|reset|image)", attrs):
                    continue
                idm = re.search(r"\bid\s*=\s*[\"']([^\"']+)", attrs)
                wrapped = re.search(r"<label\b[^>]*>[^<]*$", t[max(0, m.start() - 120):m.start()])
                if not re.search(r"aria-label(ledby)?\s*=", attrs) and not (idm and idm.group(1) in labels_for) and not wrapped:
                    add("SBU025", f, line_of(t, m.start()), m.group(0)[:70])
            gen = re.findall(r">\s*(click here|learn more|read more|here)\s*<", low)
            if len(gen) >= 2:
                add("SBU026", f, 0, f"{len(gen)} generic link labels")
            ppl = re.findall(r"john doe|jane doe|acme (inc|corp)|lorem corp|jane smith", low)
            if ppl:
                add("SBU029", f, 0, f"{len(ppl)} placeholder names")
            stats = re.findall(r"\b\d{1,3}(,\d{3})+\+\s*(users|customers|teams|developers)|\b10x\b|99\.9%", low)
            if len(stats) >= 2:
                add("SBU030", f, 0, f"{len(stats)} big claims without a visible source")
            for m in re.finditer(r"user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1(\.0)?\b", low):
                add("SBU031", f, line_of(t, m.start()), m.group(0))
            for m in re.finditer(r"<(video|audio)\b([^>]*)>", t, re.I):
                attrs = m.group(2).lower()
                if "autoplay" in attrs and ("muted" not in attrs or "controls" not in attrs and m.group(1).lower() == "audio"):
                    add("SBU032", f, line_of(t, m.start()), m.group(0)[:70])
            tw_default = re.findall(r"\b(bg|text|border|from|to|ring)-(indigo|blue|purple|violet|slate|gray|zinc)-(50|100|200|300|400|500|600|700|800|900)\b", t)
            if len(tw_default) >= 8:
                add("SBU036", f, 0, f"{len(tw_default)} default framework color classes")
            tiles = re.findall(r"rounded-(lg|xl|2xl)[^\"'`]*bg-\w+-(50|100)[^\"'`]*p-(2|3)|bg-\w+-(50|100)[^\"'`]*rounded-(lg|xl|2xl)[^\"'`]*p-(2|3)", t)
            if len(tiles) >= 3:
                add("SBU037", f, 0, f"{len(tiles)} icon tiles")
            eb = re.findall(r"<li\b[^>]*>\s*(✅|🚀|✨|🔥|💡|👉|⚡|🎯)", t)
            if len(eb) >= 3:
                add("SBU038", f, 0, f"{len(eb)} emoji bullets")
            if re.search(r"<html\b(?![^>]*\blang\s*=)[^>]*>", t, re.I):
                add("SBU040", f, 0, "<html> has no lang")
        for m in re.finditer(r"text-align\s*:\s*justify|\btext-justify\b", t):
            add("SBU027", f, line_of(t, m.start()), m.group(0))
        for m in re.finditer(r"(?:^|[}\s])(body|p)\s*\{[^}]*line-height\s*:\s*(1(?:\.[0-2]\d*)?)\s*[;}]", t):
            add("SBU028", f, line_of(t, m.start()), f"{m.group(1)} line-height {m.group(2)}")
        imp = t.count("!important")
        if imp >= 10:
            add("SBU033", f, 0, f"{imp} !important")
        for m in re.finditer(r"z-index\s*:\s*(\d{4,})|\bz-\[(\d{4,})\]", t):
            if int(m.group(1) or m.group(2)) >= 9999:
                add("SBU034", f, line_of(t, m.start()), m.group(0))
        glass = len(re.findall(r"backdrop-filter\s*:\s*blur|\bbackdrop-blur", t))
        if glass >= 4:
            add("SBU035", f, 0, f"{glass} blurred glass layers")
        hov = re.findall(r":hover\s*[>+~ ]?\s*[^{]*\{[^}]*(opacity\s*:\s*1|visibility\s*:\s*visible|display\s*:\s*block)", t)
        if hov and ":focus-within" not in t and ":focus-visible" not in t and "focus-within:" not in t:
            add("SBU039", f, 0, f"{len(hov)} hover-only reveals")
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", default=["."])
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--list-rules", action="store_true")
    a = ap.parse_args()
    if a.list_rules:
        for k, (sev, title, fix) in RULES.items():
            print(f"{k}  {sev:7}  {title}\n          {fix}")
        return 0
    files = gather(a.paths)
    findings = scan(files)
    summary = {s: sum(1 for x in findings if x["severity"] == s) for s in ("error", "warning", "info")}
    if a.json:
        print(json.dumps({"files": len(files), "findings": findings, "summary": summary}, indent=2))
    else:
        for x in findings:
            loc = f"{x['file']}:{x['line']}" if x["line"] else x["file"]
            print(f"{x['rule']} {x['severity']:7} {x['title']}\n        {loc}  {x['detail']}\n        fix: {RULES[x['rule']][2]}")
        print(f"\nScanned {len(files)} files: {summary['error']} errors, {summary['warning']} warnings, {summary['info']} info")
    return 1 if summary["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
