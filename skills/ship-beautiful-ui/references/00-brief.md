# Step 0: Brief

Generic UI starts with a generic brief. "Build me a landing page" gives the model nothing to design from, so it reaches for the defaults it has seen most. The fix is to pin the subject down before any visual decision.

## The four lines

Write these before step 1. Keep each to one sentence.

| Line | Question | Weak | Strong |
|---|---|---|---|
| Subject | What is this about, in the user's words? | "A SaaS product" | "Invoicing for freelance photographers" |
| Audience | Who looks at it, and what do they already know? | "Users" | "Photographers who hate spreadsheets and check email on their phone" |
| Job | The one thing the screen must get done | "Show features" | "Get a photographer to send their first invoice in under 2 minutes" |
| Constraints | What is fixed? | – | "Next.js + Tailwind, existing logo, must pass WCAG AA" |

## Where good design ideas come from

Distinct choices come from the subject's own world: its materials, tools, vocabulary, places and history. Before choosing anything visual, list 5 nouns from the subject's world.

> Freelance photographers: contact sheets, light meters, film rebates, darkroom red, grey cards.

Those nouns are raw material for step 1. A contact-sheet grid, grey-card neutrals and one safelight red say "photography" without a single camera icon.

## When the brief is thin

- Propose the four lines yourself from whatever the user said, and confirm in one message.
- Ask at most three questions. Prefer questions whose answers change the design: audience, the one job, existing brand.
- If the user says "you decide", decide, write it down, and move on.

## Real content

Ask for real copy, product names, numbers and screenshots. If there are none, write realistic placeholder content in the subject's vocabulary. Never ship lorem ipsum, "Feature 1 / Feature 2", or invented testimonials with fake names presented as real.

## Output

A short block at the top of your working notes, and later in the Overview section of `DESIGN.md`:

```
Subject:     ...
Audience:    ...
Job:         ...
Constraints: ...
World:       5 nouns from the subject's world
```
