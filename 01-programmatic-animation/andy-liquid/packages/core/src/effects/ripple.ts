/**
 * Ripple effect implementation
 */

export interface RippleConfig {
  color?: string
  duration?: number
  maxSize?: number
}

export interface Ripple {
  x: number
  y: number
  size: number
  maxSize: number
  opacity: number
  startTime: number
  duration: number
  color: string
}

export class RippleEffect {
  private ripples: Ripple[] = []
  private animationId: number | null = null

  constructor(
    private element: HTMLElement,
    private config: RippleConfig = {}
  ) {
    this.element.addEventListener('click', this.handleClick)
  }

  private handleClick = (e: MouseEvent) => {
    const rect = this.element.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    this.addRipple(x, y)
  }

  addRipple(x: number, y: number): void {
    const {
      color = 'rgba(255, 255, 255, 0.5)',
      duration = 600,
      maxSize = Math.max(this.element.offsetWidth, this.element.offsetHeight) * 2,
    } = this.config

    const ripple: Ripple = {
      x,
      y,
      size: 0,
      maxSize,
      opacity: 1,
      startTime: Date.now(),
      duration,
      color,
    }

    this.ripples.push(ripple)

    if (!this.animationId) {
      this.animate()
    }
  }

  private animate = () => {
    const now = Date.now()
    this.ripples = this.ripples.filter((ripple) => {
      const elapsed = now - ripple.startTime
      const progress = Math.min(elapsed / ripple.duration, 1)

      ripple.size = ripple.maxSize * progress
      ripple.opacity = 1 - progress

      return progress < 1
    })

    this.render()

    if (this.ripples.length > 0) {
      this.animationId = requestAnimationFrame(this.animate)
    } else {
      this.animationId = null
    }
  }

  private render(): void {
    // Remove existing ripples
    const existingRipples = this.element.querySelectorAll('.liquid-ripple')
    existingRipples.forEach((el) => el.remove())

    // Add new ripples
    this.ripples.forEach((ripple) => {
      const el = document.createElement('div')
      el.className = 'liquid-ripple'
      el.style.cssText = `
        position: absolute;
        left: ${ripple.x}px;
        top: ${ripple.y}px;
        width: ${ripple.size}px;
        height: ${ripple.size}px;
        margin-left: ${-ripple.size / 2}px;
        margin-top: ${-ripple.size / 2}px;
        border-radius: 50%;
        background: ${ripple.color};
        opacity: ${ripple.opacity};
        pointer-events: none;
      `
      this.element.appendChild(el)
    })
  }

  destroy(): void {
    this.element.removeEventListener('click', this.handleClick)
    if (this.animationId) {
      cancelAnimationFrame(this.animationId)
    }
    const existingRipples = this.element.querySelectorAll('.liquid-ripple')
    existingRipples.forEach((el) => el.remove())
  }
}
