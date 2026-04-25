import * as React from "react";
import { CheckCircle2, AlertCircle, AlertTriangle, Info, X } from "lucide-react";
import { cn } from "@/lib/cn";

const variantConfig = {
  success: {
    wrapper: "bg-success-50 border-success-200 dark:bg-success-950/30 dark:border-success-800",
    icon:    "text-success-500",
    title:   "text-success-800 dark:text-success-200",
    desc:    "text-success-700 dark:text-success-300",
    Icon:    CheckCircle2,
  },
  error: {
    wrapper: "bg-danger-50 border-danger-200 dark:bg-danger-950/30 dark:border-danger-800",
    icon:    "text-danger-500",
    title:   "text-danger-800 dark:text-danger-200",
    desc:    "text-danger-700 dark:text-danger-300",
    Icon:    AlertCircle,
  },
  warning: {
    wrapper: "bg-warning-50 border-warning-200 dark:bg-warning-950/30 dark:border-warning-800",
    icon:    "text-warning-500",
    title:   "text-warning-800 dark:text-warning-200",
    desc:    "text-warning-700 dark:text-warning-300",
    Icon:    AlertTriangle,
  },
  info: {
    wrapper: "bg-info-50 border-info-200 dark:bg-info-950/30 dark:border-info-800",
    icon:    "text-info-500",
    title:   "text-info-800 dark:text-info-200",
    desc:    "text-info-700 dark:text-info-300",
    Icon:    Info,
  },
} as const;

export type AlertProps = {
  variant?:    keyof typeof variantConfig;
  title?:      string;
  children?:   React.ReactNode;
  dismissible?:boolean;
  onDismiss?:  () => void;
  className?:  string;
  actions?:    React.ReactNode;
};

export function Alert({
  variant = "info",
  title,
  children,
  dismissible,
  onDismiss,
  className,
  actions,
}: AlertProps) {
  const [dismissed, setDismissed] = React.useState(false);
  const cfg = variantConfig[variant];
  const { Icon } = cfg;

  if (dismissed) return null;

  const handleDismiss = () => {
    setDismissed(true);
    onDismiss?.();
  };

  return (
    <div
      role="alert"
      className={cn(
        "flex gap-3 p-4 rounded-lg border",
        cfg.wrapper,
        className,
      )}
    >
      <Icon className={cn("size-5 shrink-0 mt-0.5", cfg.icon)} aria-hidden="true" />
      <div className="flex-1 min-w-0">
        {title && (
          <p className={cn("font-semibold text-sm", cfg.title)}>{title}</p>
        )}
        {children && (
          <div className={cn("text-sm mt-0.5", cfg.desc, !title && "font-medium")}>
            {children}
          </div>
        )}
        {actions && <div className="mt-2 flex gap-2">{actions}</div>}
      </div>
      {dismissible && (
        <button
          onClick={handleDismiss}
          aria-label="Dismiss"
          className={cn(
            "shrink-0 p-0.5 rounded hover:bg-black/10 dark:hover:bg-white/10",
            cfg.icon,
          )}
        >
          <X className="size-4" />
        </button>
      )}
    </div>
  );
}
