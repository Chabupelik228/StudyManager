/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        app: {
          canvas: 'var(--app-canvas)',
          card: 'var(--app-card)',
          cardSubtle: 'var(--app-card-subtle)',
          text: 'var(--app-text)',
          muted: 'var(--app-muted)',
          hint: 'var(--app-hint)',
          border: 'var(--app-border)',
          accent: '#2563eb',
          accentLight: '#3b82f6',
          danger: '#ef4444',
          warning: '#f59e0b',
          success: '#10b981',
        },
        tg: {
          bg: 'var(--tg-theme-bg-color, #ffffff)',
          secondaryBg: 'var(--tg-theme-secondary-bg-color, #f3f2f8)',
          text: 'var(--tg-theme-text-color, #000000)',
          hint: 'var(--tg-theme-hint-color, #8e8e93)',
          link: 'var(--tg-theme-link-color, #007aff)',
          button: 'var(--tg-theme-button-color, #007aff)',
          buttonText: 'var(--tg-theme-button-text-color, #ffffff)',
        }
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', '-apple-system', 'BlinkMacSystemFont', '"SF Pro Display"', '"Segoe UI"', 'Roboto', 'sans-serif'],
        mono: ['"SF Mono"', 'Menlo', 'Consolas', 'monospace'],
      },
      boxShadow: {
        'premium': '0 2px 10px -1px rgba(0, 0, 0, 0.05), 0 1px 3px -1px rgba(0, 0, 0, 0.03)',
        'premium-dark': '0 4px 20px -2px rgba(0, 0, 0, 0.4), 0 2px 6px -1px rgba(0, 0, 0, 0.2)',
        'glow-blue': '0 0 18px -2px rgba(37, 99, 235, 0.45)',
        'glow-emerald': '0 0 14px -2px rgba(16, 185, 129, 0.35)',
        'glow-rose': '0 0 14px -2px rgba(239, 68, 68, 0.35)',
        'glow-amber': '0 0 14px -2px rgba(245, 158, 11, 0.35)',
      }
    },
  },
  plugins: [],
}
