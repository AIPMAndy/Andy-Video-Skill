"use client"

import { useEffect, useRef } from 'react'
import { RippleEffect } from '@andy-liquid/core'
import type { RippleConfig } from '@andy-liquid/core'

/**
 * Hook for ripple effect
 */
export function useRipple(config?: RippleConfig) {
  const ref = useRef<HTMLElement>(null)
  const effectRef = useRef<RippleEffect | null>(null)

  useEffect(() => {
    if (!ref.current) return

    effectRef.current = new RippleEffect(ref.current, config)

    return () => {
      effectRef.current?.destroy()
    }
  }, [config])

  return ref
}
