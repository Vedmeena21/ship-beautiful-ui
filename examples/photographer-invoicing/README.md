# Example: invoicing for freelance photographers

One brief, two pages.

| | `before.html` | `after.html` |
|---|---|---|
| What it is | A typical AI first draft for this brief, written to show what the detector catches | The same page built by following ship-beautiful-ui |
| `detect.py` | 3 errors, 12 warnings, 3 info | 0 findings |
| `DESIGN.md` | none | [`DESIGN.md`](DESIGN.md), passes `lint_design.py` |

## The brief

- **Subject:** invoicing for freelance photographers
- **Audience:** wedding and portrait photographers who work from their phone
- **Job:** send the first invoice for a shoot in under two minutes
- **World:** darkroom safelight, contact sheet, grey card, film edge, frame numbers

## How `after.html` was made

1. **Direction**, derived from the subject:
   ```bash
   python3 scripts/derive.py --words "darkroom safelight, contact sheet, grey card, film edge"
   ```
   Paper-white base, contact-sheet black, safelight red for actions, film-edge amber for frame numbers.
   Type: the `instrument` pairing (Instrument Serif + Instrument Sans). Layout: `product-proof`.
2. **Lock:** [`DESIGN.md`](DESIGN.md), checked with `lint_design.py` (0 errors).
3. **Build:** the one memorable element is the product itself, an invoice laid out on a contact sheet. No illustrations, no card grid, no invented numbers.
4. **Motion:** button press only, with a reduced-motion fallback.
5. **Review:** `detect.py after.html` → 0 findings.

## Reproduce

```bash
python3 skills/ship-beautiful-ui/scripts/detect.py examples/photographer-invoicing/before.html
python3 skills/ship-beautiful-ui/scripts/detect.py examples/photographer-invoicing/after.html
python3 skills/ship-beautiful-ui/scripts/lint_design.py examples/photographer-invoicing/DESIGN.md
```
