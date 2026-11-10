<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/readme/header-dark.svg">
    <img src="assets/readme/header-light.svg" alt="ship-beautiful-ui" width="840">
  </picture>
</p>

<p align="center">
  <b>One skill that takes your coding agent from prompt to polished UI.<br>Its own design libraries, its own checks, and designs that come from your subject, not a template.</b>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-0F1115?style=flat-square" alt="MIT License"></a>
  <a href="skills/ship-beautiful-ui/SKILL.md"><img src="https://img.shields.io/badge/Agent%20Skill-SKILL.md-2B59FF?style=flat-square" alt="Agent Skill"></a>
  <img src="https://img.shields.io/badge/works%20with-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Cursor-2B59FF?style=flat-square" alt="Works with Claude Code, Codex and Cursor">
  <img src="https://img.shields.io/badge/dependencies-none-0F1115?style=flat-square" alt="No dependencies">
  <a href="https://github.com/Vedmeena21/ship-beautiful-ui/stargazers"><img src="https://img.shields.io/github/stars/Vedmeena21/ship-beautiful-ui?style=flat-square&color=2B59FF" alt="GitHub stars"></a>
  <a href="https://www.linkedin.com/in/ved-prakash-meena"><img src="https://img.shields.io/badge/LinkedIn-Ved%20Prakash%20Meena-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="Ved Prakash Meena on LinkedIn"></a>
</p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#how-it-works">How it works</a> ·
  <a href="#bring-your-brand-it-picks-the-colors">Bring your brand. It picks the colors.</a> ·
  <a href="#whats-inside">What's inside</a> ·
  <a href="#the-detector">The detector</a>
</p>

| Typical AI first draft | Built with ship-beautiful-ui |
|:---:|:---:|
| <img src="assets/readme/before.jpg" alt="Proofsheet, an invoicing tool for photographers, styled the default AI way: dark page, centered purple-to-blue gradient headline, emoji chips and a glowing glass card" width="420"> | <img src="assets/readme/after.jpg" alt="The same page and words redesigned with ship-beautiful-ui: a paper-white page with a serif headline 'Invoice the shoot before you finish the edit' and the real product: the invoice on a phone, ready to send" width="420"> |

### 🌐 Multi-language support

[English](README.md) | [Arabic](translations/ar/README.md) | [Chinese (Simplified)](translations/zh/README.md) | [French](translations/fr/README.md) | [German](translations/de/README.md) | [Hindi](translations/hi/README.md) | [Indonesian](translations/id/README.md) | [Japanese](translations/ja/README.md) | [Korean](translations/ko/README.md) | [Portuguese (Brazil)](translations/pt-BR/README.md) | [Russian](translations/ru/README.md) | [Spanish](translations/es/README.md) | [Turkish](translations/tr/README.md)

---

## Why this exists

Coding agents can write a whole frontend in minutes, and it still comes out looking like every other AI-built page: the same font, the same purple gradient, the same row of three identical cards, the same fade-up on every section.

That happens because the agent starts from the same defaults every time. **ship-beautiful-ui** replaces those defaults with a process, real design data, and checks that run on the result:

- **A process.** Brief → direction → lock → build → motion → review, always in that order.
- **Design from your subject.** The palette comes from things in your product's own world (a bakery's crust and flour, a darkroom's safelight red), not from a list everyone shares.
- **One source of truth.** Every visual decision is written into `DESIGN.md` before any code, and checked.
- **Checks, not vibes.** A 40-rule detector scans the code for AI tells and accessibility gaps before handoff.

No dependencies. The scripts are plain Python 3.

## Install

