/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Dark mode surfaces
        'bg-dark':       '#0F1923',
        'sidebar-dark':  '#111C27',
        'card-dark':     '#162032',
        'border-dark':   '#1E2D3D',
        // Light mode surfaces
        'bg-light':      '#F0F4F8',
        'sidebar-light': '#FFFFFF',
        'card-light':    '#FFFFFF',
        'border-light':  '#E2E8F0',
        // Brand
        teal: {
          DEFAULT: '#0F766E',
          light:   '#06B6D4',
          50:      '#E6FFFA',
          100:     '#B2F5EA',
        },
        // Status
        safe:    '#22C55E',
        alert:   '#EF4444',
        warning: '#F59E0B',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        xl: '0.75rem',
        '2xl': '1rem',
      },
    },
  },
  plugins: [],
}
