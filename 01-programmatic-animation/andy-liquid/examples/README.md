# Quick Start Examples

## Example 1: Simple Hero with Liquid Background

```tsx
import { LiquidCanvas } from '@andy-liquid/react'

export default function Hero() {
  return (
    <LiquidCanvas
      text={["Welcome", "to Andy Liquid"]}
      subText="Premium Effects"
      tagline="Built with Three.js • React • TypeScript"
      intensity={7}
    />
  )
}
```

## Example 2: Glass Card Grid

```tsx
import { GlassPanel } from '@andy-liquid/react'

export default function Features() {
  const features = [
    { title: 'Liquid Canvas', description: '3D liquid distortion effects' },
    { title: 'Glass Panels', description: 'CSS glassmorphism' },
    { title: 'Fluid Buttons', description: 'Magnetic hover effects' },
  ]

  return (
    <div className="grid grid-cols-3 gap-6 p-12">
      {features.map((feature) => (
        <GlassPanel key={feature.title} variant="medium" shape="rect">
          <div className="p-8">
            <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
            <p className="text-sm opacity-70">{feature.description}</p>
          </div>
        </GlassPanel>
      ))}
    </div>
  )
}
```

## Example 3: Magnetic Button

```tsx
import { FluidButton } from '@andy-liquid/react'

export default function CTA() {
  return (
    <FluidButton
      variant="primary"
      magnetic={true}
      ripple={true}
      icon={<span>→</span>}
      onClick={() => console.log('Clicked!')}
    >
      Get Started
    </FluidButton>
  )
}
```

## Example 4: Complete Landing Page

```tsx
import { LiquidCanvas, GlassPanel, FluidButton } from '@andy-liquid/react'

export default function Landing() {
  return (
    <div className="relative">
      {/* Background */}
      <LiquidCanvas
        text={["Andy", "Liquid"]}
        subText="Premium Design System"
        intensity={8}
      />

      {/* Content */}
      <div className="relative z-10 min-h-screen flex items-center justify-center">
        <GlassPanel variant="strong" shape="rect">
          <div className="p-12 max-w-md text-center">
            <h1 className="text-4xl font-bold mb-4">
              Premium Liquid Effects
            </h1>
            <p className="mb-8 opacity-70">
              Elevate your designs with high-end liquid and glass effects
            </p>
            <FluidButton variant="primary" magnetic>
              Explore Components
            </FluidButton>
          </div>
        </GlassPanel>
      </div>
    </div>
  )
}
```

## Example 5: Glass Navigation

```tsx
import { GlassPanel, FluidButton } from '@andy-liquid/react'

export default function Nav() {
  return (
    <nav className="fixed top-6 left-1/2 -translate-x-1/2 z-50">
      <GlassPanel variant="medium" shape="pill">
        <div className="flex items-center gap-4 px-6 py-3">
          <FluidButton variant="ghost" magnetic>Home</FluidButton>
          <FluidButton variant="ghost" magnetic>About</FluidButton>
          <FluidButton variant="ghost" magnetic>Work</FluidButton>
          <FluidButton variant="primary">Contact</FluidButton>
        </div>
      </GlassPanel>
    </nav>
  )
}
```

## Installation

```bash
npm install @andy-liquid/react
# or
pnpm add @andy-liquid/react
# or
bun add @andy-liquid/react
```

Import styles:

```tsx
import '@andy-liquid/core/styles'
```

## Next Steps

- View full documentation at [andy-liquid.dev](https://andy-liquid.dev)
- Explore more examples in `/examples`
- Read design principles in `/design/principles.md`
- Check out the Agent Skill in `/skills/andy-liquid-skill`
