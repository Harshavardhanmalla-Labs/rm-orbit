import * as React from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { cn } from "@/lib/cn";

// ─── Context ─────────────────────────────────────────────────────────────────

type SidebarContextValue = {
  collapsed: boolean;
  setCollapsed: (v: boolean) => void;
};
const SidebarContext = React.createContext<SidebarContextValue>({
  collapsed: false,
  setCollapsed: () => {},
});

// ─── Root ─────────────────────────────────────────────────────────────────────

export type SidebarProps = {
  collapsed?:       boolean;
  defaultCollapsed?:boolean;
  onCollapsedChange?:(v: boolean) => void;
  collapsible?:     boolean;
  width?:           string; // expanded width, default "240px"
  className?:       string;
  children:         React.ReactNode;
};

export function Sidebar({
  collapsed: controlledCollapsed,
  defaultCollapsed = false,
  onCollapsedChange,
  collapsible = true,
  width = "240px",
  className,
  children,
}: SidebarProps) {
  const [internalCollapsed, setInternalCollapsed] = React.useState(defaultCollapsed);
  const collapsed = controlledCollapsed ?? internalCollapsed;

  const setCollapsed = React.useCallback((v: boolean) => {
    setInternalCollapsed(v);
    onCollapsedChange?.(v);
  }, [onCollapsedChange]);

  return (
    <SidebarContext.Provider value={{ collapsed, setCollapsed }}>
      <aside
        style={{ width: collapsed ? "56px" : width }}
        className={cn(
          "relative flex flex-col h-full",
          "bg-surface-base border-r border-border-default",
          "transition-all duration-slow ease-spring-soft",
          "overflow-hidden shrink-0",
          className,
        )}
      >
        {children}

        {collapsible && (
          <button
            onClick={() => setCollapsed(!collapsed)}
            aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
            className={cn(
              "absolute top-4 -right-3 z-raised",
              "size-6 rounded-full",
              "bg-surface-elevated border border-border-default shadow-sm",
              "flex items-center justify-center",
              "text-content-muted hover:text-content-primary",
              "transition-colors duration-fast",
              "focus-ring",
            )}
          >
            {collapsed ? (
              <ChevronRight className="size-3.5" />
            ) : (
              <ChevronLeft className="size-3.5" />
            )}
          </button>
        )}
      </aside>
    </SidebarContext.Provider>
  );
}

// ─── Header ──────────────────────────────────────────────────────────────────

Sidebar.Header = function SidebarHeader({
  children,
  className,
}: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn("flex items-center gap-2 px-3 py-3 shrink-0", className)}>
      {children}
    </div>
  );
};

// ─── Content ─────────────────────────────────────────────────────────────────

Sidebar.Content = function SidebarContent({
  children,
  className,
}: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn("flex-1 overflow-y-auto overflow-x-hidden scrollbar-thin py-1", className)}>
      {children}
    </div>
  );
};

// ─── Section ─────────────────────────────────────────────────────────────────

Sidebar.Section = function SidebarSection({
  label,
  children,
  className,
}: { label?: string; children: React.ReactNode; className?: string }) {
  const { collapsed } = React.useContext(SidebarContext);
  return (
    <div className={cn("px-2 mb-1", className)}>
      {label && !collapsed && (
        <p className="px-2 mb-1 mt-3 text-[11px] font-bold uppercase tracking-widest text-content-muted select-none">
          {label}
        </p>
      )}
      {label && collapsed && <div className="mt-3 mb-1 mx-2 h-px bg-border-subtle" />}
      {children}
    </div>
  );
};

// ─── Item ─────────────────────────────────────────────────────────────────────

export type SidebarItemProps = {
  icon?:     React.ReactNode;
  label:     string;
  active?:   boolean;
  badge?:    string | number;
  onClick?:  () => void;
  href?:     string;
  className?:string;
};

Sidebar.Item = function SidebarItem({
  icon,
  label,
  active,
  badge,
  onClick,
  href,
  className,
}: SidebarItemProps) {
  const { collapsed } = React.useContext(SidebarContext);
  const Tag = href ? "a" : "button";

  return (
    <Tag
      href={href}
      onClick={onClick}
      title={collapsed ? label : undefined}
      className={cn(
        "w-full flex items-center gap-2.5 px-2 py-2 rounded-lg text-sm font-medium",
        "transition-colors duration-fast cursor-pointer",
        "focus-ring",
        active
          ? "bg-primary-50 text-primary-700 dark:bg-primary-950 dark:text-primary-300"
          : "text-content-secondary hover:bg-surface-muted hover:text-content-primary",
        collapsed && "justify-center",
        className,
      )}
    >
      {icon && (
        <span className={cn("shrink-0 [&_svg]:size-4.5", active && "text-primary-600 dark:text-primary-400")}>
          {icon}
        </span>
      )}
      {!collapsed && (
        <>
          <span className="flex-1 truncate text-left">{label}</span>
          {badge !== undefined && badge !== null && (
            <span className="ml-auto shrink-0 text-[11px] font-semibold px-1.5 py-0.5 rounded-full bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300">
              {badge}
            </span>
          )}
        </>
      )}
    </Tag>
  );
};

// ─── Footer ──────────────────────────────────────────────────────────────────

Sidebar.Footer = function SidebarFooter({
  children,
  className,
}: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn("shrink-0 border-t border-border-subtle px-2 py-2", className)}>
      {children}
    </div>
  );
};

// ─── Hook ─────────────────────────────────────────────────────────────────────

export function useSidebar() {
  return React.useContext(SidebarContext);
}
