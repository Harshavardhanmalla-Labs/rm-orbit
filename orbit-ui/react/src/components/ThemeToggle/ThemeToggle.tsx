import * as React from "react";
import { Moon, Sun } from "lucide-react";
import { cn } from "@/lib/cn";

// ─── Theme context ────────────────────────────────────────────────────────────

type Theme = "light" | "dark" | "system";

type ThemeContextValue = {
  theme:     Theme;
  resolved:  "light" | "dark";
  setTheme:  (t: Theme) => void;
  toggle:    () => void;
};

const ThemeContext = React.createContext<ThemeContextValue | null>(null);

const STORAGE_KEY = "orbit-theme";

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setThemeState] = React.useState<Theme>(() => {
    if (typeof window === "undefined") return "system";
    return (localStorage.getItem(STORAGE_KEY) as Theme) ?? "system";
  });

  const systemDark = useSystemDark();

  const resolved: "light" | "dark" =
    theme === "system" ? (systemDark ? "dark" : "light") : theme;

  // Apply class to <html>
  React.useEffect(() => {
    const root = document.documentElement;
    root.classList.toggle("dark", resolved === "dark");
  }, [resolved]);

  const setTheme = React.useCallback((t: Theme) => {
    setThemeState(t);
    localStorage.setItem(STORAGE_KEY, t);
  }, []);

  const toggle = React.useCallback(() => {
    setTheme(resolved === "dark" ? "light" : "dark");
  }, [resolved, setTheme]);

  // Sync with orbit-bar theme toggle (dispatches orbit:theme-change)
  React.useEffect(() => {
    const handler = (e: Event) => {
      const detail = (e as CustomEvent<{ theme: Theme }>).detail;
      if (detail?.theme) setThemeState(detail.theme);
    };
    window.addEventListener("orbit:theme-change", handler);
    return () => window.removeEventListener("orbit:theme-change", handler);
  }, []);

  return (
    <ThemeContext.Provider value={{ theme, resolved, setTheme, toggle }}>
      {children}
    </ThemeContext.Provider>
  );
}

function useSystemDark(): boolean {
  const [dark, setDark] = React.useState(
    () => typeof window !== "undefined" && window.matchMedia("(prefers-color-scheme: dark)").matches,
  );
  React.useEffect(() => {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const handler = (e: MediaQueryListEvent) => setDark(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }, []);
  return dark;
}

export function useTheme(): ThemeContextValue {
  const ctx = React.useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used inside <ThemeProvider>");
  return ctx;
}

// ─── ThemeToggle button ───────────────────────────────────────────────────────

export type ThemeToggleProps = {
  className?: string;
  size?:      "sm" | "md" | "lg";
};

const sizeMap = {
  sm: "size-8 [&_svg]:size-3.5",
  md: "size-9 [&_svg]:size-4",
  lg: "size-11 [&_svg]:size-5",
};

export function ThemeToggle({ className, size = "md" }: ThemeToggleProps) {
  const { resolved, toggle } = useTheme();

  return (
    <button
      onClick={toggle}
      aria-label={resolved === "dark" ? "Switch to light mode" : "Switch to dark mode"}
      className={cn(
        "inline-flex items-center justify-center rounded-button",
        "border border-border-default bg-surface-base",
        "text-content-muted hover:text-content-primary hover:bg-surface-muted",
        "transition-colors duration-fast focus-ring",
        sizeMap[size],
        className,
      )}
    >
      {resolved === "dark" ? <Sun /> : <Moon />}
    </button>
  );
}
