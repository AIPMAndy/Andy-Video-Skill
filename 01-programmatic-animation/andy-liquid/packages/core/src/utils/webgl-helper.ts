/**
 * WebGL and canvas utilities
 */

/**
 * Get device pixel ratio for crisp rendering
 */
export function getPixelRatio(): number {
  return window.devicePixelRatio || 1
}

/**
 * Check WebGL support
 */
export function supportsWebGL(): boolean {
  try {
    const canvas = document.createElement('canvas')
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl')
    return !!gl
  } catch {
    return false
  }
}

/**
 * Check backdrop-filter support
 */
export function supportsBackdropFilter(): boolean {
  const testElement = document.createElement('div')
  const style = testElement.style as CSSStyleDeclaration & { 
    backdropFilter?: string;
    webkitBackdropFilter?: string;
  }
  style.backdropFilter = 'blur(1px)'
  style.webkitBackdropFilter = 'blur(1px)'
  const supported =
    style.backdropFilter === 'blur(1px)' ||
    style.webkitBackdropFilter === 'blur(1px)'
  return supported
}

/**
 * Get performance tier based on device capabilities
 */
export function getPerformanceTier(): 'high' | 'medium' | 'low' {
  if (!supportsWebGL()) return 'low'

  const canvas = document.createElement('canvas')
  const gl = canvas.getContext('webgl')
  if (!gl) return 'low'

  const debugInfo = gl.getExtension('WEBGL_debug_renderer_info')
  if (!debugInfo) return 'medium'

  const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL).toLowerCase()

  // High-end: dedicated GPUs
  if (renderer.includes('nvidia') || renderer.includes('amd') || renderer.includes('radeon')) {
    return 'high'
  }

  // Low-end: integrated/mobile GPUs
  if (renderer.includes('intel') || renderer.includes('mali') || renderer.includes('adreno')) {
    return 'low'
  }

  return 'medium'
}

/**
 * Create 2D context with optimal settings
 */
export function create2DContext(canvas: HTMLCanvasElement): CanvasRenderingContext2D | null {
  const ctx = canvas.getContext('2d', {
    alpha: true,
    desynchronized: true,
  })

  if (ctx) {
    // Enable font smoothing
    ctx.imageSmoothingEnabled = true
    ctx.imageSmoothingQuality = 'high'
  }

  return ctx
}

/**
 * Request animation frame with fallback
 */
export function raf(callback: FrameRequestCallback): number {
  return window.requestAnimationFrame(callback)
}

/**
 * Cancel animation frame
 */
export function cancelRaf(id: number): void {
  window.cancelAnimationFrame(id)
}
