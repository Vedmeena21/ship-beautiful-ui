# Effects library

Sixteen effects written for this skill, in plain CSS and small vanilla JS. No dependencies. Each one reads colors from `DESIGN.md` tokens (as CSS variables) and has a reduced-motion fallback.

**Rule:** one effect per screen, on the one memorable element. If you want a second, remove the first.

Assumed variables (map them from `DESIGN.md`): `--base`, `--surface`, `--ink`, `--muted`, `--line`, `--accent`, `--accent-2`.

---

## 1. Grain

Paper-like texture over a flat background. Use on large calm surfaces. Avoid on dense UI.

```css
.grain{position:relative;isolation:isolate}
.grain::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:-1;opacity:.12;mix-blend-mode:multiply;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>")}
```

## 2. Soft glow field

Two or three blurred color fields behind a hero, drifting very slowly. Use the palette's accent and accent-2, never a purple-to-blue default.

```css
.glow{position:relative;overflow:hidden;isolation:isolate}
.glow i{position:absolute;width:45vmax;height:45vmax;border-radius:50%;filter:blur(80px);opacity:.35;z-index:-1;animation:drift 24s ease-in-out infinite alternate}
.glow i:nth-child(1){background:var(--accent);left:-15vmax;top:-20vmax}
.glow i:nth-child(2){background:var(--accent-2);right:-18vmax;top:10vmax;animation-delay:-8s}
@keyframes drift{to{transform:translate(4vmax,3vmax) scale(1.08)}}
@media (prefers-reduced-motion:reduce){.glow i{animation:none}}
```

## 3. Dot grid

Quiet structure for technical products. Keep dots close to the background color.

```css
.dots{background-image:radial-gradient(circle at 1px 1px,color-mix(in srgb,var(--ink) 14%,transparent) 1px,transparent 1.4px);background-size:24px 24px}
```

## 4. Spotlight

A soft light follows the pointer across a dark panel. Use on one feature panel, not the whole page.

```css
.spot{--x:50%;--y:50%;background:radial-gradient(400px circle at var(--x) var(--y),color-mix(in srgb,var(--accent) 22%,transparent),transparent 60%),var(--surface)}
```
```js
document.querySelectorAll('.spot').forEach(el=>el.addEventListener('pointermove',e=>{
  const r=el.getBoundingClientRect();el.style.setProperty('--x',e.clientX-r.left+'px');el.style.setProperty('--y',e.clientY-r.top+'px')}))
```

## 5. Gradient border

A thin two-color border on one featured element (the recommended plan, a key card).

```css
.edge{border:1.5px solid transparent;border-radius:12px;
  background:linear-gradient(var(--surface),var(--surface)) padding-box,linear-gradient(120deg,var(--accent),var(--accent-2)) border-box}
```

## 6. Marquee

A slow strip of logos or words. Pauses on hover and focus; static with reduced motion.

```html
<div class="marquee" aria-label="Customers"><div class="track"><span>Item</span><span>Item</span><!-- repeat the set twice --></div></div>
```
```css
.marquee{overflow:hidden;mask-image:linear-gradient(90deg,transparent,#000 10%,#000 90%,transparent)}
.marquee .track{display:flex;gap:48px;width:max-content;animation:slide 40s linear infinite}
.marquee:hover .track,.marquee:focus-within .track{animation-play-state:paused}
@keyframes slide{to{transform:translateX(-50%)}}
@media (prefers-reduced-motion:reduce){.marquee .track{animation:none;flex-wrap:wrap}}
```

## 7. Headline reveal

Words rise into place once on load. This is the screen's one ambient motion moment.

```css
.reveal span{display:inline-block;opacity:0;transform:translateY(.4em);animation:rise .6s cubic-bezier(.2,.7,.2,1) forwards;animation-delay:calc(var(--i)*60ms)}
@keyframes rise{to{opacity:1;transform:none}}
@media (prefers-reduced-motion:reduce){.reveal span{animation:none;opacity:1;transform:none}}
```
```js
document.querySelectorAll('.reveal').forEach(h=>{h.innerHTML=h.textContent.trim().split(/\s+/).map((w,i)=>`<span style="--i:${i}">${w}</span>`).join(' ')})
```

