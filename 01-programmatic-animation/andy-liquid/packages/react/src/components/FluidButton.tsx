"use client"

import { forwardRef, useRef, useEffect } from 'react'
import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { MagneticEffect, RippleEffect } from '@andy-liquid/core'
import type { MagneticConfig, RippleConfig } from '@andy-liquid/core'

export interface FluidButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost'
  magnetic?: boolean
  magneticConfig?: MagneticConfig
  ripple?: boolean
  rippleConfig?: RippleConfig
  icon?: ReactNode
  children: ReactNode
}

/**
 * FluidButton Component
 * Magnetic hover effect with spring physics and ripple interaction
 * Based on high-end-visual-design principles
 */
export const FluidButton = forwardRef<HTMLButtonElement, FluidButtonProps>(
  (
    {
      variant = 'primary',
      magnetic = false,
      magneticConfig,
      ripple = true,
      rippleConfig,
      icon,
      className = '',
      children,
      ...props
    },
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    _ref
  ) => {
    const buttonRef = useRef<HTMLButtonElement>(null)
    const magneticEffectRef = useRef<MagneticEffect | null>(null)
    const rippleEffectRef = useRef<RippleEffect | null>(null)

    useEffect(() => {
      if (!buttonRef.current) return

      if (magnetic) {
        magneticEffectRef.current = new MagneticEffect(buttonRef.current, magneticConfig)
      }

      if (ripple) {
        rippleEffectRef.current = new RippleEffect(buttonRef.current, rippleConfig)
      }

      return () => {
        magneticEffectRef.current?.destroy()
        rippleEffectRef.current?.destroy()
      }
    }, [magnetic, magneticConfig, ripple, rippleConfig])

    const variantClasses = {
      primary: 'bg-black dark:bg-white text-white dark:text-black',
      secondary: 'bg-transparent border border-black/20 dark:border-white/20',
      ghost: 'bg-transparent hover:bg-black/5 dark:hover:bg-white/5',
    }

    const classes = [
      'liquid-button',
      'liquid-transition',
      'relative',
      'inline-flex',
      'items-center',
      'justify-center',
      'gap-2',
      'rounded-full',
      'px-6',
      'py-3',
      'text-sm',
      'font-medium',
      'transition-all',
      variantClasses[variant],
      magnetic && 'liquid-magnetic',
      className,
    ]
      .filter(Boolean)
      .join(' ')

    return (
      <button ref={buttonRef} className={classes} {...props}>
        <span className="relative z-10 flex items-center gap-2">
          {children}
          {icon && (
            <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-white/10 dark:bg-black/10 transition-transform group-hover:translate-x-0.5 group-hover:-translate-y-0.5 group-hover:scale-105">
              {icon}
            </span>
          )}
        </span>
      </button>
    )
  }
)

FluidButton.displayName = 'FluidButton'
