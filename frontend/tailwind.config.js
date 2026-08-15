/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        tg: {
          bg: 'var(--tg-theme-bg-color, #ffffff)',
          secondaryBg: 'var(--tg-theme-secondary-bg-color, #f3f2f8)',
          text: 'var(--tg-theme-text-color, #000000)',
          hint: 'var(--tg-theme-hint-color, #8e8e93)',
          link: 'var(--tg-theme-link-color, #007aff)',
          button: 'var(--tg-theme-button-color, #007aff)',
          buttonText: 'var(--tg-theme-button-text-color, #ffffff)',
        },
        app: {
          accent: '#007aff',
          danger: '#ff3b30',
          warning: '#ff9500',
          success: '#34c759',
          separator: 'rgba(142, 142, 147, 0.2)',
        }
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', '"SF Pro Display"', '"Segoe UI"', 'Roboto', 'sans-serif'],
        mono: ['"SF Mono"', 'Menlo', 'Consolas', 'monospace'],
      },
    },
  },
  plugins: [],
}
