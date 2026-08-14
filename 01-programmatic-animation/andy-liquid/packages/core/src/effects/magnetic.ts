/**
 * Magnetic hover effect
 * Based on high-end-visual-design magnetic button physics
 */

import { magnetic, lerp } from '../utils/physics'

export interface MagneticConfig {
  strength?: number
  maxDistance?: number
  smoothing?: number
  scale?: number
}

export class MagneticEffect {
  private rafId: number | null = null
  private currentX: number = 0
  private currentY: number = 0
  private targetX: number = 0
  private targetY: number = 0
  private isHovering: boolean = false

  constructor(
    private element: HTMLElement,
    private config: MagneticConfig = {}
  ) {
    this.element.addEventListener('mouseenter', this.handleMouseEnter)
    this.element.addEventListener('mouseleave', this.handleMouseLeave)
    this.element.addEventListener('mousemove', this.handleMouseMove)
  }

  private handleMouseEnter = () => {
    this.isHovering = true
    this.startAnimation()
  }

  private handleMouseLeave = () => {
    this.isHovering = false
    this.targetX = 0
    this.targetY = 0
  }

  private handleMouseMove = (e: MouseEvent) => {
    if (!this.isHovering) return

    const rect = this.element.getBoundingClientRect()
    const centerX = rect.left + rect.width / 2
    const centerY = rect.top + rect.height / 2

    const { strength = 0.3, maxDistance = 100 } = this.config

    const magneticForce = magnetic(centerX, centerY, e.clientX, e.clientY, strength, maxDistance)

    this.targetX = magneticForce.x
    this.targetY = magneticForce.y
  }

  private startAnimation(): void {
    if (this.rafId !== null) return

    const animate = () => {
      const { smoothing = 0.15, scale = 1.02 } = this.config

      this.currentX = lerp(this.currentX, this.targetX, smoothing)
      this.currentY = lerp(this.currentY, this.targetY, smoothing)

      const scaleValue = this.isHovering ? scale : 1

      this.element.style.transform = `translate(${this.currentX}px, ${this.currentY}px) scale(${scaleValue})`

      const threshold = 0.01
      const isAtTarget =
        Math.abs(this.currentX - this.targetX) < threshold &&
        Math.abs(this.currentY - this.targetY) < threshold

      if (!isAtTarget || this.isHovering) {
        this.rafId = requestAnimationFrame(animate)
      } else {
        this.rafId = null
      }
    }

    this.rafId = requestAnimationFrame(animate)
  }

  destroy(): void {
    this.element.removeEventListener('mouseenter', this.handleMouseEnter)
    this.element.removeEventListener('mouseleave', this.handleMouseLeave)
    this.element.removeEventListener('mousemove', this.handleMouseMove)

    if (this.rafId !== null) {
      cancelAnimationFrame(this.rafId)
    }

    this.element.style.transform = ''
  }
}
