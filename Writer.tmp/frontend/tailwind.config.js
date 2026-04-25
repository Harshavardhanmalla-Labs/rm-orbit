import orbitPreset from "../../orbit-ui/tailwind-preset.js";

/** @type {import('tailwindcss').Config} */
export default {
  presets: [orbitPreset],
  darkMode: "class",
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Writer-specific grid background pattern
      backgroundImage: {
        "grid-pattern": "linear-gradient(to right, var(--orbit-border-default) 1px, transparent 1px), linear-gradient(to bottom, var(--orbit-border-default) 1px, transparent 1px)",
      },
    },
  },
  plugins: [],
};
