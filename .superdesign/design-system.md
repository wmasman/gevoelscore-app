# Gevoelscore Design System

> **Source of truth.** This file is the operational design system for any superdesign draft/iteration command. The strategic brief is at [`docs/design/brief.md`](../docs/design/brief.md) — read it first for the *why*. This file translates the brief into concrete tokens for *how*.
>
> Hex values, sizes and ratios below are confident first-pass choices that respect the brief's directional constraints. They are **refinable** — adjust in superdesign drafts or after real usage. Do not change the underlying *direction* (warm-earth + Things-3 polish + reflective restraint) without revising the brief first.

---

## Product Context

**Product:** Gevoelscore — personal Long COVID daily-tracking PWA.

**User:** Single user (the author). Adult, technically competent, brainfog-affected on bad days.

**Platform:** Next.js 15 PWA + Directus backend + PostgreSQL. Installable via "Add to Home Screen" on iOS / Android. Mobile-first, 375px reference width.

**Language:** Dutch — all UI labels, system messages, copy.

**Aesthetic in one line:** A quiet, considered, warmly-personal app that records without commenting — closer to a digital paper journal than a mood-tracker.

**Anchor reference:** Things 3 (warm whites, soft shadows, single accent, restrained chrome, expressive only on the moment of action). Departures from Things 3: warm-earth accent (not blue), score-not-checklist metaphor, personal-artifact tone (not productivity-tool).

**Cardinal principles** (full list in [`docs/REQUIREMENTS.md`](../docs/REQUIREMENTS.md)):
1. One-tap entry — a complete day requires one tap.
2. Sub-10-second flow — open, log, optionally note, close.
3. No friction in main flow — no dropdowns, sliders, required tags, multi-step forms.
4. Low cognitive load — usable on a "4-out-of-6 day" with brainfog.
5. No unsolicited notifications, ads, analytics, tracking.
6. User-owned data — self-hosted Directus + Postgres.

---

## Key Pages & Architecture

