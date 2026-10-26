/** @type {import('tailwindcss').Config} */
const c = (v) => `hsl(var(--${v}) / <alpha-value>)`;

module.exports = {
  // `overline` is a Tailwind utility; without this an app's own eyebrow-label class draws a line above the text.
  blocklist: ["overline"],
  darkMode: ["class"],
  content: ["./src/**/*.{js,jsx,ts,tsx}", "./public/index.html"],
  theme: {
    extend: {
      fontFamily: {
        display: ['Outfit', 'sans-serif'],
        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)'
      },
      colors: {
        background: c('background'),
        foreground: c('foreground'),
        card: { DEFAULT: c('card'), foreground: c('card-foreground') },
        popover: { DEFAULT: c('popover'), foreground: c('popover-foreground') },
        primary: { DEFAULT: c('primary'), foreground: c('primary-foreground') },
        secondary: { DEFAULT: c('secondary'), foreground: c('secondary-foreground') },
        muted: { DEFAULT: c('muted'), foreground: c('muted-foreground') },
        accent: { DEFAULT: c('accent'), foreground: c('accent-foreground') },
        destructive: { DEFAULT: c('destructive'), foreground: c('destructive-foreground') },
        border: c('border'),
        input: c('input'),
        ring: c('ring'),
        gold: { DEFAULT: c('gold'), ink: c('gold-ink') },
        success: { DEFAULT: c('success'), ink: c('success-ink') },
        warning: { DEFAULT: c('warning'), ink: c('warning-ink') },
        brand: { DEFAULT: c('primary'), ink: c('brand-ink') },
        obsidian: '#0A0A0F',
        charcoal: '#161622',
        lavender: '#8F8FA3',
      },
      keyframes: {
        'accordion-down': { from: { height: '0' }, to: { height: 'var(--radix-accordion-content-height)' } },
        'accordion-up': { from: { height: 'var(--radix-accordion-content-height)' }, to: { height: '0' } },
        'rise-in': { from: { opacity: '0', transform: 'translateY(14px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        float: { '0%,100%': { transform: 'translateY(0)' }, '50%': { transform: 'translateY(-10px)' } },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
        'rise-in': 'rise-in 0.55s cubic-bezier(0.2, 0.7, 0.2, 1) both',
        float: 'float 6s ease-in-out infinite',
      }
    }
  },
  plugins: [require("tailwindcss-animate")],
};
