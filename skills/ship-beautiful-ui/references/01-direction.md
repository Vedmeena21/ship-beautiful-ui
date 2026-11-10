# Step 1: Direction

A direction is three decisions: **palette**, **type**, **layout**, plus two or three principles that tie them to the subject. Make all three for this subject. Never for "a website".

## Route A (default): derive from the subject's world

Templates make products look alike because many products draw from the same short list. The subject's own world doesn't repeat: a bakery has crust, flour and espresso; a darkroom has safelight red, contact-sheet black and grey cards. Start there.

1. Take the five nouns from the brief. Prefer things with a real color: materials, food, places, tools, signage.
2. Run:
   ```bash
   python3 scripts/derive.py --words "safelight, contact sheet, grey card, film edge"
   python3 scripts/derive.py --words "..." --mode dark      # for products used at night
   python3 scripts/derive.py --suggest food                # materials that fit a kind
   ```
   It matches words to `data/materials.json`, assigns roles (base, ink, accent, accent-2), builds surface, muted and line, and pushes lightness until every pair passes contrast.
3. If a word doesn't match, use a nearer concrete noun, or pick material ids directly with `--materials`.
4. Choose **type** from `data/type-pairings.json` by mood and `fits`. The note on each pairing says how to use it.
5. Choose **layout** from `data/layouts.json` by the screen's job, not by habit.

## Route B: deal from the library

Use when the subject has no strong visual world (an internal tool, a generic utility) or the user wants options quickly.

```bash
python3 scripts/direction.py --list                         # product kinds
python3 scripts/direction.py --kind fintech --brief "invoicing for photographers"
python3 scripts/direction.py --kind fintech --brief "..." --mode light --options 3
```

It deals three options, each a palette from 60, a pairing from 40 and a layout from 20, matched to the kind. The same brief always deals the same options, so "option 2" means the same thing to you and the user. Show all three and let the user choose.

## Route C: an existing brand

The brand is the direction. Extract its colors, type and spacing from the site or brand guide, then fill the gaps (muted, line, states) and check contrast in step 2. Do not "improve" a brand into something else unless asked.

## Check the plan before building

Write the plan down:

- **Palette:** 4-8 named colors with roles.
- **Type:** families and roles (display, body, mono if needed).
- **Layout:** one sentence and the wireframe.
- **Principles:** 2-3 sentences on what makes this belong to this subject.

Then compare it with the visual defaults (V1-V12) in `references/anti-patterns.md`. If part of the plan matches one and the brief did not ask for it, revise that part and say what changed in one line. Matching a look the user asked for is fine: their words win.

Commit to the direction. Do not reopen it during the build unless the user asks.
