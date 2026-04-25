import * as React from "react";
import { Loader2 } from "lucide-react";
import { cn } from "@/lib/cn";

// ─── Variant & Size Maps ────────────────────────────────────────────────────

const variantClasses = {
  primary: [
    "bg-primary-500 text-white border-transparent",
    "hover:bg-primary-600 active:bg-primary-700",
    "disabled:bg-primary-200 disabled:text-primary-400",
    "dark:disabled:bg-primary-900 dark:disabled:text-primary-700",
  ],
  secondary: [
    "bg-surface-muted text-content-primary border-border-default",
    "hover:bg-surface-subtle hover:border-border-strong active:bg-surface-muted",
    "disabled:opacity-50",
  ],
  outline: [
    "bg-transparent text-primary-600 border-primary-300",
    "hover:bg-primary-50 hover:border-primary-400 active:bg-primary-100",
    "dark:text-primary-400 dark:border-primary-700 dark:hover:bg-primary-950",
    "disabled:opacity-50",
  ],
  ghost: [
    "bg-transparent text-content-secondary border-transparent",
    "hover:bg-surface-muted hover:text-content-primary active:bg-surface-subtle",
    "disabled:opacity-50",
  ],
  danger: [
    "bg-danger-500 text-white border-transparent",
    "hover:bg-danger-600 active:bg-danger-700",
    "disabled:bg-danger-200 disabled:text-danger-400",
  ],
  success: [
    "bg-success-500 text-white border-transparent",
    "hover:bg-success-600 active:bg-success-700",
    "disabled:bg-success-200 disabled:text-success-400",
  ],
  warning: [
    "bg-warning-500 text-white border-transparent",
    "hover:bg-warning-600 active:bg-warning-700",
    "disabled:bg-warning-200 disabled:text-warning-400",
  ],
} as const;

const sizeClasses = {
  xs: "h-7 px-2.5 text-xs gap-1.5 rounded-md",
  sm: "h-8 px-3 text-sm gap-1.5 rounded-md",
  md: "h-9 px-4 text-sm gap-2 rounded-button",
  lg: "h-11 px-5 text-base gap-2 rounded-button",
  xl: "h-12 px-6 text-base gap-2.5 rounded-lg",
} as const;

const iconSizeClasses = {
  xs: "size-3.5",
  sm: "size-4",
  md: "size-4",
  lg: "size-5",
  xl: "size-5",
} as const;

// ─── Types ──────────────────────────────────────────────────────────────────

type ButtonVariant = keyof typeof variantClasses;
type ButtonSize    = keyof typeof sizeClasses;

type ButtonBaseProps = {
  variant?:  ButtonVariant;
  size?:     ButtonSize;
  loading?:  boolean;
  iconLeft?: React.ReactNode;
  iconRight?:React.ReactNode;
  fullWidth?:boolean;
  disabled?: boolean;
};

type ButtonAsButton = ButtonBaseProps &
  Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, keyof ButtonBaseProps> & {
    as?: "button";
  };

type ButtonAsAnchor = ButtonBaseProps &
  Omit<React.AnchorHTMLAttributes<HTMLAnchorElement>, keyof ButtonBaseProps> & {
    as: "a";
  };

export type ButtonProps = ButtonAsButton | ButtonAsAnchor;

// ─── Component ──────────────────────────────────────────────────────────────

export const Button = React.forwardRef<
  HTMLButtonElement | HTMLAnchorElement,
  ButtonProps
>(function Button(
  {
    as: Tag = "button",
    variant = "primary",
    size    = "md",
    loading = false,
    iconLeft,
    iconRight,
    fullWidth = false,
    className,
    children,
    disabled,
    ...props
  },
  ref,
) {
  const isDisabled = disabled || loading;
  const iconSize   = iconSizeClasses[size];

  const classes = cn(
    // Base
    "inline-flex items-center justify-center border font-semibold",
    "whitespace-nowrap select-none",
    "transition-colors duration-fast ease-in-out",
    "focus-ring",
    // Disabled cursor
    isDisabled && "cursor-not-allowed",
    // Full width
    fullWidth && "w-full",
    // Variant
    variantClasses[variant],
    // Size
    sizeClasses[size],
    className,
  );

  const content = (
    <>
      {loading ? (
        <Loader2 className={cn(iconSize, "animate-spin")} aria-hidden="true" />
      ) : (
        iconLeft && (
          <span className={cn(iconSize, "shrink-0")} aria-hidden="true">
            {iconLeft}
          </span>
        )
      )}
      {children && <span>{children}</span>}
      {!loading && iconRight && (
        <span className={cn(iconSize, "shrink-0")} aria-hidden="true">
          {iconRight}
        </span>
      )}
    </>
  );

  if (Tag === "a") {
    return (
      <a
        ref={ref as React.Ref<HTMLAnchorElement>}
        className={classes}
        aria-disabled={isDisabled || undefined}
        {...(props as React.AnchorHTMLAttributes<HTMLAnchorElement>)}
      >
        {content}
      </a>
    );
  }

  return (
    <button
      ref={ref as React.Ref<HTMLButtonElement>}
      className={classes}
      disabled={isDisabled}
      aria-busy={loading || undefined}
      {...(props as React.ButtonHTMLAttributes<HTMLButtonElement>)}
    >
      {content}
    </button>
  );
});

Button.displayName = "Button";
