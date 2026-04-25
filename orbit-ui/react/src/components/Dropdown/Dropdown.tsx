import * as React from "react";
import { Check, ChevronRight } from "lucide-react";
import { cn } from "@/lib/cn";

// ─── Context ─────────────────────────────────────────────────────────────────

type DropdownCtx = {
  open:    boolean;
  setOpen: (v: boolean) => void;
};

const DropdownContext = React.createContext<DropdownCtx>({
  open:    false,
  setOpen: () => {},
});

// ─── Root ─────────────────────────────────────────────────────────────────────

export type DropdownProps = {
  children:   React.ReactNode;
  defaultOpen?: boolean;
  open?:       boolean;
  onOpenChange?:(open: boolean) => void;
};

export function Dropdown({
  children,
  defaultOpen = false,
  open: controlledOpen,
  onOpenChange,
}: DropdownProps) {
  const [internalOpen, setInternalOpen] = React.useState(defaultOpen);
  const isControlled = controlledOpen !== undefined;
  const open = isControlled ? controlledOpen : internalOpen;

  const setOpen = React.useCallback(
    (v: boolean) => {
      if (!isControlled) setInternalOpen(v);
      onOpenChange?.(v);
    },
    [isControlled, onOpenChange],
  );

  // Close on outside click
  const containerRef = React.useRef<HTMLDivElement>(null);
  React.useEffect(() => {
    if (!open) return;
    const handler = (e: MouseEvent) => {
      if (!containerRef.current?.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [open, setOpen]);

  return (
    <DropdownContext.Provider value={{ open, setOpen }}>
      <div ref={containerRef} className="relative inline-block">
        {children}
      </div>
    </DropdownContext.Provider>
  );
}

// ─── Trigger ─────────────────────────────────────────────────────────────────

export type DropdownTriggerProps = {
  children: React.ReactElement;
  asChild?: boolean;
};

export function DropdownTrigger({ children }: DropdownTriggerProps) {
  const { open, setOpen } = React.useContext(DropdownContext);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const props = children.props as any;

  return React.cloneElement(children as React.ReactElement<Record<string, unknown>>, {
    onClick: (e: React.MouseEvent) => {
      props.onClick?.(e);
      setOpen(!open);
    },
    "aria-expanded": open,
    "aria-haspopup": "menu",
  });
}

// ─── Content ─────────────────────────────────────────────────────────────────

type Align = "start" | "end" | "center";
type Side  = "bottom" | "top";

const alignClass: Record<Align, string> = {
  start:  "left-0",
  end:    "right-0",
  center: "left-1/2 -translate-x-1/2",
};

const sideClass: Record<Side, string> = {
  bottom: "top-full mt-1",
  top:    "bottom-full mb-1",
};

export type DropdownContentProps = {
  children:   React.ReactNode;
  align?:     Align;
  side?:      Side;
  minWidth?:  string;
  className?: string;
};

export function DropdownContent({
  children,
  align   = "start",
  side    = "bottom",
  minWidth = "w-48",
  className,
}: DropdownContentProps) {
  const { open, setOpen } = React.useContext(DropdownContext);

  if (!open) return null;

  return (
    <div
      role="menu"
      className={cn(
        "absolute z-dropdown",
        sideClass[side],
        alignClass[align],
        minWidth,
        "rounded-lg border border-border-default bg-surface-overlay shadow-lg",
        "py-1 animate-scale-in origin-top-left",
        className,
      )}
      onKeyDown={(e) => e.key === "Escape" && setOpen(false)}
    >
      {children}
    </div>
  );
}

// ─── Item ─────────────────────────────────────────────────────────────────────

export type DropdownItemProps = {
  children:    React.ReactNode;
  onSelect?:   () => void;
  disabled?:   boolean;
  destructive?:boolean;
  iconLeft?:   React.ReactNode;
  iconRight?:  React.ReactNode;
  checked?:    boolean;
  className?:  string;
};

export function DropdownItem({
  children,
  onSelect,
  disabled    = false,
  destructive = false,
  iconLeft,
  iconRight,
  checked,
  className,
}: DropdownItemProps) {
  const { setOpen } = React.useContext(DropdownContext);

  const handleSelect = () => {
    if (disabled) return;
    onSelect?.();
    setOpen(false);
  };

  return (
    <button
      role="menuitem"
      type="button"
      disabled={disabled}
      onClick={handleSelect}
      className={cn(
        "flex w-full items-center gap-2 px-3 py-1.5 text-sm",
        "transition-colors duration-fast text-left",
        destructive
          ? "text-danger-600 hover:bg-danger-50 dark:hover:bg-danger-950"
          : "text-content-primary hover:bg-surface-muted",
        disabled && "opacity-50 cursor-not-allowed",
        className,
      )}
    >
      {checked !== undefined && (
        <Check
          className={cn(
            "size-3.5 shrink-0",
            checked ? "opacity-100" : "opacity-0",
          )}
        />
      )}
      {iconLeft && (
        <span className="size-4 shrink-0 text-content-muted">{iconLeft}</span>
      )}
      <span className="flex-1">{children}</span>
      {iconRight && (
        <span className="size-4 shrink-0 text-content-muted">{iconRight}</span>
      )}
    </button>
  );
}

// ─── Sub-menu trigger (for future nesting) ─────────────────────────────────

export type DropdownSubTriggerProps = {
  children:   React.ReactNode;
  iconLeft?:  React.ReactNode;
  className?: string;
};

export function DropdownSubTrigger({
  children,
  iconLeft,
  className,
}: DropdownSubTriggerProps) {
  return (
    <button
      type="button"
      role="menuitem"
      aria-haspopup="menu"
      className={cn(
        "flex w-full items-center gap-2 px-3 py-1.5 text-sm",
        "text-content-primary hover:bg-surface-muted transition-colors duration-fast",
        className,
      )}
    >
      {iconLeft && (
        <span className="size-4 shrink-0 text-content-muted">{iconLeft}</span>
      )}
      <span className="flex-1">{children}</span>
      <ChevronRight className="size-3.5 shrink-0 text-content-muted" />
    </button>
  );
}

// ─── Separator ───────────────────────────────────────────────────────────────

export function DropdownSeparator({ className }: { className?: string }) {
  return (
    <hr
      role="separator"
      className={cn("my-1 border-t border-border-default", className)}
    />
  );
}

// ─── Label ───────────────────────────────────────────────────────────────────

export function DropdownLabel({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "px-3 py-1 text-xs font-semibold text-content-muted uppercase tracking-wider",
        className,
      )}
    >
      {children}
    </div>
  );
}
