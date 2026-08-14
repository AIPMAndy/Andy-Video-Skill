'use client'

import dynamic from 'next/dynamic'
import '@andy-liquid/core/style.css'

const LiquidCanvas = dynamic(
  () => import('@andy-liquid/react').then(mod => ({ default: mod.LiquidCanvas })),
  { ssr: false }
)

export default function TestPage() {
  return (
    <LiquidCanvas
      text={["Liquid", "Effect"]}
      subText="Interactive UI Component"
      tagline="Built with Three.js • React • Tailwind CSS"
      backgroundColor="#fafafa"
      textColor="#1d1d1f"
    />
  )
}
