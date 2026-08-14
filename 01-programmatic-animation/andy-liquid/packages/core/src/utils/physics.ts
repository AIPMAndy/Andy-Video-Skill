/**
 * Physics utilities for fluid animations
 * Based on high-end-visual-design spring physics
 */

export interface SpringConfig {
  stiffness: number
  damping: number
  mass?: number
}

export const SPRING_PRESETS: Record<string, SpringConfig> = {
  gentle: { stiffness: 100, damping: 20, mass: 1 },
  bouncy: { stiffness: 300, damping: 15, mass: 1 },
  stiff: { stiffness: 400, damping: 30, mass: 1 },
  slow: { stiffness: 80, damping: 25, mass: 1 },
}

/**
 * Calculate spring physics value
 */
export function spring(
  from: number,
  to: number,
  velocity: number,
  config: SpringConfig = SPRING_PRESETS.gentle
): { value: number; velocity: number; done: boolean } {
  const { stiffness, damping, mass = 1 } = config
  const dt = 1 / 60 // 60fps

  const springForce = -stiffness * (from - to)
  const dampingForce = -damping * velocity
  const acceleration = (springForce + dampingForce) / mass

  const newVelocity = velocity + acceleration * dt
  const newValue = from + newVelocity * dt

  const done = Math.abs(newVelocity) < 0.01 && Math.abs(newValue - to) < 0.01

  return {
    value: done ? to : newValue,
    velocity: done ? 0 : newVelocity,
    done,
  }
}

/**
 * Magnetic attraction calculation
 */
export function magnetic(
  elementX: number,
  elementY: number,
  mouseX: number,
  mouseY: number,
  strength: number = 0.3,
  maxDistance: number = 100
): { x: number; y: number } {
  const dx = mouseX - elementX
  const dy = mouseY - elementY
  const distance = Math.sqrt(dx * dx + dy * dy)

  if (distance > maxDistance) {
    return { x: 0, y: 0 }
  }

  const force = (1 - distance / maxDistance) * strength
  return {
    x: dx * force,
    y: dy * force,
  }
}

/**
 * Smooth interpolation
 */
export function lerp(start: number, end: number, factor: number): number {
  return start + (end - start) * factor
}

/**
 * Clamp value between min and max
 */
export function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max)
}

/**
 * Map value from one range to another
 */
export function mapRange(
  value: number,
  inMin: number,
  inMax: number,
  outMin: number,
  outMax: number
): number {
  return ((value - inMin) * (outMax - outMin)) / (inMax - inMin) + outMin
}
