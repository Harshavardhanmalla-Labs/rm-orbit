import orbitPreset from "../../orbit-ui/tailwind-preset.js";

/** @type {import('tailwindcss').Config} */
export default {
  presets: [orbitPreset],
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{ts,tsx}",
    "../../orbit-ui/react/src/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