**Any agent (Claude Code, Codex, Cursor and more)** via the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills add Vedmeena21/ship-beautiful-ui
```

**Claude Code plugin:**

```
/plugin marketplace add Vedmeena21/ship-beautiful-ui
/plugin install ship-beautiful-ui@ship-beautiful-ui
```

**Manual:** copy [`skills/ship-beautiful-ui`](skills/ship-beautiful-ui) into `.claude/skills/` (project) or `~/.claude/skills/` (global).

**Then just ask for UI.** The skill starts on its own when you build, redesign or polish a page, screen or component:

```
Build a landing page for an invoicing tool for freelance photographers.
The one job: send a first invoice in under 2 minutes. Next.js + Tailwind.
```

```
This dashboard looks generic. Use ship-beautiful-ui to redesign it.
```

You get three things back:

| Output | What it is |
|---|---|
| `DESIGN.md` | Your design system: tokens and rules any agent can read, checked for contrast |
| The UI | Built only from `DESIGN.md` tokens |
| `REVIEW.md` | What the detector found, what was fixed, what was kept and why |

## How it works

<p align="center">
  <img src="assets/readme/pipeline.svg" alt="The six-step pipeline: brief, direction, lock in DESIGN.md, build, motion, review" width="840">
</p>

| Step | What happens | Built in |
|---|---|---|
| **0. Brief** | Subject, audience, the one job of the screen, five nouns from the subject's world | [`00-brief.md`](skills/ship-beautiful-ui/references/00-brief.md) |
| **1. Direction** | A palette, type pairing and layout made for this subject | `derive.py`, `direction.py`, 78 materials, 60 palettes, 40 pairings, 20 layouts |
| **2. Lock** | Every decision written into `DESIGN.md` and checked | `lint_design.py`, [`DESIGN.md` template](skills/ship-beautiful-ui/templates/DESIGN.md) |
| **3. Build** | Tokens only, one bold idea, the quality floor | [`effects.md`](skills/ship-beautiful-ui/references/effects.md) (16 effects), [`ux-rules.md`](skills/ship-beautiful-ui/references/ux-rules.md) (80 rules) |
| **4. Motion** | Only motion that explains a change | [`04-motion.md`](skills/ship-beautiful-ui/references/04-motion.md): timing tokens and 12 recipes |
| **5. Review** | One gate before handoff | `detect.py` (40 rules), screenshots, [`REVIEW.md`](skills/ship-beautiful-ui/templates/REVIEW.md) |

**Who wins when instructions disagree:** your words > `DESIGN.md` > the skill's rules > anything else loaded. The agent says it out loud when it resolves a conflict, so you can overrule it.

## Bring your brand. It picks the colors.

Working at Microsoft? Tell it so, and every page is built from Microsoft's colors: the blue for actions, your neutrals for text, plus the shades a real UI needs. No brand yet? Describe your product's world in a few words and it builds a palette for you.

| You say | You get |
|---|---|
| *We work at Microsoft. Use our blue, green, red and yellow.* | Those exact colors on buttons, accents and highlights, plus matching text, border, hover and error shades |
| *An invoicing app for photographers: darkroom, safelight, film* | Paper-white page, deep black text, safelight-red buttons, film-amber details (the after page above) |
| *A bakery: crust, flour, espresso, saffron* | Flour-white page, espresso-brown text, crust-colored buttons, saffron highlights |

Every color is checked for readability (WCAG AA) before a line of code is written. No clear subject yet? `direction.py` offers three ready-made directions to pick from.

## What's inside

Everything your agent needs to design like a pro, in one folder. No accounts, no API keys, nothing extra to install.

| What you get | How many | Why it matters |
|---|:---:|---|
| Real-world materials | **78** | Colors taken from things like kraft paper, espresso, moss and film, so the palette fits your product |
| Color palettes | **60** | Ready to use, light and dark, every one tested for readability |
| Font pairings | **40** | A heading font and a body font that work together, all free on Google Fonts |
| Page layouts | **20** | Proven page structures with sketches: product hero, editorial, dashboard, pricing and more |
| Visual effects | **16** | Grain, glow, spotlight, marquee, tilt and more: copy-paste CSS that takes your colors and respects reduced motion |
| Animation recipes | **12** | Buttons, menus, modals, toasts, tabs and lists that all move the same polished way |
| UX rules | **80** | A checklist for forms, navigation, tables, charts, mobile, and empty and error states |
| Detector checks | **40** | Catch the AI look and accessibility gaps before you ship |

### Four tools that do the work

| Tool | What it does for you |
|---|---|
| `derive.py` | Describe your product in a few words, get a color palette that fits it |
| `direction.py` | Not sure where to start? Get 3 design directions to pick from, saved as a `DESIGN.md` |
| `lint_design.py` | Checks that your `DESIGN.md` is complete and every color is readable |
| `detect.py` | Scans your code (HTML, CSS, React, Vue, Svelte, Astro) for 40 signs of AI-made UI |

## The detector

```
$ python3 scripts/detect.py src/
SBU001 warning One generic sans for everything
SBU002 warning Purple-to-blue gradient
SBU010 error   Motion without reduced-motion support
SBU011 error   Focus outline removed
SBU013 warning Cream page + terracotta accent
...
Scanned 1 files: 6 errors, 10 warnings, 5 info
```

Every finding comes with a fix. Errors block handoff; warnings get fixed or a written reason in `REVIEW.md`. The full list, plus 12 visual defaults the agent checks by eye, is in [`anti-patterns.md`](skills/ship-beautiful-ui/references/anti-patterns.md).

## License

[MIT](LICENSE). Built and maintained by **Ved Prakash Meena**.

<a href="https://www.linkedin.com/in/ved-prakash-meena"><img src="https://img.shields.io/badge/Follow%20on%20LinkedIn-Ved%20Prakash%20Meena-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Follow Ved Prakash Meena on LinkedIn"></a>

<p align="center">
  <sub>If this saved you a round of "make it look less AI", a ⭐ helps others find it, and <a href="https://www.linkedin.com/in/ved-prakash-meena">follow me on LinkedIn</a> for more.</sub>
</p>
