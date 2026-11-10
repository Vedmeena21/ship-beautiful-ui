<p align="center">
  <img src="assets/readme/header.png" alt="ship-beautiful-ui: one skill from prompt to polished UI. No more AI-looking UI." width="840">
</p>

<p align="center">
  <b>One skill that takes your coding agent from prompt to polished UI.<br>Its own design libraries, its own checks, and designs that come from your subject, not a template.</b>
</p>

```bash
npx skills add Vedmeena21/ship-beautiful-ui
```

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-0F1115?style=flat-square" alt="MIT License"></a>
  <a href="skills/ship-beautiful-ui/SKILL.md"><img src="https://img.shields.io/badge/Agent%20Skill-SKILL.md-2B59FF?style=flat-square" alt="Agent Skill"></a>
  <img src="https://img.shields.io/badge/works%20with-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Cursor-2B59FF?style=flat-square" alt="Works with Claude Code, Codex and Cursor">
  <img src="https://img.shields.io/badge/dependencies-none-0F1115?style=flat-square" alt="No dependencies">
  <a href="https://github.com/Vedmeena21/ship-beautiful-ui/stargazers"><img src="https://img.shields.io/github/stars/Vedmeena21/ship-beautiful-ui?style=flat-square&color=2B59FF" alt="GitHub stars"></a>
  <a href="translations"><img src="https://img.shields.io/badge/languages-13-2B59FF?style=flat-square" alt="README in 13 languages"></a>
</p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#how-it-works">How it works</a> ·
  <a href="#your-brand-your-colors">Your brand, your colors</a> ·
  <a href="#whats-inside">What's inside</a>
</p>

| Typical AI first draft | Built with ship-beautiful-ui |
|:---:|:---:|
| <img src="assets/readme/before.jpg" alt="Proofsheet, an invoicing tool for photographers, styled the default AI way: dark page, centered purple-to-blue gradient headline, emoji chips and a glowing glass card" width="420"> | <img src="assets/readme/after.jpg" alt="The same page and words redesigned with ship-beautiful-ui: a paper-white page with a serif headline 'Invoice the shoot before you finish the edit' and the real product: the invoice on a phone, ready to send" width="420"> |

<details>
<summary>🌐 Multi-language support</summary>

[English](README.md) | [Arabic](translations/ar/README.md) | [Chinese (Simplified)](translations/zh/README.md) | [French](translations/fr/README.md) | [German](translations/de/README.md) | [Hindi](translations/hi/README.md) | [Indonesian](translations/id/README.md) | [Japanese](translations/ja/README.md) | [Korean](translations/ko/README.md) | [Portuguese (Brazil)](translations/pt-BR/README.md) | [Russian](translations/ru/README.md) | [Spanish](translations/es/README.md) | [Turkish](translations/tr/README.md)

</details>

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

## Your brand, your colors

Tell the agent what your product is, and it designs for that product, not from a shared list. Working for a company with brand colors? It uses them. No brand yet? It picks colors that fit.

- **You have a brand.** Share your colors and they are kept exactly as they are. The agent adds the rest a real UI needs: text, borders, hover and error colors.
- **You don't have one yet.** Describe your product in a few words and the agent picks colors that fit what it is about.
- **Not sure yet?** `direction.py` offers three ready-made looks to choose from.

Either way, every color is checked to be easy to read (WCAG AA) before a line of code is written.

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

## License

[MIT](LICENSE). Built and maintained by **Ved Prakash Meena**.

<a href="https://www.linkedin.com/in/ved-prakash-meena"><img src="https://img.shields.io/badge/Follow%20on%20LinkedIn-Ved%20Prakash%20Meena-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Follow Ved Prakash Meena on LinkedIn"></a>

<p align="center">
  <sub>If this saved you a round of "make it look less AI", a ⭐ helps others find it, and <a href="https://www.linkedin.com/in/ved-prakash-meena">follow me on LinkedIn</a> for more.</sub>
</p>
