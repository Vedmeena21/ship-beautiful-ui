---
version: alpha
name: Proofsheet
description: Invoicing for freelance photographers. Send an invoice for a shoot from your phone in under two minutes.
colors:
  base: "#F7F7F3"
  surface: "#FCFCFA"
  ink: "#141414"
  muted: "#70706F"
  line: "#D7D7D4"
  accent: "#B3261E"
  on-accent: "#FFFFFF"
  accent-2: "#C27E19"
typography:
  display:
    fontFamily: Instrument Serif
    fontSize: 76px
    fontWeight: 400
    lineHeight: 0.98
    letterSpacing: -0.01em
  body:
    fontFamily: Instrument Sans
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: Instrument Sans
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.3
  mono:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1.4
rounded:
  sm: 4px
  md: 8px
spacing:
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
    padding: 14px
  invoice:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.sm}"
    padding: 24px
  phone:
    backgroundColor: "{colors.ink}"
    rounded: "{rounded.md}"
---

## Overview

Subject: invoicing for freelance photographers.
Audience: wedding and portrait photographers who hate spreadsheets and work from their phone.
Job: send the first invoice for a shoot in under two minutes.
World: darkroom safelight, contact sheet, grey card, film edge, frame numbers.

Direction: derived with `derive.py` from the darkroom. Paper-white base, contact-sheet black, one safelight red for actions, film-edge amber only for status dots.

## Colors

- **base (#F7F7F3):** page, like photo paper.
- **ink (#141414):** text and the phone.
- **muted (#70706F):** secondary text.
- **accent (#B3261E):** safelight red, primary actions only.
- **accent-2 (#C27E19):** film-edge amber, status dots only.

## Typography

Instrument Serif for the headline only. Instrument Sans for everything else. JetBrains Mono for invoice numbers and amounts.

## Layout

Product proof: the headline on the left, the real product on the right: the invoice on a phone, ready to send, and the payment it brings back.

## Components

Primary button, the invoice, the phone. The invoice on the phone is the one memorable element: it is the promise of the headline, shown.

## Do's and Don'ts

- Do: show the product, not an illustration.
- Don't: purple gradients, emoji, feature-card grids, eyebrow labels, invented user counts.
