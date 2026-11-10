# Recipe: landing page

The page type most likely to come out generic: big-number hero, three identical feature cards, purple gradient, testimonial carousel.

| Step | Do |
|---|---|
| 0. Brief | Subject, audience, the one action (sign up, book, buy), five nouns from the subject's world. |
| 1. Direction | `python3 scripts/derive.py --words "<3-5 nouns>"`. Pick a type pairing by mood. Layout: `product-proof` for software, `photo-led` for places and food, `type-hero` for people and studios. |
| 2. Lock | Write `DESIGN.md`, paste the derived colors, run `lint_design.py`. |
| 3. Build | One memorable hero: the real product, a real photograph, or the headline itself. Sections grouped by meaning, not a card grid. |
| 4. Motion | One ambient moment at most (headline reveal or glow field from `effects.md`). Everything else answers the user. |
| 5. Review | `python3 scripts/detect.py src/`, screenshots at 1440px and 390px, checklist, `REVIEW.md`. |

## Prompt

```
Use ship-beautiful-ui. Build a landing page for <subject> aimed at <audience>.
The one job: <action>. Stack: <framework>. Derive the palette from the subject's world.
```
