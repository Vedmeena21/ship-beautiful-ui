# Recipe: redesign an existing UI

The brand already exists, so step 1 is mostly reading, not inventing.

| Step | Do |
|---|---|
| 0. Brief | What is wrong today, in the user's words. What must not change. |
| 1. Direction | Route C: extract the current palette, type and components. Run `detect.py` on the current code first to see what is generic or broken. |
| 2. Lock | Write the current system as `DESIGN.md`, then propose `DESIGN-v2.md`. Lint both. |
| 3. Build | Change one screen end to end before touching the rest. |
| 4. Motion | Remove motion that does not explain a change before adding any. |
| 5. Review | Compare `detect.py` results before and after. Put both numbers in `REVIEW.md`. |

## Prompt

```
Use ship-beautiful-ui to redesign <screen>. Keep <brand constraints>.
Write the current design as DESIGN.md first, then propose DESIGN-v2.md before changing code.
```
