# UX rules

Eighty rules for interfaces that work, grouped by area. Use them while building (step 3) and as a second pass in review (step 5). They are written for this skill; most are long-standing interface practice.

## Layout and hierarchy
1. Every screen has one primary action. Make it the most visible thing after the headline.
2. Group by meaning, then space by group: tight inside a group, generous between groups.
3. Align to one grid. Mixed left edges look accidental.
4. Size things by importance, not by habit. Equal boxes say "equally important".
5. Keep the most important content above the first scroll on a 1366x768 laptop.
6. Use whitespace before adding a divider. Add a divider only when space can't separate.
7. Limit a screen to two or three levels of emphasis.

## Typography
8. Body text 16px or larger on the web; 17-18px for reading pages.
9. Line length 45-80 characters.
10. Line height 1.4-1.6 for body, 1.05-1.25 for large headings.
11. One or two families. If two, make them clearly different.
12. Use weight and size for hierarchy before color.
13. Sentence case for headings, buttons and labels.
14. Tabular figures for numbers in tables and prices.
15. Never set body text in light (300) weight on screens.

## Color and contrast
16. Text contrast at least 4.5:1, large text and UI parts at least 3:1.
17. One accent color for interaction. If everything is accented, nothing is.
18. Never use color alone to carry meaning; add text or an icon.
19. Gray text never sits on a colored background.
20. Dark mode is its own palette, not inverted light mode.
21. Status colors (success, warning, danger, info) are tokens, used only for status.

## Buttons and links
22. A button says what happens: "Send invoice", not "Submit".
23. The same action keeps the same name through the flow.
24. One primary button per area; others are secondary or text buttons.
25. Links look like links: underlined or clearly colored, with a hover and focus state.
26. Disabled buttons explain why, nearby or on focus.
27. Destructive actions are visually distinct and confirm or offer undo.
28. Touch targets at least 44x44px.

## Forms
29. Every field has a visible label. Placeholder text is not a label.
30. Ask only what you need. Every field costs completion.
31. One column. Side-by-side fields only for short related pairs (city, postcode).
32. Validate on blur, not on every keystroke.
33. Errors say what is wrong and how to fix it, next to the field.
34. Keep user input when showing an error.
35. Use the right input type (email, tel, number) and autocomplete attributes.
36. Mark optional fields, not required ones, when most are required.

## Navigation
37. Users always know where they are: highlight the current section.
38. Keep primary navigation to 5-7 items.
39. Search is visible on content-heavy products.
40. The logo links home.
41. Mobile navigation keeps the most used action reachable with a thumb.
42. Breadcrumbs for hierarchies deeper than two levels.

## Feedback and states
43. Every action gets feedback within 100ms (pressed state, spinner, toast).
44. Design loading, empty, error and success states for every data view.
45. Empty states say what to do next and offer the action.
46. Prefer skeletons that match the layout over spinners for content.
47. Offer undo instead of "Are you sure?" where possible.
48. Long tasks show progress and can run in the background.

## Data and tables
49. Tables before cards for anything people compare.
50. Right-align numbers, left-align text.
51. Sticky header for long tables.
52. Sort and filter where people look for something.
53. Show units in the header, not in every cell.
54. Truncate with a tooltip or expand, never silently.

## Charts
55. Pick the chart by the question: trend = line, comparison = bar, part of whole = stacked bar (not pie beyond 3 slices).
56. Start bar charts at zero.
57. Label lines directly instead of using a legend when possible.
58. Use one accent for the series that matters; others in muted tones.
59. Give every chart a sentence that states the takeaway.

## Images and media
60. Real product screenshots and real photographs beat illustrations of nothing.
61. Every meaningful image has alt text; decorative ones have `alt=""`.
62. Reserve image space to prevent layout shift (width and height, or aspect-ratio).
63. Video never autoplays with sound; it has controls and captions.
64. Compress and size images for their display size.

## Mobile and touch
65. Design at 360px first for anything people use on phones.
66. No hover-only interactions.
67. Inputs at least 16px font size to avoid zoom on focus in mobile browsers.
68. Bottom sheets over modals on small screens.
69. Never disable pinch zoom.

## Accessibility
70. Everything works with a keyboard, in a logical order.
71. Focus is always visible.
72. One h1 per page, headings in order.
73. Icon-only buttons have an accessible name.
74. `lang` is set on the html element.
75. Respect `prefers-reduced-motion` and `prefers-color-scheme`.

## Copy
76. Write for the user's goal, in their words.
77. Front-load the important word in headings and buttons.
78. No filler adjectives ("seamless", "powerful", "cutting-edge").
79. Errors don't apologize and are never vague.
80. Numbers and claims need a source, or they go.
