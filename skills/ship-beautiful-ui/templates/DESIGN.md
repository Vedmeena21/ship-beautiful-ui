---
version: alpha
name: Replace with the product name
description: One line on what this product is and who it is for.
colors:
  base: "#F6F7F9"
  surface: "#FFFFFF"
  ink: "#14171C"
  muted: "#5B6472"
  line: "#DDE1E7"
  accent: "#1F5FD6"
  on-accent: "#FFFFFF"
typography:
  display:
    fontFamily: Replace Display Family
    fontSize: 56px
    fontWeight: 600
    lineHeight: 1.05
    letterSpacing: -0.02em
  h2:
    fontFamily: Replace Display Family
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.15
  body:
    fontFamily: Replace Body Family
    fontSize: 17px
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: Replace Body Family
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.3
rounded:
  sm: 6px
  md: 12px
  lg: 20px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 32px
  xl: 64px
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.on-accent}"
    typography: "{typography.label}"
    rounded: "{rounded.sm}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.ink}"
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: 24px
---

<!-- Template from ship-beautiful-ui (github.com/Vedmeena21/ship-beautiful-ui).
     Replace every value above. The placeholder palette is deliberately plain:
     it is not a design. Get a real one with scripts/derive.py or scripts/direction.py,
     then check with: python3 scripts/lint_design.py DESIGN.md -->

## Overview

Subject: what this is about, in the user's words.
Audience: who looks at it and what they already know.
Job: the one thing the main screen must get done.
World: five nouns from the subject's world that the design borrows from.

Direction in two or three sentences: the feeling, and why it fits this subject.

## Colors

- **Base (#F6F7F9):** page background.
- **Surface (#FFFFFF):** raised areas only.
- **Ink (#14171C):** headings and body text.
- **Muted (#5B6472):** secondary text. Never on colored backgrounds.
- **Line (#DDE1E7):** dividers and input borders.
- **Accent (#1F5FD6):** the one interactive color. Primary actions and links only.

## Typography

Display for headlines only, body for everything else. Sentence case. Body never below 16px. Line length under 80 characters.

## Layout

Describe the grid, the max content width and the alignment. Add a small ASCII wireframe of the first screen.

## Elevation & Depth

Say which elements float and how that is shown (shadow, border or tone). If nothing floats, say so.

## Shapes

Small radius for controls, medium for containers, large only for the one hero surface.

## Components

Describe the primary button, inputs, navigation and any custom component, with their states (hover, focus, disabled, loading, error).

## Do's and Don'ts

- Do: spend boldness on one element per screen.
- Do: use only tokens from this file in code.
- Don't: list here the generic defaults you rejected in the direction step, so nobody drifts back to them.
- Don't: add motion that the user did not trigger, beyond one moment per screen.
