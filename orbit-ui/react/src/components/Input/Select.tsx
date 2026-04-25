import * as React from "react";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/cn";

const sizeClasses = {
  sm: "h-8 text-sm pl-3 pr-8 rounded-md",
  md: "h-9 text-sm pl-3 pr-9 rounded-input",
  lg: "h-11 text-base pl-4 pr-10 rounded-input",
} as const;

export type SelectProps = {
  size?:       keyof typeof sizeClasses;
  label?:      string;
  helperText?: string;
  errorText?:  string;
  placeholder?:string;
  fullWidth?:  boolean;
  wrapperClassName?: string;
} & Omit<React.SelectHTMLAttributes<HTMLSelectElement>, "size">;

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  function Select(
    { size = "md", label, helperText, errorText, placeholder, fullWidth, id, className, wrapperClassName, children, ...props },
    ref,
  ) {
    const selectId = id ?? React.useId();
    const hasError = Boolean(errorText);

    return (
      <div className={cn("flex flex-col gap-1.5", fullWidth && "w-full", wrapperClassName)}>
        {label && (
          <label htmlFor={selectId} className="text-sm font-medium text-content-secondary">
            {label}
          </label>
        )}
        <div className="relative">
          <select
            ref={ref}
            id={selectId}
            aria-invalid={hasError || undefined}
            className={cn(
              "w-full appearance-none",
              "border bg-surface-base text-content-primary",
              "transition-colors duration-fast",
              "focus-ring focus:border-border-focus",
              "disabled:cursor-not-allowed disabled:opacity-60 disabled:bg-surface-muted",
              hasError
                ? "border-danger-500"
                : "border-border-default hover:border-border-strong",
              sizeClasses[size],
              className,
            )}
            {...props}
          >
            {placeholder && (
              <option value="" disabled>
                {placeholder}
              </option>
            )}
            {children}
          </select>
          <span className="pointer-events-none absolute right-2.5 top-1/2 -translate-y-1/2 text-content-muted">
            <ChevronDown className="size-4" />
          </span>
        </div>
        {!hasError && helperText && (
          <p className="text-xs text-content-muted">{helperText}</p>
        )}
        {hasError && (
          <p className="text-xs text-danger-600 dark:text-danger-400" role="alert">{errorText}</p>
        )}
      </div>
    );
  },
);

Select.displayName = "Select";
