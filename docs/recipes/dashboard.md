# Recipe: dashboard or web app

Apps live or die on density, hierarchy and states, not on hero effects.

| Step | Do |
|---|---|
| 0. Brief | Who uses it daily, what they check first, what they change most. |
| 1. Direction | `python3 scripts/direction.py --kind saas --brief "<one line>"` (or the brand). Layout: `dashboard-focus`, with `settings-plain` for settings. |
| 2. Lock | Add status tokens (success, warning, danger, info) and components for table rows, inputs and badges. Run `lint_design.py`. |
| 3. Build | Tables before cards. Loading, empty and error states for every data view. Keyboard paths for frequent actions. Chart rules 55-59 in `ux-rules.md`. |
| 4. Motion | Feedback only (recipes 1-7 in `04-motion.md`). No ambient motion. |
| 5. Review | `detect.py` on the source, then the checklist, with extra attention to states and tables. |

## Prompt

```
Use ship-beautiful-ui. Design the <screen> of <product> for <role>, who checks <thing> first.
Stack: <framework + component library>.
```
