"use client"

import { useEffect, useRef, useMemo, useState } from 'react'
import type { LiquidCanvasConfig } from '@andy-liquid/core'
import { initLiquidEffect } from '@andy-liquid/core'

export interface LiquidCanvasProps extends Omit<LiquidCanvasConfig, 'text'> {
  text?: string | string[]
  className?: string
  style?: React.CSSProperties
}

/**
 * LiquidCanvas Component
 * Three.js powered 3D liquid distortion effect
 * Based on liquid-effect-animation by StarKnightt
 */
export function LiquidCanvas({
  text,
  subText,
  tagline,
  backgroundColor = '#fafafa',
  textColor = '#1d1d1f',
  intensity = 7,
  metalness = 0.35,
  roughness = 0.45,
  displacementScale = 2,
  enableRain = false,
  className = '',
  style = {},
}: LiquidCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [isClient, setIsClient] = useState(false)

  // Ensure we're on client side
  useEffect(() => {
    setIsClient(true)
  }, [])

  // Convert string to array if needed and memoize config
  const config = useMemo<LiquidCanvasConfig>(() => {
    const textArray = text ? (Array.isArray(text) ? text : [text]) : undefined
    return {
      text: textArray,
      subText,
      tagline,
      backgroundColor,
      textColor,
      intensity,
      metalness,
      roughness,
      displacementScale,
      enableRain,
    }
  }, [text, subText, tagline, backgroundColor, textColor, intensity, metalness, roughness, displacementScale, enableRain])

  useEffect(() => {
    if (!isClient || !canvasRef.current) return

    const app = initLiquidEffect(canvasRef.current, config)

    return () => {
      if (app && app.dispose) {
        app.dispose()
      }
    }
  }, [isClient, config])

  // Don't render anything on server
  if (!isClient) {
    return null
  }

  return (
    <div
      className={`liquid-canvas-container ${className}`}
      style={{
        position: 'fixed',
        inset: 0,
        margin: 0,
        width: '100%',
        height: '100%',
        touchAction: 'none',
        overflow: 'hidden',
        ...style,
      }}
    >
      <canvas
        ref={canvasRef}
        id="liquid-canvas"
        style={{
          position: 'fixed',
          inset: 0,
          width: '100%',
          height: '100%',
        }}
      />
    </div>
  )
}
