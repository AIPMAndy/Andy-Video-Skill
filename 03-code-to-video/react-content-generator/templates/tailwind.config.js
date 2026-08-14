/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // 主色调
        primary: {
          50: '#eef2ff',
          100: '#e0e7ff',
          200: '#c7d2fe',
          300: '#a5b4fc',
          400: '#818cf8',
          500: '#6366f1',
          600: '#4f46e5',
          700: '#4338ca',
          800: '#3730a3',
          900: '#312e81',
        },
      },
      animation: {
        'fadeInScale': 'fadeInScale 0.6s cubic-bezier(0.25, 1, 0.5, 1) both',
        'slideInUp': 'slideInUp 0.5s cubic-bezier(0.25, 1, 0.5, 1) both',
        'float-badge': 'float-badge 3s ease-in-out infinite',
      },
      keyframes: {
        fadeInScale: {
          'from': { opacity: '0', transform: 'translateY(40px) scale(0.95)' },
          'to': { opacity: '1', transform: 'translateY(0) scale(1)' },
        },
        slideInUp: {
          'from': { opacity: '0', transform: 'translateY(50px)' },
          'to': { opacity: '1', transform: 'translateY(0)' },
        },
        'float-badge': {
          '0%, 100%': { transform: 'translateY(0) rotate(3deg)' },
          '50%': { transform: 'translateY(-5px) rotate(3deg)' },
        },
      },
    },
  },
  plugins: [],
}
