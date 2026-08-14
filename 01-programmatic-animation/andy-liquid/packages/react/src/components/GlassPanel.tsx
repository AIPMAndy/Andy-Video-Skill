"use client"

import { forwardRef } from 'react'
import type { ReactNode, HTMLAttributes } from 'react'

export interface GlassPanelProps extends HTMLAttributes<HTMLDivElement> {
  variant?: 'subtle' | 'medium' | 'strong'
  shape?: 'pill' | 'rect'
  border?: boolean
  glow?: boolean
  children: ReactNode
}

/**
 * GlassPanel Component
 * CSS glassmorphism effect with accessibility support
 * Based on design-taste-frontend Apple Liquid Glass approximation
 */
export const GlassPanel = forwardRef<HTMLDivElement, GlassPanelProps>(
  (
    {
      variant = 'medium',
      shape = 'pill',
      border = true,
      glow = false,
      className = '',
      children,
      ...props
    },
    ref
  ) => {
    const classes = [
      'liquid-glass',
      `liquid-glass--${variant}`,
      shape === 'rect' && 'liquid-glass--rect',
      !border && 'liquid-glass--no-border',
      glow && 'liquid-glass--glow',
      className,
    ]
      .filter(Boolean)
      .join(' ')

    return (
      <div ref={ref} className={classes} {...props}>
        {children}
      </div>
    )
  }
)

GlassPanel.displayName = 'GlassPanel'
