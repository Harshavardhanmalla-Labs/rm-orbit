/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        surface: '#161616',
        toolbar: '#1e1e1e',
        tile: '#1a1a1a',
      },
    },
  },
  plugins: [],
};
