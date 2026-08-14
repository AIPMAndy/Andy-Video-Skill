'use client'

import dynamic from 'next/dynamic'
import { GlassPanel, FluidButton } from '@andy-liquid/react'
import '@andy-liquid/core/style.css'

const LiquidCanvas = dynamic(
  () => import('@andy-liquid/react').then(mod => ({ default: mod.LiquidCanvas })),
  { ssr: false }
)

export default function Home() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-[#fafafa]">
      {/* Liquid Background - Pure Visual */}
      <div className="absolute inset-0 z-0">
        <LiquidCanvas
          text={[]}
          backgroundColor="#fafafa"
          textColor="#1d1d1f"
          intensity={7}
          metalness={0.35}
          roughness={0.45}
          displacementScale={2.5}
          enableRain={false}
        />
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center justify-center min-h-screen px-4">
        {/* Hero - Minimal */}
        <div className="text-center mb-12">
          <h1 className="text-8xl md:text-9xl font-bold text-gray-900 mb-6 tracking-tight">
            Andy Liquid
          </h1>
          <p className="text-2xl md:text-3xl text-gray-600 font-light mb-12">
            Premium Liquid Effects Library
          </p>
          <div className="flex gap-4 justify-center">
            <FluidButton
              variant="primary"
              magnetic
              ripple
              onClick={() => window.open('https://github.com/AIPMAndy/andy-liquid', '_blank')}
            >
              View on GitHub
            </FluidButton>
            <FluidButton
              variant="secondary"
              magnetic
              ripple
              onClick={() => window.location.href = '/test'}
            >
              See Examples
            </FluidButton>
          </div>
        </div>

        {/* Features - Minimal Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl w-full mt-16">
          <GlassPanel variant="subtle" shape="rect" className="p-6 text-center">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Three.js 3D</h3>
            <p className="text-sm text-gray-600">GPU-accelerated liquid effects</p>
          </GlassPanel>

          <GlassPanel variant="subtle" shape="rect" className="p-6 text-center">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Glassmorphism</h3>
            <p className="text-sm text-gray-600">Modern frosted glass UI</p>
          </GlassPanel>

          <GlassPanel variant="subtle" shape="rect" className="p-6 text-center">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Magnetic</h3>
            <p className="text-sm text-gray-600">Smooth spring animations</p>
          </GlassPanel>
        </div>

        {/* Footer Note */}
        <div className="absolute bottom-8">
          <p className="text-sm text-gray-500">
            Built with Three.js • React 19 • Next.js 16
          </p>
        </div>
      </div>
    </div>
  )
}
