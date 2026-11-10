# Anti-patterns

The things that make UI look AI-generated, plus gaps in the quality floor. Rules SBU001-SBU040 are checked automatically by `scripts/detect.py`; the visual defaults at the end can only be caught by looking, so check them in step 1 (plan) and step 5 (screenshots).

Severity: **error** blocks handoff, **warning** needs a fix or a written reason in `REVIEW.md`, **info** is a judgment call.

## Checked by `scripts/detect.py`

| Rule | Severity | Pattern | Fix |
|---|---|---|---|
| SBU001 | warning | One generic sans for everything | Only Inter (or the system stack) is used. Pair a display face with a body face that fit the subject. |
| SBU002 | warning | Purple-to-blue gradient | Purple/violet to blue/indigo gradients are the most common AI decoration. Use a flat accent from DESIGN.md. |
| SBU003 | info | Gradient text | background-clip:text gradients on headings read as templated. Let type size and weight do the work. |
| SBU004 | warning | Same soft shadow everywhere | The same low-opacity black shadow appears on many elements. Use shadow only for things that float. |
| SBU005 | warning | All-caps tracked eyebrows | Many uppercase, letter-spaced labels. Keep labels only where they carry information, in sentence case. |
| SBU006 | info | Numbered markers | 01 / 02 / 03 markers. Use them only for real sequences. |
| SBU007 | error | Lorem ipsum | Placeholder Latin. Write realistic copy in the subject's vocabulary. |
| SBU008 | warning | Filler marketing copy | Phrases like 'unlock the power', 'seamless', 'revolutionize'. Say what the product does, plainly. |
| SBU009 | warning | Animating layout properties | Transitions on width/height/top/left/margin cause layout work. Animate transform and opacity. |
| SBU010 | error | Motion without reduced-motion support | Animations or transitions exist but nothing handles prefers-reduced-motion. |
| SBU011 | error | Focus outline removed | outline: none/0 without a :focus-visible style. Keyboard users lose their place. |
| SBU012 | warning | Raw colors in components | Many hard-coded hex colors in component files. Use DESIGN.md tokens (CSS variables or theme). |
| SBU013 | warning | Cream page + terracotta accent | The most common 'tasteful' AI default. Fine if the brief asked for it; otherwise choose for the subject. |
| SBU014 | warning | Near-black + neon accent | Near-black background with an acid green or neon accent: a common AI default. |
| SBU015 | info | One radius on everything | Almost every rounded corner uses the same value. Vary radius by hierarchy. |
| SBU016 | info | Arrow appended to every link | '→' added to many links or buttons. Let the label say what happens. |
| SBU017 | info | Middle-dot meta strings | Many 'A · B · C' strings. Use structure (lists, columns) when the items matter. |
| SBU018 | warning | Fade-up on everything | Many scroll-reveal / fade-in-up animations. Keep one ambient motion moment per screen. |
| SBU019 | error | Image without alt | <img> without an alt attribute. Describe it, or use alt="" if decorative. |
| SBU020 | warning | Tiny text | font-size below 12px. Body text should be 16px or larger; labels at least 12px. |
| SBU021 | warning | Emoji as icons | Emoji in headings or buttons stand in for real icons. Use one consistent icon set or none. |
| SBU022 | warning | Skipped heading level | Heading levels jump (for example h1 to h3). Screen readers use them to navigate. |
| SBU023 | warning | More than one h1 | A page should have one h1 that says what it is. |
| SBU024 | error | Icon button without a name | A <button> with no text and no aria-label. Give it a name. |
| SBU025 | error | Input without a label | Form fields need a <label for> or aria-label; placeholder text is not a label. |
| SBU026 | warning | Generic link text | 'Click here', 'learn more', 'read more' say nothing out of context. Name the destination. |
| SBU027 | info | Justified text | text-align: justify makes uneven word gaps on the web. Left-align body text. |
| SBU028 | warning | Tight body line height | Body line-height under 1.3 is hard to read. Use 1.4-1.6 for body text. |
| SBU029 | warning | Placeholder people and companies | John Doe, Jane Doe, Acme Inc. Use real names with permission, or none. |
| SBU030 | info | Unsourced big numbers | '10x', '99.9%', '10,000+ users' need a source. Remove numbers you can't back up. |
| SBU031 | error | Zoom disabled | user-scalable=no or maximum-scale=1 blocks pinch zoom for low-vision users. |
| SBU032 | warning | Autoplaying media | Video or audio that autoplays with sound, or without controls. Mute it and give controls. |
| SBU033 | info | Lots of !important | Many !important rules usually mean fighting specificity. Fix the selectors instead. |
| SBU034 | info | Extreme z-index | z-index of 9999 and up. Define a small z-index scale in DESIGN.md. |
| SBU035 | info | Glass on everything | backdrop-filter blur on many elements. Frosted glass works for one layer, not every card. |
| SBU036 | warning | Framework default palette | Many default framework color classes (bg-indigo-500, text-blue-600). Map colors to DESIGN.md tokens. |
| SBU037 | info | Icon tile above every heading | A tinted rounded square with an icon above each heading is template chrome. Use icons only where they help scanning. |
| SBU038 | warning | Emoji bullets | Rows of emoji used as bullets (rocket, sparkles, check). Use plain lists or real icons. |
| SBU039 | warning | Content only on hover | Content hidden until :hover is unreachable by keyboard and touch. Add :focus-within or show it. |
| SBU040 | error | Missing page language | <html> without a lang attribute. Screen readers need it to pronounce text. |

## Visual defaults (check by eye)

These are legitimate when the brief asks for them. When it doesn't, they are defaults, not choices.

| # | Default look | Ask instead |
|---|---|---|
| V1 | Warm cream page, high-contrast serif, terracotta accent | What color is actually in this subject's world? (`scripts/derive.py`) |
| V2 | Near-black page with one neon accent | Does this product live at night? If not, why dark? |
| V3 | Purple-to-blue gradient blobs as decoration | What image or object could carry the mood instead? |
| V4 | Big number + small label + gradient as the hero | What is the most characteristic thing in this subject's world? Lead with that. |
| V5 | Three identical feature cards in a row | Are these really equal? Size them by importance, or use a list. |
| V6 | An all-caps tracked label above every heading | Does the label carry information the heading doesn't? |
| V7 | One radius and one soft shadow on everything | Which surfaces float? Which are controls? Vary by role. |
| V8 | Fade-and-slide-up on every section | Which one moment deserves motion? |
| V9 | Testimonial carousel with stock faces | Is there a real quote you can use with permission? If not, cut it. |
| V10 | Generic 3D blob or abstract gradient hero image | Show the product, or a real photograph from the subject's world. |
| V11 | Inter (or one geometric sans) for everything | Pick a pairing with roles (`data/type-pairings.json`). |
| V12 | Emoji as icons and bullets | One icon set, or none. |
