import * as React from "react";
import { Loader2 } from "lucide-react";
import { cn } from "@/lib/cn";

const variantClasses = {
  primary:   "bg-primary-500 text-white hover:bg-primary-600 active:bg-primary-700 disabled:bg-primary-200",
  secondary: "bg-surface-muted text-content-secondary border border-border-default hover:bg-surface-subtle hover:text-content-primary disabled:opacity-50",
  ghost:     "bg-transparent text-content-muted hover:bg-surface-muted hover:text-content-primary disabled:opacity-50",
  danger:    "bg-danger-500 text-white hover:bg-danger-600 active:bg-danger-700 disabled:bg-danger-200",
} as const;

const sizeClasses = {
  xs: "size-7 rounded-md [&_svg]:size-3.5",
  sm: "size-8 rounded-md [&_svg]:size-4",
  md: "size-9 rounded-button [&_svg]:size-4",
  lg: "size-11 rounded-button [&_svg]:size-5",
  xl: "size-12 rounded-lg [&_svg]:size-5",
} as const;

export type IconButtonProps = {
  variant?:  keyof typeof variantClasses;
  size?:     keyof typeof sizeClasses;
  loading?:  boolean;
  label:     string; // required for accessibility
  children:  React.ReactNode;
  className?:string;
} & Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, "children">;

export const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(
  function IconButton(
    { variant = "ghost", size = "md", loading, label, children, className, disabled, ...props },
    ref,
  ) {
    return (
      <button
        ref={ref}
        aria-label={label}
        aria-busy={loading || undefined}
        disabled={disabled || loading}
        className={cn(
          "inline-flex items-center justify-center shrink-0",
          "transition-colors duration-fast",
          "focus-ring",
          "disabled:cursor-not-allowed",
          variantClasses[variant],
          sizeClasses[size],
          className,
        )}
        {...props}
      >
        {loading ? (
          <Loader2 className="animate-spin" aria-hidden="true" />
        ) : (
          children
        )}
      </button>
    );
  },
);

IconButton.displayName = "IconButton";
