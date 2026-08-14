---
name: andy-liquid
description: Premium liquid and glass effects for modern applications. Integrates Three.js 3D liquid simulations, CSS glassmorphism, and high-end visual design principles for web, mobile, and materials.
---

# Andy Liquid Skill

> Premium liquid and glass effects that elevate any interface from template to agency-tier.

## When to Use

Use this skill when the brief includes:
- "liquid", "glass", "glassmorphism", "fluid", "premium", "high-end"
- Interactive 3D effects
- Apple-style design language
- $150k+ agency-level polish
- Physics-based animations
- Magnetic hover effects

## Core Components

### 1. LiquidCanvas (Three.js 3D)

**Use for**: Hero sections, landing pages, portfolio headers, immersive experiences

```tsx
import { LiquidCanvas } from '@andy-liquid/react'

<LiquidCanvas
  text={["Premium", "Design"]}
  subText="Interactive Experience"
  tagline="Built with Three.js"
  intensity={7}              // 1-10, default 7
  metalness={0.35}           // 0-1, chrome feel
  roughness={0.45}           // 0-1, matte vs glossy
  backgroundColor="#fafafa"
  textColor="#1d1d1f"
/>
```

**Performance**: GPU-intensive, auto-degrades on low-end devices

### 2. GlassPanel (CSS Glassmorphism)

**Use for**: Cards, modals, navigation, overlays, tooltips

```tsx
import { GlassPanel } from '@andy-liquid/react'

<GlassPanel
  variant="medium"    // subtle | medium | strong
  shape="rect"        // pill | rect
  glow={true}
>
  <h2>Premium Content</h2>
</GlassPanel>
```

**A11y**: Auto-fallback for `prefers-reduced-transparency`

### 3. FluidButton (Magnetic Interaction)

**Use for**: CTAs, primary actions, interactive elements

```tsx
import { FluidButton } from '@andy-liquid/react'

<FluidButton
  variant="primary"
  magnetic={true}
  ripple={true}
  icon={<ArrowRight />}
>
  Get Started
</FluidButton>
```

**Physics**: Spring-based magnetic attraction with 60fps smoothing

## Design Decision Tree

### Step 1: Read the Brief

Extract signals:
- **Device target**: Web desktop → LiquidCanvas, Mobile → GlassPanel only
- **Performance budget**: High-end → full effects, Mid-range → CSS only
- **Visual intensity**: Calm → subtle glass, Bold → strong glass + magnetic
- **Audience**: B2B → subtle, Consumer → medium, Agency/Portfolio → strong

### Step 2: Select Effect Intensity

Based on MOTION_INTENSITY dial (from design-taste-frontend):

| Intensity | LiquidCanvas | GlassPanel | FluidButton |
|-----------|--------------|------------|-------------|
| 1-3       | ❌ No        | subtle     | ripple only |
| 4-6       | ❌ No        | medium     | ripple + scale |
| 7-8       | ✅ Yes       | strong     | magnetic + ripple |
| 9-10      | ✅ Yes       | strong + glow | magnetic + custom |

### Step 3: Performance Tier Detection

Auto-detect or manually set:

```tsx
import { getPerformanceTier } from '@andy-liquid/core'

const tier = getPerformanceTier() // 'high' | 'medium' | 'low'

// High: Full LiquidCanvas + strong glass
// Medium: CSS glass + magnetic buttons
// Low: Static gradients + basic transitions
```

## Implementation Patterns

### Pattern 1: Hero with Liquid Background

```tsx
export default function Hero() {
  return (
    <div className="relative min-h-screen">
      <LiquidCanvas
        text={["Andy", "Liquid"]}
        intensity={8}
      />
      <div className="relative z-10 flex items-center justify-center min-h-screen">
        <GlassPanel variant="strong" shape="rect">
          <h1>Premium Design System</h1>
          <FluidButton magnetic>Explore</FluidButton>
        </GlassPanel>
      </div>
    </div>
  )
}
```

### Pattern 2: Glass Navigation

