# Step 2: Lock the direction in DESIGN.md

`DESIGN.md` is a plain markdown file at the project root that tells any coding agent how the UI should look. Once it exists, it outranks everything except the user. It uses the open DESIGN.md format, so other tools can read it too.

It has two layers:

1. **YAML tokens** between `---` fences at the top: exact values.
2. **Markdown sections**: why the values are what they are, and how to use them.

## Token schema

```yaml
---
version: alpha            # optional
name: <string>
description: <string>     # optional
colors:
  <name>: <any CSS color>        # "#1A1C1E", "oklch(62% 0.18 250)"
typography:
  <name>:
    fontFamily: <string>
    fontSize: <dimension>        # 48px, 3rem
    fontWeight: <number>
    lineHeight: <number|dimension>
    letterSpacing: <dimension>   # -0.02em
rounded:
  <level>: <dimension>
spacing:
  <level>: <dimension|number>
components:
  <component-name>:
    backgroundColor: "{colors.accent}"   # token reference
    textColor: "{colors.on-accent}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: 12px
---
```

Component properties: `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`. Variants are separate entries (`button-primary`, `button-primary-hover`).

## Sections, in this order

1. Overview
2. Colors
3. Typography
4. Layout
5. Elevation & Depth
6. Shapes
7. Components
8. Do's and Don'ts

Put the brief (subject, audience, job, world nouns) in **Overview**. Put the defaults you rejected in step 1 into **Do's and Don'ts**, so later steps can't drift back to them. Add the motion timing tokens from `04-motion.md` under Components or Do's and Don'ts.

## Getting a draft

- From Route B: `python3 scripts/direction.py --kind <kind> --brief "<brief>" --choose <n> --write DESIGN.md --name "<Product>"`
- From Route A: start from `templates/DESIGN.md` and paste the `colors:` block from `python3 scripts/derive.py --words "..." --yaml`.
- From a brand: start from the template and fill in the brand's values.

## Check it

```bash
python3 scripts/lint_design.py DESIGN.md
python3 scripts/lint_design.py DESIGN.md --json
```

It reports missing structure, sections out of order or duplicated, invalid colors, broken token references, unknown component properties, and contrast for component text/background pairs and the core pairs (ink/base, muted/base, muted/surface, on-accent/accent, accent/base). Fix every error before building.

## Rules for the rest of the pipeline

- Components use token references, never raw values.
- A new color, size or font needed during build goes into `DESIGN.md` first, then into code.
- If code and `DESIGN.md` disagree at review time, one of them gets fixed. They never ship different.
