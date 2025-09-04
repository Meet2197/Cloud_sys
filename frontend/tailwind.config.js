module.exports = {
  darkMode: 'class',
  content: [
    './components/**/*.{vue,js,ts}',
    './pages/**/*.{vue,js,ts}',
    './app.vue',
    './plugins/**/*.{js,ts}',
  ],
  theme: {
    extend: {
      colors: {
        base: '#0b0f14',
        panel: '#111827',
        accent: '#60a5fa'
      },
      boxShadow: {
        soft: '0 10px 30px rgba(0,0,0,0.2)'
      },
      borderRadius: {
        xl2: '1.25rem'
      }
    }
  },
  plugins: []
}
