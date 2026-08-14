export interface LiquidCanvasConfig {
  text?: string[]
  subText?: string
  tagline?: string
  backgroundColor?: string
  textColor?: string
  intensity?: number
  metalness?: number
  roughness?: number
  displacementScale?: number
  enableRain?: boolean
}

export interface LiquidApp {
  dispose?: () => void
  liquidPlane?: {
    material: {
      metalness: number
      roughness: number
    }
    uniforms: {
      displacementScale: {
        value: number
      }
    }
  }
  setRain?: (enabled: boolean) => void
  loadImage?: (dataUrl: string) => void
}

export interface LiquidCanvasInstance {
  canvas: HTMLCanvasElement
  config: LiquidCanvasConfig
  app?: LiquidApp
  cleanup: () => void
}
