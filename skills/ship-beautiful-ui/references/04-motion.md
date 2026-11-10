# Step 4: Motion

Motion should explain a change: something opened, something saved, something moved. Motion that runs on its own everywhere is the fastest way to make a page look generated.

## The decision rule

| The motion is... | Build it with | Examples |
|---|---|---|
| A response to a user action | CSS transitions (or the motion library the project already uses) | Open, close, toggle, press, toast, tab change |
| Tied to scroll | CSS scroll-driven animations (`animation-timeline: view()` / `scroll()`) with a static fallback; a timeline library only if the project already has one | Reading progress, image wipes, pinned story beats |
| A single showcase moment | One effect from `references/effects.md` | Headline reveal, glow field |
| Decoration on every section | Nothing | Fade-up on each block, hover lift on every card |

If `DESIGN.md` says something about motion, it wins.

## Timing tokens

Add these to `DESIGN.md` (Do's and Don'ts or Components) and to code as variables, then use only these:

| Token | Value | For |
|---|---|---|
| `--dur-quick` | 120ms | press, toggle, color change |
| `--dur-base` | 200ms | menus, popovers, tabs, toasts |
| `--dur-slow` | 320ms | modals, drawers, large surfaces |
| `--ease-out` | `cubic-bezier(.2,.7,.2,1)` | things entering or reacting |
| `--ease-in` | `cubic-bezier(.5,0,.75,0)` | things leaving |
| `--ease-move` | `cubic-bezier(.65,0,.35,1)` | things moving from A to B on screen |

## Rules

- **Enter with ease-out, leave with ease-in, move with ease-in-out.** Ease-in on an entrance feels sluggish.
- **Short.** Most UI motion is 120-320ms. Exits are faster than entrances.
- **Transform and opacity only.** Never animate width, height, top, left or margin.
- **From the source.** A menu grows from its button; a toast slides from the edge it lives on.
- **Interruptible.** A second click mid-animation reverses or retargets; it never queues.
- **Nothing on rapid repeat actions** such as keyboard shortcuts or fast toggling.
- **One ambient moment per screen**, at most. Everything else answers the user.

## Recipes

**1. Button press**
```css
.btn{transition:transform var(--dur-quick) var(--ease-out),background-color var(--dur-quick) var(--ease-out)}
.btn:active{transform:scale(.97)}
```

**2. Menu from its trigger**
```css
.menu{transform-origin:top left;opacity:0;transform:scale(.96) translateY(-4px);pointer-events:none;
  transition:opacity var(--dur-base) var(--ease-out),transform var(--dur-base) var(--ease-out)}
.menu[data-open]{opacity:1;transform:none;pointer-events:auto}
```

**3. Modal**
```css
dialog{opacity:0;transform:translateY(8px) scale(.98);transition:opacity var(--dur-slow) var(--ease-out),transform var(--dur-slow) var(--ease-out),overlay var(--dur-slow) allow-discrete,display var(--dur-slow) allow-discrete}
dialog[open]{opacity:1;transform:none}
@starting-style{dialog[open]{opacity:0;transform:translateY(8px) scale(.98)}}
```

**4. Toast**
```css
.toast{animation:toast-in var(--dur-base) var(--ease-out)}
.toast.leaving{animation:toast-out var(--dur-quick) var(--ease-in) forwards}
@keyframes toast-in{from{opacity:0;transform:translateY(12px)}}
@keyframes toast-out{to{opacity:0;transform:translateY(12px)}}
```

**5. Accordion (no height animation)**
```css
.acc{display:grid;grid-template-rows:0fr;transition:grid-template-rows var(--dur-base) var(--ease-out)}
.acc[data-open]{grid-template-rows:1fr}
.acc > div{overflow:hidden}
```

**6. Tab indicator**
```css
.tabs{position:relative}
.tabs .bar{position:absolute;bottom:0;height:2px;background:var(--accent);left:0;width:var(--w);transform:translateX(var(--x));
  transition:transform var(--dur-base) var(--ease-move),width var(--dur-base) var(--ease-move)}
```
Set `--x` and `--w` from the active tab's `offsetLeft` and `offsetWidth` in JS.

**7. List item added or removed**
```css
.item{animation:item-in var(--dur-base) var(--ease-out)}
@keyframes item-in{from{opacity:0;transform:translateY(-6px)}}
```
Remove items after a `var(--dur-quick)` fade, then let the list close the gap without animating height.

**8. Page-load sequence (the one ambient moment)**
Stagger 3-5 elements of the hero by 60-80ms with `--ease-out`, 400-600ms each. Nothing else on the page animates on load. See effect 7 in `effects.md`.

**9. Scroll reveal for one section**
```css
.beat{animation:beat-in linear both;animation-timeline:view();animation-range:entry 10% cover 30%}
@keyframes beat-in{from{opacity:0;transform:translateY(24px)}}
@supports not (animation-timeline:view()){.beat{animation:none}}
```
Use it for the beats of a story page, not for every block of a landing page.

**10. Pinned story beats**
```css
.story{height:400vh}
.story .stage{position:sticky;top:0;height:100vh}
.story .frame{animation:frame linear both;animation-timeline:view(block);}
```
Swap or fade the frames inside the sticky stage as the section scrolls. Build every beat as a readable static block first.

**11. Value change**
Briefly highlight a changed number with a background tint that fades over `--dur-slow`. Do not count up every number on the page; see effect 8 for the one metric worth it.

**12. Drag feedback**
Lift the dragged item with a stronger shadow and `scale(1.02)`; show the drop target with a dashed `--accent` outline. Return with `--ease-move` if dropped outside.

## Reduced motion

Every recipe needs a reduced-motion path. The blanket fallback:

```css
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}
}
```

In JS, check `matchMedia('(prefers-reduced-motion: reduce)').matches` before starting any pointer-driven or timeline motion.

## Review your motion

For each animation ask: does it explain a change? Is the easing right for its direction? Is it under 320ms? Would the screen be worse without it? If not, remove it.
