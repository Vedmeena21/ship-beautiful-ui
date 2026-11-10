# Step 5: Review

One gate at the end, in this order.

## 1. Scan the code

```bash
python3 scripts/detect.py src/                 # a folder
python3 scripts/detect.py index.html app.css   # files
python3 scripts/detect.py src/ --json          # machine-readable
python3 scripts/detect.py --list-rules         # all 40 rules
```

It checks for the patterns in `references/anti-patterns.md`: generic fonts, purple-to-blue gradients, identical shadows and radii, eyebrow labels, filler copy, lorem ipsum, animating layout properties, missing reduced-motion support, removed focus outlines, raw colors, emoji icons, skipped headings, unlabeled buttons and inputs, disabled zoom, autoplay media, missing `lang`, and more.

- **Errors** block handoff. Fix them.
- **Warnings** get fixed, or a one-line reason in `REVIEW.md`.
- **Info** is a judgment call.

## 2. Check DESIGN.md again

```bash
python3 scripts/lint_design.py DESIGN.md
```

Code and `DESIGN.md` must agree. If the build added a value, it belongs in `DESIGN.md`.

## 3. Look at it

If your environment can take screenshots, capture the screen at desktop width and at 390px. Look at the pictures, not the code:

- Does it look like it belongs to this subject, or could it be any product's page?
- Is there one memorable element, and is everything else quiet?
- Do any of the visual defaults (V1-V12 in `anti-patterns.md`) show?
- What would you remove? Remove it.

## 4. Checklist

**Direction**
- [ ] Palette, type and layout match `DESIGN.md`.
- [ ] None of the rejected defaults crept back in.
- [ ] Copy uses the subject's real vocabulary.

**Structure**
- [ ] Numbering only on real sequences.
- [ ] Not everything is an identical card.
- [ ] Radius and shadow follow hierarchy.

**Quality floor**
- [ ] Works at 360px, no horizontal scroll.
- [ ] Keyboard focus visible everywhere, tab order logical.
- [ ] Text contrast meets WCAG AA.
- [ ] `prefers-reduced-motion` respected.
- [ ] Touch targets at least 44x44px.
- [ ] Loading, empty and error states exist where data loads.

**Motion**
- [ ] At most one motion moment the user did not trigger.
- [ ] Timing tokens used; enter ease-out, exit ease-in.
- [ ] Only transform and opacity animated.

## 5. Write REVIEW.md

Fill in `templates/REVIEW.md`: scan results, what you fixed, what you kept and why, screenshots if you took them. It is for the next person or agent who touches the UI.
