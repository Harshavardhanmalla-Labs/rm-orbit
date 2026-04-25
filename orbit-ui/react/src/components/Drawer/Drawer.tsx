import * as React from "react";
import { X } from "lucide-react";
import { cn } from "@/lib/cn";

// ─── Types ────────────────────────────────────────────────────────────────────

export type DrawerSide  = "left" | "right" | "top" | "bottom";
export type DrawerSize  = "sm" | "md" | "lg" | "xl" | "full";

export type DrawerProps = {
  open:          boolean;
  onClose:       () => void;
  side?:         DrawerSide;
  size?:         DrawerSize;
  title?:        React.ReactNode;
  description?:  React.ReactNode;
  children:      React.ReactNode;
  footer?:       React.ReactNode;
  closeOnOverlay?: boolean;
  className?:    string;
};

// ─── Size maps ────────────────────────────────────────────────────────────────

const sideHoriz: Record<DrawerSize, string> = {
  sm:   "w-72",
  md:   "w-80",
  lg:   "w-96",
  xl:   "w-[480px]",
  full: "w-full",
};

const sideVert: Record<DrawerSize, string> = {
  sm:   "h-48",
  md:   "h-64",
  lg:   "h-96",
  xl:   "h-[480px]",
  full: "h-full",
};

const slideIn: Record<DrawerSide, string> = {
  left:   "translate-x-0",
  right:  "translate-x-0",
  top:    "translate-y-0",
  bottom: "translate-y-0",
};

const slideOut: Record<DrawerSide, string> = {
  left:   "-translate-x-full",
  right:  "translate-x-full",
  top:    "-translate-y-full",
  bottom: "translate-y-full",
};

const position: Record<DrawerSide, string> = {
  left:   "inset-y-0 left-0",
  right:  "inset-y-0 right-0",
  top:    "inset-x-0 top-0",
  bottom: "inset-x-0 bottom-0",
};

const roundedMap: Record<DrawerSide, string> = {
  left:   "rounded-r-2xl",
  right:  "rounded-l-2xl",
  top:    "rounded-b-2xl",
  bottom: "rounded-t-2xl",
};

// ─── Drawer ───────────────────────────────────────────────────────────────────

export function Drawer({
  open,
  onClose,
  side = "right",
  size = "md",
  title,
  description,
  children,
  footer,
  closeOnOverlay = true,
  className,
}: DrawerProps) {
  const isHoriz = side === "left" || side === "right";
  const sizeClass = isHoriz ? sideHoriz[size] : sideVert[size];

  // Lock body scroll
  React.useEffect(() => {
    if (open) {
      const prev = document.body.style.overflow;
      document.body.style.overflow = "hidden";
      return () => { document.body.style.overflow = prev; };
    }
  }, [open]);

  // Escape key
  React.useEffect(() => {
    if (!open) return;
    const onKeyDown = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [open, onClose]);

  return (
    <>
      {/* Backdrop */}
      <div
        aria-hidden="true"
        onClick={closeOnOverlay ? onClose : undefined}
        className={cn(
          "fixed inset-0 z-40 bg-black/50 transition-opacity duration-300",
          open ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none",
        )}
      />

      {/* Panel */}
      <div
        role="dialog"
        aria-modal="true"
        aria-label={typeof title === "string" ? title : "Drawer"}
        className={cn(
          "fixed z-50 flex flex-col bg-surface-base shadow-xl transition-transform duration-300",
          position[side],
          sizeClass,
          roundedMap[side],
          open ? slideIn[side] : slideOut[side],
          className,
        )}
      >
        {/* Header */}
        {(title || description) && (
          <div className="flex items-start justify-between gap-4 px-6 pt-5 pb-4 border-b border-border-subtle flex-shrink-0">
            <div className="flex-1 min-w-0">
              {title && (
                <h2 className="text-base font-semibold text-content-primary">{title}</h2>
              )}
              {description && (
                <p className="mt-1 text-sm text-content-muted">{description}</p>
              )}
            </div>
            <button
              type="button"
              onClick={onClose}
              aria-label="Close drawer"
              className={cn(
                "flex-shrink-0 rounded-button p-1.5 text-content-muted",
                "hover:bg-surface-muted hover:text-content-primary transition-colors duration-fast",
              )}
            >
              <X className="w-4 h-4" aria-hidden="true" />
            </button>
          </div>
        )}

        {/* Close button when no title */}
        {!title && !description && (
          <button
            type="button"
            onClick={onClose}
            aria-label="Close drawer"
            className={cn(
              "absolute top-4 right-4 z-10 rounded-button p-1.5 text-content-muted",
              "hover:bg-surface-muted hover:text-content-primary transition-colors duration-fast",
            )}
          >
            <X className="w-4 h-4" aria-hidden="true" />
          </button>
        )}

        {/* Body */}
        <div className="flex-1 overflow-y-auto px-6 py-4">{children}</div>

        {/* Footer */}
        {footer && (
          <div className="flex-shrink-0 px-6 py-4 border-t border-border-subtle">
            {footer}
          </div>
        )}
      </div>
    </>
  );
}
