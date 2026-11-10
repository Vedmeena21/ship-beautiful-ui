# UI review

<!-- Written by ship-beautiful-ui, step 5. Keep it short. -->

**Screen(s):** which pages or components were reviewed
**Date:** YYYY-MM-DD
**Direction:** derived from the subject (`derive.py`) / dealt from the library (`direction.py`) / existing brand

## Automated scan

| Tool | Command | Result |
|---|---|---|
| Detector | `python3 scripts/detect.py <src>` | N errors, N warnings, N info |
| DESIGN.md check | `python3 scripts/lint_design.py DESIGN.md` | errors / warnings |

## What I fixed

- Finding → fix

## What I kept, and why

- Finding → reason it stays

## Visual check

- Desktop: screenshot path or "not available"
- 390px: screenshot path or "not available"
- The one memorable element:
- What I removed:

## Checklist

- [ ] Matches DESIGN.md
- [ ] No rejected defaults crept back
- [ ] Works at 360px
- [ ] Keyboard focus visible
- [ ] WCAG AA text contrast
- [ ] Reduced motion respected
- [ ] One non-user-triggered motion moment at most
- [ ] No raw values in components
