"use client"

import { useEffect, useRef } from 'react'
import { MagneticEffect } from '@andy-liquid/core'
import type { MagneticConfig } from '@andy-liquid/core'

/**
 * Hook for magnetic hover effect
 */
export function useMagneticHover(config?: MagneticConfig) {
  const ref = useRef<HTMLElement>(null)
  const effectRef = useRef<MagneticEffect | null>(null)

  useEffect(() => {
    if (!ref.current) return

    effectRef.current = new MagneticEffect(ref.current, config)

    return () => {
      effectRef.current?.destroy()
    }
  }, [config])

  return ref
}
