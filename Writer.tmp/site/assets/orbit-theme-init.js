/**
 * orbit-theme-init.js
 * Anti-FOUC (Flash of Unstyled Content) script.
 * Must be inlined in <head> BEFORE any CSS loads.
 * Reads stored theme preference and applies `dark` class
 * to <html> immediately, before React hydrates.
 */
(function () {
  try {
    var stored = localStorage.getItem("orbit-theme");
    var prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    var isDark =
      stored === "dark" || ((!stored || stored === "system") && prefersDark);
    if (isDark) document.documentElement.classList.add("dark");
  } catch (_) {}
})();
