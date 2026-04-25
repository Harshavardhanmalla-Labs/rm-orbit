import { createRequire } from "module";
const require = createRequire(import.meta.url);

const colors    = require("./tokens/colors.json");
const typo      = require("./tokens/typography.json");
const shadows   = require("./tokens/shadows.json");
const radius    = require("./tokens/radius.json");
const motion    = require("./tokens/motion.json");
const zIndex    = require("./tokens/z-index.json");

/** @type {import('tailwindcss').Config} */
const orbitPreset = {
  darkMode: "class",

  theme: {
    extend: {
      // ─── Colors ──────────────────────────────────────────────────────────
      colors: {
        primary: colors.primary,
        neutral: colors.neutral,
        success: colors.success,
        warning: colors.warning,
        danger:  colors.danger,
        info:    colors.info,

        // Semantic surface tokens (CSS variable–driven for dark/light toggle)
        surface: {
          base:     "var(--orbit-surface-base)",
          subtle:   "var(--orbit-surface-subtle)",
          muted:    "var(--orbit-surface-muted)",
          elevated: "var(--orbit-surface-elevated)",
          overlay:  "var(--orbit-surface-overlay)",
        },
        content: {
          primary:   "var(--orbit-text-primary)",
          secondary: "var(--orbit-text-secondary)",
          muted:     "var(--orbit-text-muted)",
          disabled:  "var(--orbit-text-disabled)",
          inverse:   "var(--orbit-text-inverse)",
          link:      "var(--orbit-text-link)",
        },
        border: {
          default: "var(--orbit-border-default)",
          subtle:  "var(--orbit-border-subtle)",
          strong:  "var(--orbit-border-strong)",
          focus:   "var(--orbit-border-focus)",
        },
      },

      // ─── Typography ──────────────────────────────────────────────────────
      fontFamily: {
        sans:    typo.fontFamily.sans,
        display: typo.fontFamily.display,
        mono:    typo.fontFamily.mono,
      },
      fontSize: typo.fontSize,

      // ─── Border Radius ───────────────────────────────────────────────────
      borderRadius: {
        none:   radius.none,
        xs:     radius.xs,
        sm:     radius.sm,
        DEFAULT:radius.md,
        md:     radius.md,
        lg:     radius.lg,
        xl:     radius.xl,
        "2xl":  radius["2xl"],
        "3xl":  radius["3xl"],
        full:   radius.full,
        // Component-specific aliases
        button: radius.button,
        input:  radius.input,
        card:   radius.card,
        modal:  radius.modal,
        badge:  radius.badge,
        panel:  radius.panel,
        chip:   radius.chip,
      },

      // ─── Shadows ─────────────────────────────────────────────────────────
      boxShadow: shadows,

      // ─── Z-Index ─────────────────────────────────────────────────────────
      zIndex: zIndex,

      // ─── Animation & Keyframes ───────────────────────────────────────────
      transitionDuration: {
        instant:  motion.duration.instant,
        fast:     motion.duration.fast,
        normal:   motion.duration.normal,
        slow:     motion.duration.slow,
        slower:   motion.duration.slower,
        slowest:  motion.duration.slowest,
      },
      transitionTimingFunction: {
        "ease-in":     motion.easing["ease-in"],
        "ease-out":    motion.easing["ease-out"],
        "ease-in-out": motion.easing["ease-in-out"],
        spring:        motion.easing.spring,
        "spring-soft": motion.easing["spring-soft"],
      },
      animation: {
        "fade-in":     `fade-in ${motion.duration.normal} ${motion.easing["ease-out"]} both`,
        "fade-out":    `fade-out ${motion.duration.normal} ${motion.easing["ease-in"]} both`,
        "slide-up":    `slide-up ${motion.duration.normal} ${motion.easing["ease-out"]} both`,
        "slide-down":  `slide-down ${motion.duration.normal} ${motion.easing["ease-out"]} both`,
        "slide-left":  `slide-left ${motion.duration.normal} ${motion.easing["ease-out"]} both`,
        "slide-right": `slide-right ${motion.duration.normal} ${motion.easing["ease-out"]} both`,
        "scale-in":    `scale-in ${motion.duration.fast} ${motion.easing["spring-soft"]} both`,
        "scale-out":   `scale-out ${motion.duration.fast} ${motion.easing["ease-in"]} both`,
        shimmer:       `shimmer 1.5s linear infinite`,
        "pulse-ring":  `pulse-ring 1.5s ${motion.easing["ease-out"]} infinite`,
        float:         `float 3s ${motion.easing["ease-in-out"]} infinite`,
        spin:          `spin 1s linear infinite`,
        "bounce-soft": `bounce-soft 1.5s ${motion.easing["ease-in-out"]} infinite`,
      },
      keyframes: motion.keyframes,

      // ─── Spacing ─────────────────────────────────────────────────────────
      // Uses Tailwind's default 4px base scale; we extend with named sizes
      spacing: {
        "4.5": "18px",
        "13":  "52px",
        "15":  "60px",
        "18":  "72px",
        "22":  "88px",
        "26":  "104px",
        "30":  "120px",
      },
    },
  },

  plugins: [
    // ─── Glass Utility ───────────────────────────────────────────────────
    function orbitGlassPlugin({ addUtilities, theme }) {
      addUtilities({
        ".glass": {
          backdropFilter: "blur(12px)",
          WebkitBackdropFilter: "blur(12px)",
          background: "var(--orbit-glass-bg)",
          borderColor: "var(--orbit-glass-border)",
          boxShadow: shadows.glass,
        },
        ".glass-sm": {
          backdropFilter: "blur(8px)",
          WebkitBackdropFilter: "blur(8px)",
          background: "var(--orbit-glass-bg)",
          borderColor: "var(--orbit-glass-border)",
          boxShadow: shadows["glass-sm"],
        },
        ".glass-subtle": {
          backdropFilter: "blur(4px)",
          WebkitBackdropFilter: "blur(4px)",
          background: "var(--orbit-glass-bg)",
        },
      });
    },

    // ─── Focus Ring Utility ──────────────────────────────────────────────
    function orbitFocusPlugin({ addUtilities }) {
      addUtilities({
        ".focus-ring": {
          outline: "none",
          "&:focus-visible": {
            outline: "2px solid var(--orbit-border-focus)",
            outlineOffset: "2px",
          },
        },
        ".focus-ring-inset": {
          outline: "none",
          "&:focus-visible": {
            outline: "2px solid var(--orbit-border-focus)",
            outlineOffset: "-2px",
          },
        },
      });
    },

    // ─── Scrollbar Utility ───────────────────────────────────────────────
    function orbitScrollbarPlugin({ addUtilities }) {
      addUtilities({
        ".scrollbar-thin": {
          scrollbarWidth: "thin",
          scrollbarColor: "var(--orbit-border-default) transparent",
          "&::-webkit-scrollbar": { width: "6px", height: "6px" },
          "&::-webkit-scrollbar-track": { background: "transparent" },
          "&::-webkit-scrollbar-thumb": {
            background: "var(--orbit-border-strong)",
            borderRadius: "9999px",
          },
          "&::-webkit-scrollbar-thumb:hover": {
            background: "var(--orbit-text-muted)",
          },
        },
        ".scrollbar-none": {
          scrollbarWidth: "none",
          "&::-webkit-scrollbar": { display: "none" },
        },
      });
    },

    // ─── Skeleton/Shimmer Utility ────────────────────────────────────────
    function orbitSkeletonPlugin({ addUtilities }) {
      addUtilities({
        ".skeleton": {
          background:
            "linear-gradient(90deg, var(--orbit-surface-muted) 25%, var(--orbit-surface-subtle) 50%, var(--orbit-surface-muted) 75%)",
          backgroundSize: "1000px 100%",
          animation: "shimmer 1.5s linear infinite",
          borderRadius: "4px",
        },
      });
    },
  ],
};

export default orbitPreset;
