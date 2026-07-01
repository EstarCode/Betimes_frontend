/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1E3A5F',
          hover: '#162D4A',
          light: '#2A4A70',
        },
        gold: {
          DEFAULT: '#B8923C',
          bg: '#FEF9F0',
        },
        surface: {
          DEFAULT: '#FAFAFA',
          hover: '#F5F5F5',
        },
        border: {
          DEFAULT: '#64748B',
          light: '#CBD5E1',
          divider: '#E2E8F0',
        },
        text: {
          primary: '#1E293B',
          secondary: '#475569',
          muted: '#64748B',
        },
        error: {
          DEFAULT: '#DC2626',
          bg: '#FEF2F2',
        },
        success: {
          DEFAULT: '#059669',
          bg: '#F0FDF4',
        },
        warning: {
          DEFAULT: '#D97706',
          bg: '#FFFBEB',
        },
        info: {
          DEFAULT: '#0284C7',
          bg: '#F0F9FF',
        },
      },
      fontFamily: {
        sans: ['IBM Plex Sans', 'ui-sans-serif', 'system-ui', 'Roboto'],
      },
      fontSize: {
        'xs': '12px',
        'sm': '13px',
        'base': '14px',
        'md': '16px',
        'lg': '18px',
        'xl': '20px',
        '2xl': '24px',
      },
      lineHeight: {
        'tight': '1.2',
        'snug': '1.3',
        'normal': '1.4',
      },
      spacing: {
        '18': '72px',
        '22': '88px',
      },
      borderRadius: {
        DEFAULT: '4px',
        'sm': '3px',
      },
    },
  },
  plugins: [],
}
