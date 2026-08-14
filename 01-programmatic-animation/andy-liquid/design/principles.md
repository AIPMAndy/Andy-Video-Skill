# Design Principles

> High-end visual design principles for Andy Liquid

## Philosophy

Andy Liquid follows three core principles:

1. **Anti-Slop**: Never generate templated, generic-looking interfaces
2. **Performance-First**: GPU-accelerated, 60fps, mobile-optimized
3. **Accessibility**: Progressive enhancement with graceful degradation

## Visual Language

### Texture Archetypes

**Ethereal Glass** (Tech/SaaS/AI)
- Deep OLED blacks (`#050505`)
- Radial mesh gradients (purple/emerald orbs)
- Heavy `backdrop-blur-2xl`
- Wide geometric Grotesk typography

**Editorial Luxury** (Lifestyle/Agency)
- Warm creams (`#FDFBF7`)
- Muted sage or espresso tones
- Variable Serif fonts for headings
- Subtle film-grain overlay

**Soft Structuralism** (Consumer/Health)
- Silver-grey or white backgrounds
- Massive bold Grotesk typography
- Soft, diffused ambient shadows

## Component Architecture

### Double-Bezel Pattern

Never place elements flatly. Use nested enclosures:

```tsx
<div className="p-2 bg-black/5 rounded-[2rem] ring-1 ring-black/5">
  {/* Outer shell */}
  <div className="bg-white rounded-[calc(2rem-0.5rem)] shadow-inner">
    {/* Inner core */}
    Content
  </div>
</div>
```

### Button-in-Button Icons

Trailing icons get their own circular wrapper:

```tsx
<button className="rounded-full px-6 py-3">
  <span>Click me</span>
  <span className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center">
    →
  </span>
</button>
```

## Motion Choreography

### Fluid Easing

Never use `linear` or default `ease-in-out`. Always custom cubic-bezier:

```css
--ease-fluid: cubic-bezier(0.32, 0.72, 0, 1);
--ease-elastic: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

### Spring Physics

All interactive motion uses spring physics:

```typescript
{
  gentle: { stiffness: 100, damping: 20 },
  bouncy: { stiffness: 300, damping: 15 },
}
```

### Magnetic Attraction

Elements follow cursor with smooth interpolation:

```typescript
// Calculate magnetic force
const dx = mouseX - elementX
const dy = mouseY - elementY
const distance = Math.sqrt(dx * dx + dy * dy)
const force = (1 - distance / maxDistance) * strength
```

## Spatial Rhythm

### Macro-Whitespace

Double standard padding:
- Sections: `py-24` to `py-40`
- Cards: `p-8` to `p-12`
- Buttons: `px-6 py-3`

### Micro-Details

- Eyebrow tags: `text-[10px] uppercase tracking-[0.2em]`
- Hairline borders: `border border-white/10`
- Inner highlights: `shadow-[inset_0_1px_0_rgba(255,255,255,0.15)]`

## Performance Guardrails

### GPU-Safe Animation

✅ Animate: `transform`, `opacity`
❌ Never animate: `width`, `height`, `top`, `left`

### Blur Constraints

- Apply `backdrop-filter` only to fixed/sticky elements
- Never apply to scrolling containers
- Use sparingly (GPU intensive)

### Z-Index Discipline

Reserve for systemic layers only:
- Sticky nav: `z-40`
- Modals: `z-50`
- Tooltips: `z-60`

## Color Philosophy

### Light Mode

- Background: `#fafafa` (not pure white)
- Text: `#1d1d1f` (not pure black)
- Glass: `rgba(255, 255, 255, 0.12)`

### Dark Mode

- Background: `#0a0a0a` (OLED black)
- Text: `#fafafa`
- Glass: `rgba(255, 255, 255, 0.08)`

## Typography

### Font Stack

```css
font-family: -apple-system, "SF Pro Display", "Helvetica Neue", Arial, sans-serif;
```

### Scale

- Hero: `min(13vw, 19vh)` - responsive to viewport
- H1: `text-5xl` to `text-6xl`
- Body: `text-base` to `text-lg`
- Eyebrow: `text-[10px]` to `text-xs`

### Weight & Tracking

- Headlines: `font-bold` (700), `-tracking-tight`
- Body: `font-normal` (400)
- Eyebrows: `font-semibold` (600), `tracking-[0.2em]`

## Accessibility

### Reduced Transparency

```css
@media (prefers-reduced-transparency: reduce) {
  .liquid-glass {
    background: rgb(255 255 255 / .96);
    backdrop-filter: none;
  }
}
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Contrast

Minimum WCAG AA: 4.5:1 for text, 3:1 for UI components

## Anti-Patterns

❌ **Don't**:
- Use AI-purple gradients
- Center everything
- Make three equal feature cards
- Apply glassmorphism to everything
- Use infinite-loop micro-animations everywhere
- Default to Inter + slate-900

✅ **Do**:
- Read the brief first
- Match the audience and context
- Use effects strategically
- Provide fallbacks
- Test on real devices

## Inspiration Sources

- Apple Marketing pages
- Linear.app
- Awwwards winners
- High-end agency work ($150k+ budgets)
- Premium consumer brands

## Execution Checklist

Before shipping:
- [ ] Vibe archetype selected based on brief
- [ ] All major cards use Double-Bezel
- [ ] Custom cubic-bezier transitions
- [ ] Section padding ≥ `py-24`
- [ ] Scroll entry animations present
- [ ] Mobile collapse to single-column
- [ ] GPU-safe animations only
- [ ] Backdrop-blur on fixed elements only
- [ ] Reads as "$150k agency build"
