# Contributing

Thanks for helping. The most useful contributions are small and specific.

## Where things live

```
ship-beautiful-ui/
├── skills/ship-beautiful-ui/
│   ├── SKILL.md            # the six steps and who wins
│   ├── scripts/            # derive, direction, lint_design, detect (Python 3, no deps)
│   ├── data/               # materials, palettes, type pairings, layouts (JSON)
│   ├── references/         # one file per step, plus effects, motion, UX rules, anti-patterns
│   └── templates/          # DESIGN.md and REVIEW.md
├── docs/recipes/           # landing page, dashboard, mobile, redesign, scroll story
├── examples/               # before/after redesign: before.html, after.html, DESIGN.md
├── tests/                  # unit tests and fixtures for every script
└── .claude-plugin/         # Claude Code plugin marketplace
```

## Good first contributions

- **A new recipe.** Copy a file in `docs/recipes/`, keep the six-step table, and add it to `docs/recipes/README.md` and the README.
- **A new library entry.** A palette, material, type pairing, layout or effect. Run the tests: palettes and derived colors must pass contrast.
- **A new detector rule.** Add it to `scripts/detect.py`, a fixture that triggers it, and a line in `references/anti-patterns.md` (regenerate from `RULES`).

## Rules

- Write in plain English, short sentences, no hype.
- Do not copy text or code from other projects. Write it in your own words.
- Every count in the README (palettes, rules, recipes) must match the code. The tests check the main ones.
- Keep `SKILL.md` short. Detail goes in `references/`.

## Testing a change

Run `python3 -m unittest discover tests`. Then install the skill from your branch into a scratch project, give your agent a real brief, and check that it produces `DESIGN.md`, the UI and `REVIEW.md`, in that order. Mention the brief and the agent you used in the pull request.
