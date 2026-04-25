import * as React from "react";
import { cn } from "@/lib/cn";

export type SwitchProps = {
  checked?:        boolean;
  defaultChecked?: boolean;
  onChange?:       (checked: boolean) => void;
  disabled?:       boolean;
  label?:          React.ReactNode;
  description?:    string;
  id?:             string;
  size?:           "sm" | "md";
  className?:      string;
};

const trackSize = {
  sm: "w-7 h-4",
  md: "w-9 h-5",
} as const;

const thumbSize = {
  sm: "size-3",
  md: "size-3.5",
} as const;

const thumbTranslate = {
  sm: "translate-x-3.5",
  md: "translate-x-4.5",
} as const;

export const Switch = React.forwardRef<HTMLInputElement, SwitchProps>(
  function Switch(
    {
      checked,
      defaultChecked,
      onChange,
      disabled = false,
      label,
      description,
      id,
      size = "md",
      className,
    },
    ref,
  ) {
    const generatedId = React.useId();
    const inputId = id ?? generatedId;

    const [internalChecked, setInternalChecked] = React.useState(
      defaultChecked ?? false,
    );
    const isControlled = checked !== undefined;
    const isChecked = isControlled ? checked : internalChecked;

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      if (!isControlled) setInternalChecked(e.target.checked);
      onChange?.(e.target.checked);
    };

    return (
      <label
        htmlFor={inputId}
        className={cn(
          "inline-flex items-start gap-2.5 group",
          disabled ? "cursor-not-allowed opacity-50" : "cursor-pointer",
          className,
        )}
      >
        <span className="relative flex shrink-0 mt-0.5">
          <input
            ref={ref}
            id={inputId}
            type="checkbox"
            role="switch"
            aria-checked={isChecked}
            checked={isChecked}
            disabled={disabled}
            onChange={handleChange}
            className="sr-only"
          />
          {/* Track */}
          <span
            className={cn(
              trackSize[size],
              "relative flex items-center rounded-full transition-colors duration-fast",
              isChecked ? "bg-primary-500" : "bg-border-strong",
              "focus-within:ring-2 focus-within:ring-primary-400 focus-within:ring-offset-1",
            )}
            aria-hidden="true"
          >
            {/* Thumb */}
            <span
              className={cn(
                thumbSize[size],
                "absolute left-0.5 rounded-full bg-white shadow-sm",
                "transition-transform duration-fast",
                isChecked ? thumbTranslate[size] : "translate-x-0",
              )}
            />
          </span>
        </span>
        {(label || description) && (
          <span className="flex flex-col gap-0.5">
            {label && (
              <span className="text-sm font-medium text-content-primary leading-none">
                {label}
              </span>
            )}
            {description && (
              <span className="text-xs text-content-muted">{description}</span>
            )}
          </span>
        )}
      </label>
    );
  },
);

Switch.displayName = "Switch";
