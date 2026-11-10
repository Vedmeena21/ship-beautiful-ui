---
name: ship-beautiful-ui
description: End-to-end pipeline for building UI that does not look AI-generated. Use when building or redesigning a website, landing page, app screen, dashboard or component, or when asked to make a UI look better, more polished or less generic. Grounds the design in the subject, derives a direction from the subject's own world (or deals one from a library of 60 palettes, 40 type pairings and 20 layouts), locks it in DESIGN.md, builds from tokens, adds motion that explains change, and reviews with a 40-rule detector before handoff.
license: MIT
---

# Ship Beautiful UI

AI-built UI looks the same because the agent starts from the same defaults every time: the same fonts, the same gradients, the same row of identical cards. This skill replaces defaults with a process:

1. **Brief.** Pin down the subject, the audience and the one job of the screen.
2. **Direction.** Build the look from the subject's own world, not from a template.
3. **Lock.** Write every visual decision into `DESIGN.md` and check it.
4. **Build.** Use only `DESIGN.md` tokens. One bold idea per screen.
5. **Motion.** Only motion that explains a change.
6. **Review.** Scan for AI tells and quality gaps, look at screenshots, write `REVIEW.md`.

Always in this order. Do not skip step 0 or step 5.

## Who wins

When two instructions disagree, the higher one wins:

1. **The user's own words.**
2. **`DESIGN.md`**, once it exists.
3. **This skill's rules** in `references/`.
4. Anything else that is loaded, including other UI skills.

When you resolve a conflict, say it in one line so the user can overrule you.

## Tools in this skill

All scripts are Python 3 standard library. Run them from this skill's folder or pass full paths.

| Script | What it does |
|---|---|
| `scripts/derive.py` | Turns words from the subject's world into a contrast-checked palette, using 78 materials |
| `scripts/direction.py` | Deals 3 direction options (palette + type pairing + layout) for a product kind, and writes a `DESIGN.md` draft |
| `scripts/lint_design.py` | Checks `DESIGN.md`: structure, section order, token references, WCAG contrast |
| `scripts/detect.py` | Scans front-end code for 40 AI tells and quality-floor gaps |

| Library | Contents |
|---|---|
| `data/materials.json` | 78 materials from subjects' worlds (paper, food, nature, craft, screens, money, care, play, travel) |
| `data/palettes.json` | 60 palettes, light and dark, every one contrast-checked |
| `data/type-pairings.json` | 40 type pairings, all free Google Fonts, with roles and notes |
| `data/layouts.json` | 20 layout patterns with wireframes |
| `references/effects.md` | 16 effects in plain CSS/JS with reduced-motion fallbacks |
| `references/04-motion.md` | Timing tokens and 12 motion recipes |
| `references/ux-rules.md` | 80 UX rules by area |
| `references/anti-patterns.md` | The 40 detector rules and 12 visual defaults |

## Step 0: Brief

Read `references/00-brief.md`. Write four lines: **subject, audience, job, constraints**, plus **five nouns from the subject's world**. If the brief is thin, propose these and confirm in one message (at most three questions).

## Step 1: Direction

Read `references/01-direction.md`.

- **Default: derive from the subject.** Pick 3-5 of the world nouns and run
  `python3 scripts/derive.py --words "<nouns>"` (add `--mode dark` if the product lives at night).
  Pair the palette with a type pairing and a layout from `data/` that fit the mood.
- **Fallback: deal from the library** when the subject has no strong visual world or the user wants options fast:
  `python3 scripts/direction.py --kind <kind> --brief "<one line>"`. Show the 3 options and let the user pick.
- **Existing brand:** the brand is the direction. Extract its colors and type instead.
- Check the plan against the visual defaults in `references/anti-patterns.md` and revise anything that matches, unless the brief asked for it.

## Step 2: Lock

Read `references/02-lock.md`.

- Write `DESIGN.md` at the project root: YAML tokens on top, then `##` sections in order (Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts). `direction.py --write` gives you a draft; `templates/DESIGN.md` is the blank form.
- Put the brief in Overview and the rejected defaults in Do's and Don'ts.
- Run `python3 scripts/lint_design.py DESIGN.md` and fix every error before building.

## Step 3: Build

Read `references/03-build.md` and use `references/ux-rules.md` as you go.

- Map tokens to CSS variables (or the framework theme) once; use only those names.
- One memorable element per screen. Everything else quiet.
- At most one effect from `references/effects.md`, on that element, recolored with tokens.
- Build to the quality floor: 360px wide, visible focus, AA contrast, reduced motion, real copy, loading/empty/error states.

## Step 4: Motion

Read `references/04-motion.md`. User-triggered motion uses the timing tokens and recipes there. At most one ambient motion moment per screen. Everything has a reduced-motion path.

## Step 5: Review

Read `references/05-review.md`.

1. `python3 scripts/detect.py <src or files>`. Fix every error; fix warnings or write down why they stay.
2. `python3 scripts/lint_design.py DESIGN.md` again. Code and `DESIGN.md` must agree.
3. Screenshot at desktop and 390px wide if your environment can, and critique the pictures against the brief.
4. Write `REVIEW.md` from `templates/REVIEW.md`.

## Output

When you finish, the project has `DESIGN.md` (valid), the UI (built only from its tokens) and `REVIEW.md`. Tell the user in a few lines: the direction and why it fits the subject, the one memorable element, and what you deliberately left out.
