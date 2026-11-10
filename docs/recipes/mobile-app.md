# Recipe: mobile app

| Step | Do |
|---|---|
| 0. Brief | The one task per screen. One-handed use? Offline? |
| 1. Direction | Derive from the subject or deal from the library. Respect the platform's own conventions (navigation, sheets, haptics). |
| 2. Lock | Same tokens, mapped to the platform theme object. Touch targets at least 44x44pt. |
| 3. Build | Platform components first; custom only for the one memorable element. Mobile rules 65-69 in `ux-rules.md`. |
| 4. Motion | Platform-native transitions for navigation; timing tokens for your own feedback. |
| 5. Review | `detect.py` covers web code; for native apps rely on screenshots and the checklist. |

## Prompt

```
Use ship-beautiful-ui. Design the <screen> for a <platform> app that helps <audience> <job>.
```