## 8. Number roll-up

A real metric counts up when it scrolls into view. Only for numbers you can source.

```js
const io=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;const el=e.target,to=+el.dataset.to,t0=performance.now();
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const step=t=>{const p=reduce?1:Math.min(1,(t-t0)/900);el.textContent=Math.round(to*(1-Math.pow(1-p,3))).toLocaleString();if(p<1)requestAnimationFrame(step)};
  requestAnimationFrame(step);io.unobserve(el)}));
document.querySelectorAll('[data-to]').forEach(el=>io.observe(el));
```

## 9. Typed line

One line types itself, for developer tools and terminals. Keep it under 40 characters.

```css
.typed{font-family:var(--font-mono);white-space:nowrap;overflow:hidden;border-right:2px solid var(--accent);width:0;animation:type 1.6s steps(var(--n)) .3s forwards,caret .8s step-end infinite}
@keyframes type{to{width:calc(var(--n)*1ch)}}@keyframes caret{50%{border-color:transparent}}
@media (prefers-reduced-motion:reduce){.typed{animation:none;width:auto;border:0}}
```

## 10. Magnetic button

The primary button leans slightly toward the pointer. Maximum 6px. One button per page.

```js
document.querySelectorAll('.magnet').forEach(b=>{if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();const x=(e.clientX-r.left-r.width/2)/r.width,y=(e.clientY-r.top-r.height/2)/r.height;b.style.transform=`translate(${x*6}px,${y*6}px)`});
  b.addEventListener('pointerleave',()=>b.style.transform='')});
```
```css
.magnet{transition:transform .2s cubic-bezier(.2,.7,.2,1)}
```

## 11. Tilt card

A product shot tilts a few degrees with the pointer. Maximum 6 degrees.

```js
document.querySelectorAll('.tilt').forEach(c=>{if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect();const x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
    c.style.transform=`perspective(900px) rotateX(${-y*6}deg) rotateY(${x*6}deg)`});
  c.addEventListener('pointerleave',()=>c.style.transform='')});
```

## 12. Sticky stack

Sections stack on top of each other as you scroll. Good for 3-5 steps of a process.

```css
.stack > section{position:sticky;top:calc(64px + var(--i)*16px);min-height:70vh;background:var(--surface);border:1px solid var(--line);border-radius:16px}
```

## 13. Scroll progress

A thin bar shows reading progress on long articles. Uses scroll-driven animation where supported.

```css
.progress{position:fixed;inset:0 0 auto;height:3px;background:var(--accent);transform-origin:0 50%;transform:scaleX(0);animation:grow linear both;animation-timeline:scroll(root)}
@keyframes grow{to{transform:scaleX(1)}}
@supports not (animation-timeline:scroll()){.progress{display:none}}
@media (prefers-reduced-motion:reduce){.progress{display:none}}
```

## 14. Image wipe

An image uncovers itself as it enters the viewport.

```css
.wipe{animation:wipe linear both;animation-timeline:view();animation-range:entry 0% cover 35%}
@keyframes wipe{from{clip-path:inset(0 0 100% 0)}to{clip-path:inset(0)}}
@supports not (animation-timeline:view()){.wipe{animation:none}}
@media (prefers-reduced-motion:reduce){.wipe{animation:none}}
```

## 15. Skeleton shimmer

Loading placeholders that match the final layout. Better than a spinner for content.

```css
.skeleton{background:linear-gradient(90deg,var(--line) 0%,color-mix(in srgb,var(--line) 50%,var(--surface)) 50%,var(--line) 100%);background-size:200% 100%;animation:shimmer 1.4s linear infinite;border-radius:6px}
@keyframes shimmer{to{background-position:-200% 0}}
@media (prefers-reduced-motion:reduce){.skeleton{animation:none}}
```

## 16. Underline draw

Links underline from left to right on hover and focus.

```css
.draw{text-decoration:none;background:linear-gradient(currentColor,currentColor) 0 100%/0 1.5px no-repeat;transition:background-size .25s cubic-bezier(.2,.7,.2,1)}
.draw:hover,.draw:focus-visible{background-size:100% 1.5px}
```
