# Hamburger icon's middle bar lingers when opening into an X (mobile only)

**Symptom:** on real phones, tapping the mobile nav hamburger to open it shows the middle bar still visible for a beat after the outer two bars have started rotating into the X shape. Not reproducible in desktop browser DevTools with mobile viewport emulation — it only shows up on actual touch hardware.

**Root cause:** the icon is three `<span>` bars (`_includes/header.html`). Opening added the `.open` class, which drove two *independently timed* CSS transitions that had to land in sync purely by hand-tuned coincidence:

```css
.hamburger span {
  transition: transform 0.2s ease;
}

.hamburger span:nth-child(2) {
  transition: opacity 0.05s ease 0.15s;
}

.hamburger.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.hamburger.open span:nth-child(2) { opacity: 0; transition: opacity 0.05s ease; }
.hamburger.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
```

- Outer bars (1 and 3): animate `transform` (translate + rotate) over 200ms.
- Middle bar (2): animates `opacity` over a separate, much shorter 50ms transition.

These are two unrelated transition clocks on two different CSS properties. They were tuned by eye to *look* synced (fade out fast while rotation is still in progress), and a first pass at this already happened once (commit `0eac6d7`, "Retune hamburger icon transition timing to fix lingering middle bar") — it adjusted the duration/delay numbers but kept the same two-clock structure. Desktop DevTools mobile emulation just resizes the viewport; it doesn't emulate real touch-device GPU compositing, so the clocks appeared in sync there while still drifting apart on actual phone hardware, where `transform` (translate+rotate) and `opacity` transitions can be scheduled/painted on different frames under load.

**Fix:** stop syncing two clocks and put everything on one. Collapse the middle bar with `transform: scaleX(0)` instead of an opacity fade, using the exact same `transition: transform 0.2s ease` as the outer bars:

```css
.hamburger span {
  display: block;
  width: 20px;
  height: 2px;
  background: var(--text);
  transition: transform 0.2s ease;
}

.hamburger.open span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.hamburger.open span:nth-child(2) { transform: scaleX(0); }
.hamburger.open span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
```

All three bars now animate the same property, with the same duration and easing, driven by the same class toggle — there's no separate timing value left to drift out of sync, on any device.

**Files touched:** `assets/css/style.css`.

**Prevention:**
- When multiple elements need to look synchronized in a CSS transition, don't hand-tune two separate `transition` declarations (different properties and/or durations) to coincide — put them on the same property/duration/easing so the browser can't desync them under jank.
- Desktop DevTools device emulation is viewport-only; it does not reproduce real mobile GPU compositing behavior. Any animation/timing fix aimed at a mobile-only symptom needs verification on an actual phone before being considered resolved.
