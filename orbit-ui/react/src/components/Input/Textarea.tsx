import * as React from "react";
import { cn } from "@/lib/cn";

export type TextareaProps = {
  label?:      string;
  helperText?: string;
  errorText?:  string;
  autoResize?: boolean;
  fullWidth?:  boolean;
  wrapperClassName?: string;
} & React.TextareaHTMLAttributes<HTMLTextAreaElement>;

export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  function Textarea(
    { label, helperText, errorText, autoResize, fullWidth, id, className, wrapperClassName, onChange, ...props },
    ref,
  ) {
    const textareaId = id ?? React.useId();
    const helperTextId = `${textareaId}-helper`;
    const errorTextId  = `${textareaId}-error`;
    const hasError = Boolean(errorText);

    const handleChange = React.useCallback(
      (e: React.ChangeEvent<HTMLTextAreaElement>) => {
        if (autoResize) {
          e.target.style.height = "auto";
          e.target.style.height = `${e.target.scrollHeight}px`;
        }
        onChange?.(e);
      },
      [autoResize, onChange],
    );

    return (
      <div className={cn("flex flex-col gap-1.5", fullWidth && "w-full", wrapperClassName)}>
        {label && (
          <label htmlFor={textareaId} className="text-sm font-medium text-content-secondary">
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          id={textareaId}
          aria-invalid={hasError || undefined}
          aria-describedby={errorText ? errorTextId : helperText ? helperTextId : undefined}
          onChange={handleChange}
          className={cn(
            "w-full border bg-surface-base text-content-primary rounded-input",
            "px-3 py-2 text-sm",
            "placeholder:text-content-muted",
            "transition-colors duration-fast",
            "focus-ring focus:border-border-focus",
            "disabled:cursor-not-allowed disabled:opacity-60 disabled:bg-surface-muted",
            "scrollbar-thin",
            autoResize && "resize-none overflow-hidden",
            !autoResize && "min-h-[80px] resize-y",
            hasError
              ? "border-danger-500 focus:border-danger-500 focus-visible:outline-danger-500"
              : "border-border-default hover:border-border-strong",
            className,
          )}
          {...props}
        />
        {!hasError && helperText && (
          <p id={helperTextId} className="text-xs text-content-muted">{helperText}</p>
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

Textarea.displayName = "Textarea";
