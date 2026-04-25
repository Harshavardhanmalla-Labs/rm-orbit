import * as React from "react";
import { cn } from "@/lib/cn";

// ─── Types ────────────────────────────────────────────────────────────────────

export type PopoverAlign = "start" | "center" | "end";
export type PopoverSide  = "top" | "bottom" | "left" | "right";

export type PopoverProps = {
  trigger:    React.ReactElement;
  children:   React.ReactNode;
  side?:      PopoverSide;
  align?:     PopoverAlign;
  open?:      boolean;
  onOpenChange?: (open: boolean) => void;
  className?: string;
};

// ─── Position classes ─────────────────────────────────────────────────────────

const sideClasses: Record<PopoverSide, string> = {
  bottom: "top-full mt-2",
  top:    "bottom-full mb-2",
  left:   "right-full mr-2 top-0",
  right:  "left-full ml-2 top-0",
};

const alignClasses: Record<PopoverAlign, Record<PopoverSide, string>> = {
  start: {
    bottom: "left-0",
    top:    "left-0",
    left:   "top-0",
    right:  "top-0",
  },
  center: {
    bottom: "left-1/2 -translate-x-1/2",
    top:    "left-1/2 -translate-x-1/2",
    left:   "top-1/2 -translate-y-1/2",
    right:  "top-1/2 -translate-y-1/2",
  },
  end: {
    bottom: "right-0",
    top:    "right-0",
    left:   "bottom-0",
    right:  "bottom-0",
  },
};

// ─── Popover ──────────────────────────────────────────────────────────────────

export function Popover({
  trigger,
  children,
  side = "bottom",
  align = "start",
  open: controlledOpen,
  onOpenChange,
  className,
}: PopoverProps) {
  const isControlled = controlledOpen !== undefined;
  const [internal, setInternal] = React.useState(false);
  const open = isControlled ? controlledOpen! : internal;

  const setOpen = (v: boolean) => {
    if (!isControlled) setInternal(v);
    onOpenChange?.(v);
  };

  const ref = React.useRef<HTMLDivElement>(null);

  // Outside click
  React.useEffect(() => {
    if (!open) return;
    const handler = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [open]);

  // Escape key
  React.useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(false); };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open]);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const triggerProps = trigger.props as any;
  const cloned = React.cloneElement(trigger as React.ReactElement<Record<string, unknown>>, {
    onClick: (e: React.MouseEvent) => {
      triggerProps.onClick?.(e);
      setOpen(!open);
    },
    "aria-expanded": open,
    "aria-haspopup": "dialog",
  });

  return (
    <div ref={ref} className="relative inline-flex">
      {cloned}
      {open && (
        <div
          role="dialog"
          aria-modal="false"
          className={cn(
            "absolute z-50 min-w-[200px] rounded-panel border border-border-default",
            "bg-surface-base shadow-lg animate-in fade-in-0 zoom-in-95",
            sideClasses[side],
            alignClasses[align][side],
            className,
          )}
        >
          {children}
        </div>
      )}
    </div>
  );
}

// ─── PopoverHeader / Body ─────────────────────────────────────────────────────

export function PopoverHeader({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn("px-4 py-3 border-b border-border-subtle", className)}>
      <p className="text-sm font-semibold text-content-primary">{children}</p>
    </div>
  );
}

export function PopoverBody({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={cn("px-4 py-3 text-sm text-content-secondary", className)}>{children}</div>;
}

export function PopoverFooter({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn("px-4 py-3 border-t border-border-subtle flex justify-end gap-2", className)}>
      {children}
    </div>
  );
}