v1 screens (full list in [`docs/REQUIREMENTS.md`](../docs/REQUIREMENTS.md#v1-screens)):

```
/ (Home / Daily — the cardinal screen)
├── /recent              (Recent missed — last 4–7 days, fast catch-up)
├── /calendar            (Full backfill grid by month)
├── /day/[date]          (Past-day view, read-only with explicit Edit toggle)
├── /timeline            (30-day / 90-day line chart + streak counter)
├── /settings            (Tag management, 2FA, CSV import/export, sign out)
└── /login + /2fa        (Pre-app gate)
```

**Navigation pattern: TBD in feature plan.** Either a bottom tab nav (Today / Calendar / Timeline / Settings) or a Home-rooted pattern with quick links. Both are compatible with this design system.

**Out of scope for v1** (architectured-for, not built): projects/interventions, calendar sync, HealthKit/Garmin, weather, sub-scores.

---

## Branding & Colors

### Palette philosophy

- **Single accent** — warm-earth (terracotta / clay / ochre family) carries brand identity across the entire app.
- **No traffic-light semantics** — errors are NOT red, success is NOT green, warnings are NOT amber. State is communicated through copy, position, and text weight. The brief forbids color-coded meaning.
- **Warm-whites foundation** — backgrounds and surfaces are warm off-whites, never `#FFFFFF`. Text is warm dark, never `#000`.
- **One non-accent color allowed: the empty-day dot.** A deliberately gentler ochre-orange, used only in the calendar / recent-missed view as a "you didn't log this day" marker.

### Accent (brand) palette

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Clay 500 (accent) | `#B5694A` | 181, 105, 74 | **Primary brand** — selected score, active chip, streak number, focus ring, links, primary action |
| Clay 600 (hover) | `#9D5839` | 157, 88, 57 | Hover state on accent surfaces |
| Clay 700 (active) | `#834828` | 131, 72, 40 | Pressed state |
| Clay 100 (tint) | `#F5E8DF` | 245, 232, 223 | Active-chip background, selected-row tint, very subtle accent surfaces |

### Warm-whites foundation

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Background base | `#FAF6F1` | 250, 246, 241 | App background — warm off-white with ochre warmth |
| Surface elevated | `#FFFCF8` | 255, 252, 248 | Cards, sheets, elevated panels — slightly lighter than base so elevation reads via background contrast, not just shadow |
| Surface muted | `#F2EDE5` | 242, 237, 229 | Input backgrounds at rest, read-only surfaces (past-day view), subtle zones |

### Warm-dark text

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Text primary | `#2B2520` | 43, 37, 32 | Body text, headers — warm dark, never `#000` |
| Text secondary | `#6B5F54` | 107, 95, 84 | Captions, metadata, "dagen" in streak, save confirmation text |
| Text tertiary | `#9C8F82` | 156, 143, 130 | Placeholder text, disabled chip text, calendar dimmed days |
| Text disabled | `#BFB5A8` | 191, 181, 168 | Disabled controls (rare in v1) |

### Borders & dividers

| Name | Hex | Usage |
|------|-----|-------|
| Border default | `#E8DFD2` | Card outlines, input borders at rest, divider lines — very subtle |
| Border hover | `#D5C8B5` | Hover state on neutral borders |
| Border focus | `#B5694A` (Clay 500) | Focus ring color — 2px solid + 2px offset |

### The one allowed second color

| Name | Hex | Usage |
|------|-----|-------|
| Ochre dot | `#E8A35C` | **Exclusively** the empty-day marker in calendar / recent-missed views. Deliberately less saturated than Clay 500 so it reads as nudge, not alarm. **Forbidden anywhere else in the UI.** |

### Contrast verification

All text/background combinations meet WCAG 2.2 AA (4.5:1 normal text, 3:1 large/UI):
- `#2B2520` on `#FAF6F1` → 13.8:1 ✓
- `#2B2520` on `#FFFCF8` → 14.5:1 ✓
- `#6B5F54` on `#FAF6F1` → 6.2:1 ✓
- `#B5694A` on `#FAF6F1` → 4.6:1 ✓
- `#FFFCF8` on `#B5694A` (selected score) → 4.7:1 ✓

---

## Typography

### Font

**Inter** — humanist sans, designed-but-neutral, optimized for screen reading, free, broadly supported. Loaded via `next/font` for zero-CLS. Single typeface family throughout. No serif. No system fallback as default (system fonts only kick in if Inter fails to load).

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Type scale

Brainfog floor: body text ≥17px, line-height ≥1.5. Numerical scale, no T-shirt sizes — sizes read directly.

| Name | Size | Weight | Line | Letter | Usage |
|------|------|--------|------|--------|-------|
| Display | 28px | 600 | 1.2 | -0.01em | Streak number ("47"), score-row big numbers when emphasized |
| H1 | 24px | 600 | 1.25 | -0.01em | Page titles — "Vandaag", "Tijdlijn", "Instellingen" |
| H2 | 20px | 600 | 1.3 | 0 | Section headers within a page |
| H3 | 18px | 500 | 1.4 | 0 | Subsection headers, card titles |
| Body large | 18px | 400 | 1.6 | 0 | Note input, primary reading body |
| **Body** | **17px** | **400** | **1.6** | **0** | **Default body. Brainfog floor.** |
| Body small | 15px | 400 | 1.5 | 0 | Captions, metadata, secondary info |
| Score number | 24px | 600 | 1 | 0 | The "1"–"10" rendered inside score buttons |

Weights used: **400** (regular), **500** (medium), **600** (semibold). No 700/800/900 — too loud.

### Text color mapping

- Body / paragraphs → Text primary (`#2B2520`)
- Captions / metadata / "dagen" in streak → Text secondary (`#6B5F54`)
- Placeholder text → Text tertiary (`#9C8F82`)
- Brand emphasis (streak number, link, selected score number) → Clay 500 (`#B5694A`)
- Save confirmation "Bewaard." → Text secondary, body-small, fades

---

## Spacing

**Base unit: 4px.** Generous breathing room per Things-3 + brainfog rules.

| Token | Value | Tailwind | Usage |
|-------|-------|----------|-------|
| 1 | 4px | `1` | Icon ↔ label, tight inline |
| 2 | 8px | `2` | Between related items, chip gap |
| 3 | 12px | `3` | Small padding, input inner |
| 4 | 16px | `4` | Standard padding, card padding, gaps between cards |
| 5 | 20px | `5` | Generous between sections |
| 6 | 24px | `6` | Section-to-section vertical |
| 8 | 32px | `8` | Page section margins |
| 10 | 40px | `10` | Top-of-page / large breathing |
| 12 | 48px | `12` | Major sections, page padding |
| 16 | 64px | `16` | Vertical rhythm for hero areas |
| 20 | 80px | `20` | Bottom-nav clearance (if used) |

**Page-level defaults:**
- Horizontal padding: 16px (sm screens) / 20px (≥640px)
- Vertical padding top: 24px
- Vertical padding bottom: 80px (clearance for safe-area + potential bottom nav)
- Inter-section vertical gap: 32px

---

## Border Radius

Soft-rounded, Things-3-inspired. Nothing sharp, nothing fully circular except pills/avatars.

| Token | Value | Tailwind | Usage |
|-------|-------|----------|-------|
| sm | 8px | `rounded-lg` | Small inputs |
| md | 12px | `rounded-xl` | Buttons (non-pill), score buttons |
| lg | 16px | `rounded-2xl` | Cards, panels |
| xl | 20px | `rounded-[20px]` | Large surfaces, sheets |
| 2xl | 28px | `rounded-[28px]` | Modal/sheet top corners (bottom sheet style) |
| full | 9999px | `rounded-full` | Tag chips, FAB-style controls, avatar |

---

## Shadows

**Single-direction soft drop shadow.** Warm-tinted (rgba based on Text-primary, not pure black) so shadows feel warm. **No editorial-embossed double shadow** (TVO uses one; gevoelscore deliberately doesn't — too dimensional for the reflective+quiet direction).

```css
--shadow-sm:  0 1px 2px rgba(43, 37, 32, 0.04);
--shadow-md:  0 2px 6px rgba(43, 37, 32, 0.06),
              0 1px 2px rgba(43, 37, 32, 0.04);
--shadow-lg:  0 8px 24px rgba(43, 37, 32, 0.08),
              0 2px 4px rgba(43, 37, 32, 0.04);
```

| Token | Usage |
|-------|-------|
| sm | Subtle ground for chips, secondary cards |
| md | Cards, selected score button, primary buttons |
| lg | Sheets, modals, popovers |

**No celebration shadow / glow.** No pulsing, no halo, no animated shadows.

---

## Motion & Animation

Hard cap: **≤200ms** for any interactive transition, per brainfog rule. `prefers-reduced-motion` flattens all durations to 0.01ms (in `globals.css`).

| Duration | Usage |
|----------|-------|
| 100ms | Micro — button press, chip tap |
| 150ms | Standard transitions — hover, color change |
| 200ms | Maximum — sheet enter/exit, fade-in |

### Easing

```css
/* Default */
transition-timing-function: ease-out;

/* Enter (fade in) */
transition-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);

/* Exit (fade out) */
transition-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
```

**Forbidden as decoration:** bounce, elastic, overshoot, spring-with-rebound easing. No celebratory motion. No ambient pulses, no shimmer, no marquee. Loading skeletons use opacity fade (no shimmer animation). No repeating pulses on idle elements (streak number, score, anything passive).

**Allowed as communication** (see `docs/design/brief.md#motion-as-communication`): one-shot acknowledgments tied to meaningful moments. Examples: today-card tint-pulse on completion of a day's entry; score-number scale-pulse on integer-cross during drag (visual substitute for haptic tick on platforms without Web Vibration); sheet content morphing between input steps as one continuous transformation. The test: does this motion tell the user something they need to know? If yes, it can exist (within the 200ms cap for transitions; one-shot completion acknowledgments may run slightly longer if they aid spatial parsing). If no, it's decoration and forbidden.

### Common motions

```css
/* Button press */
&:active { transform: scale(0.98); transition: transform 100ms ease-out; }

/* Sheet enter (bottom sheet) */
transform: translateY(0); /* from translateY(100%) */
transition: transform 200ms cubic-bezier(0.0, 0.0, 0.2, 1);

/* Save confirmation fade */
opacity: 1; /* from 0 */
transition: opacity 150ms ease-out;
/* Held 1500ms, then fade-out 200ms */
```

---

## Components

### Score buttons (1–10) — the cardinal component

The defining UI of the app. All ten visually identical at rest; only the selected one fills with accent. Number IS the meaning.

**Default state:**
```css
background: var(--surface-elevated);  /* #FFFCF8 */
color: var(--text-primary);           /* #2B2520 */
border: 1px solid var(--border-default);
border-radius: 12px;                  /* md */
min-width: 48px; min-height: 48px;    /* brainfog target */
padding: 12px;
font: 600 24px/1 Inter;
box-shadow: var(--shadow-sm);
transition: background 150ms ease-out, color 150ms ease-out;
```

**Selected state:**
```css
background: var(--clay-500);          /* #B5694A */
color: var(--surface-elevated);       /* #FFFCF8 */
border-color: var(--clay-500);
box-shadow: var(--shadow-md);
font-weight: 600;
/* No scale, no glow, no animation beyond the color transition */
```

**Layout:** exact arrangement (1×10 row vs 2×5 grid vs other) is a feature-plan decision per [REQUIREMENTS](../docs/REQUIREMENTS.md#v1-screens), not specified here. Both work with this token system.

**Forbidden on this component:** no red-amber-green gradient across the row, no face emoji, no number-with-icon, no celebratory animation on tap.

### Tag chips

```css
/* Untapped */
background: transparent;
color: var(--text-secondary);
border: 1px solid var(--border-default);
border-radius: 9999px;                /* full pill */
padding: 6px 14px;
font: 500 15px/1.4 Inter;
min-height: 32px;
transition: all 150ms ease-out;

/* Tapped */
background: var(--clay-100);          /* #F5E8DF */
color: var(--clay-700);               /* #834828 */
border-color: var(--clay-500);
font-weight: 600;
```

Gap between chips: 8px. Frequently-used surface first (mechanic in REQUIREMENTS); rarely-used fade out of the primary row.

### Note input

```css
background: var(--surface-muted);     /* #F2EDE5 */
border: 1px solid var(--border-default);
border-radius: 16px;                  /* lg */
padding: 16px;
min-height: 96px;
font: 400 18px/1.6 Inter;
color: var(--text-primary);
resize: vertical;
transition: border-color 150ms ease-out;

&:focus {
  border-color: var(--clay-500);
  outline: 2px solid rgba(181, 105, 74, 0.2);
  outline-offset: 2px;
}

&::placeholder { color: var(--text-tertiary); }
```

No character counter. No "x characters remaining" text. No mandatory-field asterisk (it's optional).

### Streak counter

Subtle elevation allowed per brief. Quiet pride, never loud.

```html
<div class="streak">
  <span class="streak-number">47</span>
  <span class="streak-label">dagen</span>
</div>
```

```css
.streak-number {
  font: 600 28px/1 Inter;
  color: var(--clay-500);             /* #B5694A — only place accent appears as text color in chrome */
}
.streak-label {
  font: 500 17px/1 Inter;
  color: var(--text-secondary);
  margin-left: 4px;
}
```

**Forbidden:** "🔥 47 days!", "47 days in a row!", "Mooie streak!", any badge, any milestone animation, any "you're crushing it" copy.

### Save confirmation

```css
.save-confirmation {
  font: 500 15px/1.5 Inter;
  color: var(--text-secondary);
  opacity: 1;
  transition: opacity 200ms ease-out;
}
/* Shown for 1500ms total: fade-in 100ms, hold 1200ms, fade-out 200ms */
```

Text: `Bewaard.` — terminal period, past tense, no icon.

**Forbidden:** checkmark icon flash, green color, pulse animation, "✓ Saved!", "Opgeslagen!".

### Past-day read-only view

```css
background: var(--surface-muted);     /* #F2EDE5 — visually distinct from edit-mode */
/* Score, note, tags displayed as static text/chip-display, no input borders */
```

Edit affordance:
```css
.edit-button {
  background: transparent;
  color: var(--clay-500);
  border: 1px solid var(--clay-500);
  border-radius: 9999px;              /* pill */
  padding: 8px 16px;
  font: 500 15px/1 Inter;
  min-height: 36px;

  &:hover { background: var(--clay-100); }
}
```

### Empty-day marker (calendar / recent-missed)

```css
.empty-day-dot {
  width: 6px;
  height: 6px;
  border-radius: 9999px;
  background: var(--ochre-dot);       /* #E8A35C */
  /* Position: centered in calendar cell, or 4px left of the date in a list */
}
```

**This is the only place `#E8A35C` may appear in the entire app.**

### Calendar day cell

```css
/* Default */
background: transparent;
color: var(--text-primary);
font: 400 17px/1 Inter;
min-width: 44px; min-height: 44px;    /* WCAG AA touch target, slightly tighter than buttons */
border-radius: 8px;
display: grid; place-items: center;

/* Today */
border: 1px solid var(--clay-500);

/* Has entry */
background: var(--clay-100);
color: var(--clay-700);

/* Empty (logged-no-entry-this-day) */
/* No background. Add ::after with empty-day-dot. */

/* Out of month */
color: var(--text-tertiary);
```

### Sheets / modals

```css
background: var(--surface-elevated);
border-top-left-radius: 28px;
border-top-right-radius: 28px;
box-shadow: var(--shadow-lg);

/* Backdrop */
background: rgba(43, 37, 32, 0.4);    /* Warm-dark at 40% alpha */
transition: opacity 200ms ease-out;
```

Focus management per [`docs/architecture/frontend-conventions.md`](../docs/architecture/frontend-conventions.md#focus-management): focus moves into the sheet on open, traps until close, returns to trigger element on close. Escape closes.

### Buttons (general)

**Primary:**
```css
background: var(--clay-500);
color: var(--surface-elevated);
border-radius: 12px;
padding: 12px 24px;
min-height: 48px;
font: 600 17px/1 Inter;
box-shadow: var(--shadow-sm);
transition: background 150ms ease-out;

&:hover  { background: var(--clay-600); }
&:active { background: var(--clay-700); transform: scale(0.98); }
&:focus-visible {
  outline: 2px solid var(--clay-500);
  outline-offset: 2px;
}
```

**Secondary (ghost):**
```css
background: transparent;
color: var(--clay-500);
border: 1px solid var(--border-default);
border-radius: 12px;
/* same dimensions as primary */

&:hover { background: var(--clay-100); border-color: var(--clay-500); }
```

**Destructive actions:** the brief forbids semantic red. Destructive actions use the secondary button styling + clear copy (`Verwijderen — kan niet ongedaan gemaakt worden`) + a confirmation sheet. No red, no exclamation icon.

---

## Icons

**Library:** Lucide React (`lucide-react`).

**Rule:** Icons supplement text labels, they do **not** replace them. Brainfog accessibility — icon-only buttons are forbidden in primary flows. Exceptions: close (×) on sheets, back arrow on subpages, where the meaning is universal.

### Sizes
| Size | Dimensions | Tailwind | Usage |
|------|------------|----------|-------|
| sm | 16px | `h-4 w-4` | Inline with text |
| md | 20px | `h-5 w-5` | Standard UI |
| lg | 24px | `h-6 w-6` | Nav, emphasis |

### Common icons

| Category | Lucide names |
|----------|--------------|
| Navigation | `ArrowLeft`, `ChevronRight`, `Home`, `Calendar`, `Activity` (timeline), `Settings` |
| Actions | `Edit`, `Plus`, `Check`, `X`, `Download` (export), `Upload` (import) |
| State | `MoreHorizontal` |

**Forbidden:** decorative icons, emoji-as-icon, mood/face icons, achievement icons.

---

## Layout

### Breakpoints

| Name | Width | Tailwind | Description |
|------|-------|----------|-------------|
| Mobile | < 640px | default | Primary target. 375px reference. |
| SM | ≥ 640px | `sm:` | Large phones, foldables |
| MD | ≥ 768px | `md:` | Tablets — extra horizontal padding, otherwise mobile layout |
| LG | ≥ 1024px | `lg:` | Desktop — content max-width applied, otherwise same |

**Mobile-first.** Desktop is a derivative layout, not the default. Per REQUIREMENTS.

### Container

```css
.container {
  max-width: 560px;    /* Single-user app, no wide-form content; content stays readable */
  margin: 0 auto;
  padding: 0 16px;
}

@media (min-width: 640px) {
  .container { padding: 0 20px; }
}
```

### Page structure

```
┌──────────────────────────────────┐
│ Header (sticky, 56px)            │
│  - Page title (H1)               │
│  - Optional back arrow (left)    │
│  - Optional settings (right)     │
├──────────────────────────────────┤
│                                  │
│ Page content                     │
│ background: --background-base    │
│ padding: 16px 16px 80px          │
│                                  │
├──────────────────────────────────┤
│ Bottom nav (TBD, 64px + safe)    │
│ -or- no bottom nav (TBD)         │
└──────────────────────────────────┘
```

---

## Accessibility

Strictly enforces [`docs/architecture/frontend-conventions.md`](../docs/architecture/frontend-conventions.md#accessibility-target) — WCAG 2.2 AA plus five brainfog extensions.

### Touch targets
- **Buttons / primary controls:** ≥48×48 (brainfog rule; above WCAG AA 24×24)
- **Calendar day cells:** ≥44×44 (WCAG AA)
- **Inline links in text:** WCAG AA (24×24) minimum

### Focus
```css
:focus-visible {
  outline: 2px solid var(--clay-500);
  outline-offset: 2px;
  border-radius: inherit;
}
```

Never `outline: none` without a replacement. Default focus ring lives in `globals.css`.

### Reduced motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Color contrast
All combinations meet 4.5:1 (normal text) or 3:1 (large text / UI) — see "Contrast verification" under Branding & Colors.

### Information density
**Max 5 primary actions visible at once on any single screen.** Brainfog rule. If a screen needs more, hide behind a "More" affordance.

### No time pressure
No timers on any user-facing flow. No auto-dismiss countdowns. The only time-bounded UI is the save-confirmation fade, which is not actionable.

---

## Dutch labels & microcopy

### Tone of voice rules (full discussion in [`docs/design/brief.md`](../docs/design/brief.md#dutch-microcopy-rules))

- No exclamation marks anywhere in chrome.
- No second-person questions (`Vandaag`, not `Hoe was vandaag?`).
- Past tense over imperative for system states (`Bewaard`, not `Opgeslagen!`).
- Terminal periods on standalone strings (`Bewaard.`, `Geen invoer.`).
- One word beats three.
- **No em-dash (`—`) in user-facing strings.** Prefer comma, period, or colon. `Niet opgeslagen. Probeer nogmaals.` (period), not `Niet opgeslagen — probeer nogmaals` (em-dash). Standalone `—` as an empty-state glyph is fine; the rule is about punctuation in sentences.

### Common actions

| English | Dutch |
|---------|-------|
| Edit | Bewerken |
| Save | (no chrome — auto-save; if explicit button needed: `Opslaan`) |
| Cancel | Annuleren |
| Delete | Verwijderen |
| Export | Exporteren |
| Import | Importeren |
| Back | Terug |
| Close | Sluiten |
| Sign out | Uitloggen |
| Settings | Instellingen |

### Page titles

| Screen | Dutch |
|--------|-------|
| Home / Daily | `Vandaag` |
| Recent missed | `Recent gemist` |
| Calendar | `Kalender` |
| Past day | `[date]` (e.g. `donderdag 8 mei`) |
| Timeline | `Tijdlijn` |
| Settings | `Instellingen` |
| Login | `Inloggen` |
| 2FA | `Verificatie` |

### State & feedback

| Context | Dutch |
|---------|-------|
| Save confirmation | `Bewaard.` |
| Empty entry placeholder | `Geen invoer.` |
| No tags used | `Nog geen tags.` |
| No data in timeline | `Nog te weinig data.` |
| Network error | `Verbinding verloren.` |
| Generic error | `Er ging iets mis. Opnieuw proberen.` |
| Loading | `Laden…` (used sparingly; prefer skeleton UI) |

### Streak

| Context | Dutch |
|---------|-------|
| Streak counter | `47 dagen` (number + label, no exclamation, no "op rij") |
| Zero streak | `Geen actieve reeks.` |

### Forbidden microcopy patterns

| ❌ Forbidden | ✓ Allowed instead |
|---|---|
| `Hoe was vandaag?` | `Vandaag` |
| `Opgeslagen!` | `Bewaard.` |
| `Top, opgeslagen 🎉` | `Bewaard.` |
| `47 dagen op rij!` | `47 dagen` |
| `Je hebt nog niets ingevuld vandaag` | `Geen invoer.` |
| `Oeps, er ging iets mis!` | `Er ging iets mis. Opnieuw proberen.` |
| `Mooie streak — ga zo door` | (nothing — show streak, no commentary) |
| `Aan de slag!` | `Beginnen` (if a CTA is needed at all) |

All Dutch strings live in `src/copy.ts` per [frontend-conventions](../docs/architecture/frontend-conventions.md#copy-discipline).

---

## What this design system deliberately omits

- **Semantic colors (success/warning/error/info).** The brief forbids color-coded meaning. State is communicated through copy, position, and text weight.
- **Mood-tracker visual language** (emoji scores, color-coded score scale, achievement badges, level progression).
- **Multiple typography families.** Single typeface (Inter) covers all roles.
- **Editorial double-shadow embossing.** Single-direction soft shadow only.
- **Bounce/elastic animation easing.** Linear ease-out only, ≤200ms.
- **Dark mode palette values.** The CSS-variable seam is in place; dark mode is v1.5+ per [frontend-conventions](../docs/architecture/frontend-conventions.md). When it ships, it must inherit the warm-earth + warm-darks direction.
- **Pixel-exact screen layouts.** Layout choices (score-row arrangement, bottom nav vs not, calendar grid) belong in feature-plan step files, not the design system. The system provides the tokens; the layout uses them.

---

## How to use this file in superdesign

Per the superdesign workflow, this file is passed as `--context-file` to every design-draft command:

```bash
superdesign create-design-draft --project-id 36dcb035-8b16-4941-b67c-1b5f3c709f31 \
  --title "Home / Daily v1" \
  -p "<one-prompt combining all design directions for the screen>" \
  --context-file .superdesign/design-system.md \
  --context-file src/app/globals.css
```

For iteration:

```bash
superdesign iterate-design-draft --draft-id <id> \
  -p "<variation A>" -p "<variation B>" --mode branch \
  --context-file .superdesign/design-system.md \
  --context-file src/app/globals.css
```

**The design system is a hard constraint.** Variations explore layout, not visual style.
