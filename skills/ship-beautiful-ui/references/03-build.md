# Step 3: Build

Build from `DESIGN.md` and nothing else. If you are about to type a hex value or a font name into a component, add a token instead.

## Map tokens to code once

- **CSS:** custom properties on `:root` (`--base`, `--ink`, `--accent`, `--font-display`, `--space-md`, `--radius-sm`, `--dur-base`).
- **Tailwind:** extend the theme with the same names and don't use the default palette classes in components.
- **Native apps:** the platform theme object with the same names.
- **Fonts:** load only the families in `DESIGN.md`, only the weights you use, with `font-display: swap`.

## Spend boldness in one place

Choose the one memorable element of the screen: a typographic hero, a real product shot, a live demo, an unusual layout, or one effect from `references/effects.md`. Make it great and keep everything around it quiet. Before you finish, remove one decorative thing.

## Structure carries meaning

- Borders, dividers, numbering and labels must encode information. Number only real sequences.
- Group by meaning and size by importance. Identical cards say "equally important".
- One radius scale, applied by role: small for controls, medium for containers, large only for the hero surface.
- Shadow only where something floats above something else.

## Type

- Follow the type scale in `DESIGN.md`. Body 16px or more on the web.
- 45-80 characters per line. A little more line height for serif body text.
- Sentence case for headings and buttons.

## Copy

- Write for the user's goal in their words: "Send invoice", not "Submit".
- An action keeps its name through the flow.
- Errors say what happened and how to fix it. Empty states say what to do next.
- No filler, no fake testimonials, no numbers without a source.

## Effects

Pick at most one from `references/effects.md` (grain, glow field, dot grid, spotlight, gradient border, marquee, headline reveal, number roll-up, typed line, magnetic button, tilt card, sticky stack, scroll progress, image wipe, skeleton shimmer, underline draw). Recolor it with tokens. Keep its reduced-motion fallback.

## The quality floor

Build to this without being asked:

- Responsive from 360px to wide desktop, no horizontal scroll.
- Visible keyboard focus, logical tab order.
- WCAG AA contrast (4.5:1 text, 3:1 large text and UI parts).
- `prefers-reduced-motion` respected.
- Touch targets at least 44x44px.
- Useful alt text, or `alt=""` for decoration.
- Loading, empty and error states wherever data loads.
- `lang` on the html element, one h1, headings in order, labels on every field.

`references/ux-rules.md` has 80 more rules by area (layout, type, color, buttons, forms, navigation, feedback, tables, charts, media, mobile, accessibility, copy).

## CSS hygiene

Watch specificity: utility classes and component classes that set the same property cancel each other. Put section spacing in one place, from the `DESIGN.md` spacing scale.