```tsx
export function GlassNav() {
  return (
    <nav className="fixed top-6 left-1/2 -translate-x-1/2 z-50">
      <GlassPanel variant="medium" shape="pill">
        <div className="flex items-center gap-6 px-6 py-3">
          <FluidButton variant="ghost" magnetic>Home</FluidButton>
          <FluidButton variant="ghost" magnetic>Work</FluidButton>
          <FluidButton variant="primary">Contact</FluidButton>
        </div>
      </GlassPanel>
    </nav>
  )
}
```

### Pattern 3: Card Grid with Glass

```tsx
export function FeatureGrid() {
  return (
    <div className="grid grid-cols-3 gap-6">
      {features.map((feature) => (
        <GlassPanel key={feature.id} variant="subtle" shape="rect">
          <div className="p-8">
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </div>
        </GlassPanel>
      ))}
    </div>
  )
}
```

## Performance Guidelines

### GPU Optimization

✅ **DO**:
- Use `transform` and `opacity` for animations
- Apply `backdrop-filter` only to fixed/sticky elements
- Limit LiquidCanvas to hero sections
- Use `will-change: transform` sparingly

❌ **DON'T**:
- Animate `width`, `height`, `top`, `left`
- Apply blur to scrolling containers
- Use multiple LiquidCanvas instances
- Nest glass panels more than 2 levels deep

### Mobile Considerations

```tsx
import { useMediaQuery } from './hooks'

export function ResponsiveHero() {
  const isMobile = useMediaQuery('(max-width: 768px)')

  if (isMobile) {
    // Fallback to static gradient
    return <StaticGradientHero />
  }

  return <LiquidCanvas {...props} />
}
```

## Accessibility

All components include:
- `prefers-reduced-transparency` fallback
- `prefers-reduced-motion` support
- Keyboard navigation
- Screen reader compatibility
- WCAG AA contrast ratios

## Design Tokens

### Glass Variants

```css
/* Subtle: 12px blur, 8% opacity */
--glass-subtle-blur: 12px;
--glass-subtle-opacity: 0.08;

/* Medium: 24px blur, 12% opacity */
--glass-medium-blur: 24px;
--glass-medium-opacity: 0.12;

/* Strong: 40px blur, 18% opacity */
--glass-strong-blur: 40px;
--glass-strong-opacity: 0.18;
```

### Motion Presets

```typescript
// Spring physics
const SPRING_PRESETS = {
  gentle: { stiffness: 100, damping: 20 },
  bouncy: { stiffness: 300, damping: 15 },
  stiff: { stiffness: 400, damping: 30 },
}

// Easing curves
const EASING = {
  fluid: 'cubic-bezier(0.32, 0.72, 0, 1)',
  elastic: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
}
```

## Anti-Patterns

❌ **Don't** use generic glassmorphism everywhere:
- Public sector / government sites
- B2B enterprise dashboards (unless brand calls for it)
- Accessibility-critical interfaces
- Content-heavy reading experiences

❌ **Don't** combine all effects at once:
- LiquidCanvas + strong glass + magnetic on every element = overwhelming

✅ **Do** use strategically:
- Hero: LiquidCanvas
- Navigation: Medium glass
- CTAs: Magnetic buttons
- Cards: Subtle glass

## Testing Checklist

Before shipping:
- [ ] Test on low-end device (throttle CPU 6x in DevTools)
- [ ] Verify `prefers-reduced-transparency` fallback
- [ ] Check mobile touch interactions
- [ ] Measure Lighthouse performance score (target >90)
- [ ] Test dark mode appearance
- [ ] Verify keyboard navigation
- [ ] Check screen reader announcements

## Credits

Built upon:
- threejs-components by Kevin Levron
- liquid-effect-animation by StarKnightt
- taste-skill by Leonxlnx
- high-end-visual-design principles

## Installation

```bash
npm install @andy-liquid/react
# or
pnpm add @andy-liquid/react
# or
bun add @andy-liquid/react
```

Import styles in your app:

```tsx
import '@andy-liquid/core/styles'
```

## Support

- Documentation: https://andy-liquid.dev
- GitHub: https://github.com/AIPMAndy/andy-liquid
- Issues: https://github.com/AIPMAndy/andy-liquid/issues
