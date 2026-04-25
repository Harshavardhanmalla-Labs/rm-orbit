import * as React from "react";
import { cn } from "@/lib/cn";

// ─── Types ──────────────────────────────────────────────────────────────────

const sizeClasses = {
  sm: "h-8 text-sm px-3 rounded-md",
  md: "h-9 text-sm px-3 rounded-input",
  lg: "h-11 text-base px-4 rounded-input",
} as const;

export type InputProps = {
  size?:       keyof typeof sizeClasses;
  label?:      string;
  helperText?: string;
  errorText?:  string;
  prefix?:     React.ReactNode; // icon or text on the left
  suffix?:     React.ReactNode; // icon or text on the right
  fullWidth?:  boolean;
  wrapperClassName?: string;
} & Omit<React.InputHTMLAttributes<HTMLInputElement>, "size" | "prefix">;

// ─── Component ──────────────────────────────────────────────────────────────

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  function Input(
    {
      size       = "md",
      label,
      helperText,
      errorText,
      prefix,
      suffix,
      fullWidth  = false,
      id,
      className,
      wrapperClassName,
      disabled,
      ...props
    },
    ref,
  ) {
    const inputId      = id ?? React.useId();
    const helperTextId = `${inputId}-helper`;
    const errorTextId  = `${inputId}-error`;
    const hasError     = Boolean(errorText);

    return (
      <div className={cn("flex flex-col gap-1.5", fullWidth && "w-full", wrapperClassName)}>
        {label && (
          <label
            htmlFor={inputId}
            className="text-sm font-medium text-content-secondary"
          >
            {label}
          </label>
        )}

        <div className="relative flex items-center">
          {prefix && (
            <span
              className="absolute left-3 flex items-center text-content-muted pointer-events-none [&_svg]:size-4"
              aria-hidden="true"
            >
              {prefix}
            </span>
          )}

          <input
            ref={ref}
            id={inputId}
            disabled={disabled}
            aria-invalid={hasError || undefined}
            aria-describedby={
              errorText
                ? errorTextId
                : helperText
                ? helperTextId
                : undefined
            }
            className={cn(
              // Base
              "w-full border bg-surface-base text-content-primary",
              "placeholder:text-content-muted",
              "transition-colors duration-fast",
              "focus-ring focus:border-border-focus",
              // Disabled
              "disabled:cursor-not-allowed disabled:opacity-60 disabled:bg-surface-muted",
              // Error state
              hasError
                ? "border-danger-500 focus:border-danger-500 focus-visible:outline-danger-500"
                : "border-border-default hover:border-border-strong",
              // Size
              sizeClasses[size],
              // Prefix/suffix padding adjustments
              prefix && "pl-9",
              suffix && "pr-9",
              className,
            )}
            {...props}
          />

          {suffix && (
            <span
              className="absolute right-3 flex items-center text-content-muted pointer-events-none [&_svg]:size-4"
              aria-hidden="true"
            >
              {suffix}
            </span>
          )}
        </div>

        {!hasError && helperText && (
          <p id={helperTextId} className="text-xs text-content-muted">
            {helperText}
          </p>
        )}
        {hasError && (
          <p id={errorTextId} className="text-xs text-danger-600 dark:text-danger-400" role="alert">
            {errorText}
          </p>
        )}
      </div>
    );
  },
);

Input.displayName = "Input";
