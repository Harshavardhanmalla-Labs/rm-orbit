import * as React from "react";
import { CheckCircle2, AlertCircle, AlertTriangle, Info, X } from "lucide-react";
import { cn } from "@/lib/cn";

// ─── Types ───────────────────────────────────────────────────────────────────

export type ToastVariant = "success" | "error" | "warning" | "info";

export type ToastItem = {
  id:        string;
  variant?:  ToastVariant;
  title:     string;
  message?:  string;
  duration?: number; // ms, 0 = persistent
  action?:   { label: string; onClick: () => void };
};

const variantConfig: Record<
  ToastVariant,
  { icon: React.ElementType; classes: string; iconClasses: string }
> = {
  success: {
    icon:        CheckCircle2,
    classes:     "border-success-200 dark:border-success-800",
    iconClasses: "text-success-500",
  },
  error: {
    icon:        AlertCircle,
    classes:     "border-danger-200 dark:border-danger-800",
    iconClasses: "text-danger-500",
  },
  warning: {
    icon:        AlertTriangle,
    classes:     "border-warning-200 dark:border-warning-800",
    iconClasses: "text-warning-500",
  },
  info: {
    icon:        Info,
    classes:     "border-info-200 dark:border-info-800",
    iconClasses: "text-info-500",
  },
};

// ─── Single Toast ────────────────────────────────────────────────────────────

type SingleToastProps = ToastItem & { onDismiss: (id: string) => void };

function SingleToast({ id, variant = "info", title, message, duration = 4000, action, onDismiss }: SingleToastProps) {
  const cfg = variantConfig[variant];
  const Icon = cfg.icon;

  React.useEffect(() => {
    if (duration === 0) return;
    const t = setTimeout(() => onDismiss(id), duration);
    return () => clearTimeout(t);
  }, [id, duration, onDismiss]);

  return (
    <div
      role="alert"
      aria-live="polite"
      className={cn(
        "flex items-start gap-3 w-full max-w-sm pointer-events-auto",
        "bg-surface-elevated border rounded-lg shadow-dropdown px-4 py-3",
        "animate-slide-left",
        cfg.classes,
      )}
    >
      <Icon className={cn("size-5 shrink-0 mt-0.5", cfg.iconClasses)} aria-hidden="true" />
      <div className="flex-1 min-w-0">
        <p className="text-sm font-semibold text-content-primary">{title}</p>
        {message && <p className="text-xs text-content-muted mt-0.5">{message}</p>}
        {action && (
          <button
            onClick={action.onClick}
            className="mt-1.5 text-xs font-semibold text-primary-600 dark:text-primary-400 hover:underline"
          >
            {action.label}
          </button>
        )}
      </div>
      <button
        onClick={() => onDismiss(id)}
        aria-label="Dismiss"
        className="shrink-0 p-0.5 rounded hover:bg-surface-muted text-content-muted"
      >
        <X className="size-3.5" />
      </button>
    </div>
  );
}

// ─── Toast Provider + Context ─────────────────────────────────────────────────

type ToastContextValue = {
  toast: (item: Omit<ToastItem, "id">) => void;
  dismiss: (id: string) => void;
};

const ToastContext = React.createContext<ToastContextValue | null>(null);

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<ToastItem[]>([]);

  const toast = React.useCallback((item: Omit<ToastItem, "id">) => {
    const id = Math.random().toString(36).slice(2);
    setToasts((prev) => [...prev.slice(-4), { ...item, id }]); // max 5
  }, []);

  const dismiss = React.useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ toast, dismiss }}>
      {children}
      {/* Toast stack */}
      <div
        aria-live="polite"
        className="fixed bottom-4 right-4 z-toast flex flex-col gap-2 pointer-events-none"
      >
        {toasts.map((t) => (
          <SingleToast key={t.id} {...t} onDismiss={dismiss} />
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast(): ToastContextValue {
  const ctx = React.useContext(ToastContext);
  if (!ctx) throw new Error("useToast must be used inside <ToastProvider>");
  return ctx;
}
