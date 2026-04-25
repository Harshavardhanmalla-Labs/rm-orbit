import * as React from "react";
import { cn } from "@/lib/cn";

// ─── Context ──────────────────────────────────────────────────────────────────

type RadioGroupContextValue = {
  name:     string;
  value:    string;
  onChange: (value: string) => void;
  size:     "sm" | "md";
  disabled: boolean;
};

const RadioGroupContext = React.createContext<RadioGroupContextValue | null>(null);

function useRadioGroup() {
  return React.useContext(RadioGroupContext);
}

// ─── RadioGroup ───────────────────────────────────────────────────────────────

export type RadioGroupProps = {
  name:         string;
  value?:       string;
  defaultValue?: string;
  onChange?:    (value: string) => void;
  size?:        "sm" | "md";
  disabled?:    boolean;
  orientation?: "horizontal" | "vertical";
  label?:       string;
  children:     React.ReactNode;
  className?:   string;
};

export function RadioGroup({
  name,
  value: controlledValue,
  defaultValue = "",
  onChange,
  size = "md",
  disabled = false,
  orientation = "vertical",
  label,
  children,
  className,
}: RadioGroupProps) {
  const [internalValue, setInternalValue] = React.useState(defaultValue);
  const isControlled = controlledValue !== undefined;
  const value = isControlled ? controlledValue : internalValue;

  const handleChange = React.useCallback(
    (v: string) => {
      if (!isControlled) setInternalValue(v);
      onChange?.(v);
    },
    [isControlled, onChange],
  );

  return (
    <RadioGroupContext.Provider value={{ name, value, onChange: handleChange, size, disabled }}>
      <fieldset className={cn("border-0 p-0 m-0", className)} disabled={disabled}>
        {label && (
          <legend className="text-sm font-medium text-content-primary mb-2">{label}</legend>
        )}
        <div
          role="radiogroup"
          className={cn(
            "flex gap-2",
            orientation === "vertical" ? "flex-col" : "flex-row flex-wrap",
          )}
        >
          {children}
        </div>
      </fieldset>
    </RadioGroupContext.Provider>
  );
}

// ─── Radio ────────────────────────────────────────────────────────────────────

export type RadioProps = {
  value:        string;
  label?:       React.ReactNode;
  description?: string;
  disabled?:    boolean;
  className?:   string;
} & Omit<React.InputHTMLAttributes<HTMLInputElement>, "type" | "value" | "size">;

const dotSizeMap = {
  sm: "w-2 h-2",
  md: "w-2.5 h-2.5",
};

const ringMap = {
  sm: "w-3.5 h-3.5",
  md: "w-4 h-4",
};

export function Radio({ value, label, description, disabled: propDisabled, className, ...rest }: RadioProps) {
  const group = useRadioGroup();

  if (!group) {
    throw new Error("<Radio> must be used inside <RadioGroup>");
  }

  const { name, value: groupValue, onChange, size, disabled: groupDisabled } = group;
  const disabled = propDisabled ?? groupDisabled;
  const checked = groupValue === value;

  return (
    <label
      className={cn(
        "inline-flex items-start gap-2.5 cursor-pointer select-none",
        disabled && "cursor-not-allowed opacity-50",
        className,
      )}
    >
      <span className="relative flex-shrink-0 mt-0.5">
        {/* Hidden native input for accessibility */}
        <input
          type="radio"
          name={name}
          value={value}
          checked={checked}
          disabled={disabled}
          onChange={() => !disabled && onChange(value)}
          className="sr-only"
          {...rest}
        />
        {/* Custom ring */}
        <span
          aria-hidden="true"
          className={cn(
            "flex items-center justify-center rounded-full border-2 transition-colors duration-fast",
            ringMap[size],
            checked
              ? "border-interactive-primary bg-interactive-primary"
              : "border-border-strong bg-surface-base",
            !disabled && !checked && "hover:border-interactive-primary",
          )}
        >
          {checked && (
            <span
              className={cn(
                "rounded-full bg-white flex-shrink-0",
                dotSizeMap[size],
              )}
            />
          )}
        </span>
      </span>

      {(label || description) && (
        <span className="flex flex-col gap-0.5">
          {label && (
            <span
              className={cn(
                "font-medium text-content-primary",
                size === "sm" ? "text-sm" : "text-sm",
              )}
            >
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
}
