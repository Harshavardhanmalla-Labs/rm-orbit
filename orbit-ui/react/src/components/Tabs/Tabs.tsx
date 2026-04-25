import * as React from "react";
import { cn } from "@/lib/cn";

// ─── Context ─────────────────────────────────────────────────────────────────

type TabsContextValue = {
  active:    string;
  setActive: (id: string) => void;
  variant:   "underline" | "pill" | "boxed";
};
const TabsContext = React.createContext<TabsContextValue>({
  active: "",
  setActive: () => {},
  variant: "underline",
});

// ─── Root ─────────────────────────────────────────────────────────────────────

export type TabsProps = {
  defaultTab?:   string;
  activeTab?:    string;
  onTabChange?:  (id: string) => void;
  variant?:      "underline" | "pill" | "boxed";
  className?:    string;
  children:      React.ReactNode;
};

export function Tabs({
  defaultTab,
  activeTab,
  onTabChange,
  variant = "underline",
  className,
  children,
}: TabsProps) {
  const [internalActive, setInternalActive] = React.useState(defaultTab ?? "");
  const active = activeTab ?? internalActive;

  const setActive = React.useCallback((id: string) => {
    setInternalActive(id);
    onTabChange?.(id);
  }, [onTabChange]);

  return (
    <TabsContext.Provider value={{ active, setActive, variant }}>
      <div className={cn("flex flex-col", className)}>
        {children}
      </div>
    </TabsContext.Provider>
  );
}

// ─── List (tab header bar) ────────────────────────────────────────────────────

const listVariantClasses = {
  underline: "border-b border-border-default gap-0",
  pill:      "gap-1 bg-surface-muted p-1 rounded-lg",
  boxed:     "gap-0 border border-border-default rounded-lg overflow-hidden",
};

Tabs.List = function TabList({
  children,
  className,
}: { children: React.ReactNode; className?: string }) {
  const { variant } = React.useContext(TabsContext);
  return (
    <div
      role="tablist"
      className={cn(
        "flex items-center shrink-0",
        listVariantClasses[variant],
        className,
      )}
    >
      {children}
    </div>
  );
};

// ─── Tab (individual tab button) ──────────────────────────────────────────────

export type TabProps = {
  id:         string;
  children:   React.ReactNode;
  icon?:      React.ReactNode;
  badge?:     string | number;
  disabled?:  boolean;
  className?: string;
};

const tabVariantClasses = {
  underline: {
    base:    "relative pb-2.5 pt-1 px-3 text-sm font-medium transition-colors duration-fast border-b-2 -mb-px",
    active:  "border-primary-500 text-primary-600 dark:text-primary-400",
    inactive:"border-transparent text-content-muted hover:text-content-primary hover:border-border-strong",
  },
  pill: {
    base:    "px-3 py-1.5 text-sm font-medium rounded-md transition-colors duration-fast",
    active:  "bg-surface-elevated text-content-primary shadow-sm",
    inactive:"text-content-muted hover:text-content-primary",
  },
  boxed: {
    base:    "px-4 py-2.5 text-sm font-medium transition-colors duration-fast border-r border-border-default last:border-r-0",
    active:  "bg-surface-base text-content-primary",
    inactive:"bg-surface-subtle text-content-muted hover:bg-surface-muted hover:text-content-primary",
  },
};

Tabs.Tab = function Tab({ id, children, icon, badge, disabled, className }: TabProps) {
  const { active, setActive, variant } = React.useContext(TabsContext);
  const isActive = active === id;
  const v = tabVariantClasses[variant];

  return (
    <button
      role="tab"
      aria-selected={isActive}
      aria-controls={`tabpanel-${id}`}
      id={`tab-${id}`}
      disabled={disabled}
      onClick={() => !disabled && setActive(id)}
      className={cn(
        "inline-flex items-center gap-1.5 whitespace-nowrap focus-ring",
        "disabled:opacity-40 disabled:cursor-not-allowed",
        v.base,
        isActive ? v.active : v.inactive,
        className,
      )}
    >
      {icon && <span className="[&_svg]:size-4 shrink-0">{icon}</span>}
      {children}
      {badge !== undefined && (
        <span className="ml-1 text-[11px] font-semibold px-1.5 py-0.5 rounded-full bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300">
          {badge}
        </span>
      )}
    </button>
  );
};

// ─── Panels ───────────────────────────────────────────────────────────────────

Tabs.Panels = function TabPanels({
  children,
  className,
}: { children: React.ReactNode; className?: string }) {
  return <div className={cn("flex-1", className)}>{children}</div>;
};

// ─── Panel ────────────────────────────────────────────────────────────────────

Tabs.Panel = function TabPanel({
  id,
  children,
  className,
}: { id: string; children: React.ReactNode; className?: string }) {
  const { active } = React.useContext(TabsContext);
  if (active !== id) return null;

  return (
    <div
      role="tabpanel"
      id={`tabpanel-${id}`}
      aria-labelledby={`tab-${id}`}
      className={cn("animate-fade-in", className)}
    >
      {children}
    </div>
  );
};
