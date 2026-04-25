import * as React from "react";
import { Check, Minus } from "lucide-react";
import { cn } from "@/lib/cn";

export type CheckboxProps = {
  checked?:        boolean;
  defaultChecked?: boolean;
  indeterminate?:  boolean;
  onChange?:       (checked: boolean) => void;
  disabled?:       boolean;
  label?:          React.ReactNode;
  description?:    string;
  id?:             string;
  className?:      string;
  size?:           "sm" | "md";
};

export const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  function Checkbox(
    {
      checked,
      defaultChecked,
      indeterminate = false,
      onChange,
      disabled = false,
      label,
      description,
      id,
      className,
      size = "md",
    },
    ref,
  ) {
    const innerRef = React.useRef<HTMLInputElement>(null);
    const resolvedRef = ref
      ? (ref as React.RefObject<HTMLInputElement>)
      : innerRef;
    const generatedId = React.useId();
    const inputId = id ?? generatedId;

    // Sync indeterminate DOM property
    React.useEffect(() => {
      if (resolvedRef.current) {
        resolvedRef.current.indeterminate = indeterminate;
      }
    }, [indeterminate, resolvedRef]);

    const [internalChecked, setInternalChecked] = React.useState(
      defaultChecked ?? false,
    );
    const isControlled = checked !== undefined;
    const isChecked = isControlled ? checked : internalChecked;

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      if (!isControlled) setInternalChecked(e.target.checked);
      onChange?.(e.target.checked);
    };

    const boxSize = size === "sm" ? "size-3.5" : "size-4";
    const iconSize = size === "sm" ? "size-2.5" : "size-3";

    const active = isChecked || indeterminate;

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
            ref={resolvedRef}
            id={inputId}
            type="checkbox"
            checked={isChecked}
            disabled={disabled}
            onChange={handleChange}
            className="sr-only"
          />
          <span
            className={cn(
              boxSize,
              "flex items-center justify-center rounded border transition-colors duration-fast",
              active
                ? "bg-primary-500 border-primary-500"
                : "bg-surface-default border-border-default group-hover:border-primary-400",
              "focus-within:ring-2 focus-within:ring-primary-400 focus-within:ring-offset-1",
            )}
            aria-hidden="true"
          >
            {indeterminate ? (
              <Minus className={cn(iconSize, "text-white stroke-[3]")} />
            ) : isChecked ? (
              <Check className={cn(iconSize, "text-white stroke-[3]")} />
            ) : null}
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

Checkbox.displayName = "Checkbox";
