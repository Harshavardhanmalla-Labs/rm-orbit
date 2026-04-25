import * as React from "react";
import { X } from "lucide-react";
import { cn } from "@/lib/cn";
import { IconButton } from "../Button/IconButton";

// ─── Size map ────────────────────────────────────────────────────────────────

const sizeClasses = {
  sm:   "max-w-sm",
  md:   "max-w-md",
  lg:   "max-w-lg",
  xl:   "max-w-xl",
  "2xl":"max-w-2xl",
  full: "max-w-full m-4",
} as const;

// ─── Context ─────────────────────────────────────────────────────────────────

const ModalContext = React.createContext<{ onClose?: () => void }>({});

// ─── Modal Root ──────────────────────────────────────────────────────────────

export type ModalProps = {
  open:          boolean;
  onClose?:      () => void;
  size?:         keyof typeof sizeClasses;
  closeOnBackdrop?: boolean;
  className?:    string;
  children:      React.ReactNode;
};

export function Modal({
  open,
  onClose,
  size             = "md",
  closeOnBackdrop  = true,
  className,
  children,
}: ModalProps) {
  // Lock scroll while open
  React.useEffect(() => {
    if (open) {
      document.body.style.overflow = "hidden";
      return () => { document.body.style.overflow = ""; };
    }
  }, [open]);

  // Close on Escape
  React.useEffect(() => {
    if (!open || !onClose) return;
    const handler = (e: KeyboardEvent) => { if (e.key === "Escape") onClose(); };
    document.addEventListener("keydown", handler);
    return () => document.removeEventListener("keydown", handler);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <ModalContext.Provider value={{ onClose }}>
      {/* Backdrop */}
      <div
        className="fixed inset-0 z-modal-backdrop bg-surface-overlay animate-fade-in"
        aria-hidden="true"
        onClick={closeOnBackdrop ? onClose : undefined}
      />
      {/* Panel */}
      <div
        role="dialog"
        aria-modal="true"
        className="fixed inset-0 z-modal flex items-center justify-center p-4"
      >
        <div
          className={cn(
            "relative w-full bg-surface-elevated rounded-modal shadow-modal",
            "border border-border-default",
            "animate-scale-in",
            sizeClasses[size],
            className,
          )}
          onClick={(e) => e.stopPropagation()}
        >
          {children}
        </div>
      </div>
    </ModalContext.Provider>
  );
}

// ─── Modal.Header ────────────────────────────────────────────────────────────

Modal.Header = function ModalHeader({
  children,
  className,
}: { children: React.ReactNode; className?: string }) {
  const { onClose } = React.useContext(ModalContext);
  return (
    <div className={cn("flex items-start justify-between gap-4 p-5 pb-0", className)}>
      <div className="flex-1">{children}</div>
      {onClose && (
        <IconButton label="Close modal" onClick={onClose} size="sm" variant="ghost" className="-mt-0.5 -mr-1">
          <X />
        </IconButton>
      )}
    </div>
  );
};

Modal.Title = function ModalTitle({ children, className }: { children: React.ReactNode; className?: string }) {
  return <h2 className={cn("text-lg font-semibold text-content-primary", className)}>{children}</h2>;
};

Modal.Description = function ModalDescription({ children, className }: { children: React.ReactNode; className?: string }) {
  return <p className={cn("text-sm text-content-muted mt-1", className)}>{children}</p>;
};

// ─── Modal.Body ──────────────────────────────────────────────────────────────

Modal.Body = function ModalBody({
  children,
  className,
}: { children: React.ReactNode; className?: string }) {
  return (
    <div className={cn("px-5 py-4", className)}>
      {children}
    </div>
  );
};

// ─── Modal.Footer ────────────────────────────────────────────────────────────

Modal.Footer = function ModalFooter({
  children,
  className,
}: { children: React.ReactNode; className?: string }) {
  return (
    <div
      className={cn(
        "flex items-center justify-end gap-2 px-5 py-4 pt-0",
        className,
      )}
    >
      {children}
    </div>
  );
};
