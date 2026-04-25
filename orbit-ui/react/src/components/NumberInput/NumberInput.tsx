import * as React from "react";
import { ChevronUp, ChevronDown } from "lucide-react";
import { cn } from "@/lib/cn";

// ─── Types ────────────────────────────────────────────────────────────────────

export type NumberInputProps = {
  value?:         number;
  defaultValue?:  number;
  onChange?:      (value: number) => void;
  min?:           number;
  max?:           number;
  step?:          number;
  precision?:     number;
  prefix?:        React.ReactNode;
  suffix?:        React.ReactNode;
  size?:          "sm" | "md" | "lg";
  disabled?:      boolean;
  readOnly?:      boolean;
  placeholder?:   string;
  className?:     string;
  formatDisplay?: (value: number) => string;
} & Omit<React.InputHTMLAttributes<HTMLInputElement>, "value" | "onChange" | "type" | "size">;

// ─── Helpers ──────────────────────────────────────────────────────────────────

function clamp(val: number, min?: number, max?: number) {
  if (min !== undefined && val < min) return min;
  if (max !== undefined && val > max) return max;
  return val;
}

function round(val: number, precision: number) {
  const factor = Math.pow(10, precision);
  return Math.round(val * factor) / factor;
}

// ─── Sizes ────────────────────────────────────────────────────────────────────

const sizeClasses = {
  sm: "h-8  text-sm px-2.5",
  md: "h-10 text-sm px-3",
  lg: "h-11 text-base px-3.5",
};

const btnClasses = {
  sm: "w-6",
  md: "w-7",
  lg: "w-8",
};

// ─── NumberInput ──────────────────────────────────────────────────────────────

export function NumberInput({
  value: controlledValue,
  defaultValue,
  onChange,
  min,
  max,
  step = 1,
  precision = 0,
  prefix,
  suffix,
  size = "md",
  disabled = false,
  readOnly = false,
  placeholder,
  className,
  formatDisplay,
  ...rest
}: NumberInputProps) {
  const isControlled = controlledValue !== undefined;
  const [internal, setInternal] = React.useState<number>(defaultValue ?? 0);
  const [text, setText] = React.useState<string>("");
  const [focused, setFocused] = React.useState(false);

  const value = isControlled ? controlledValue! : internal;

  React.useEffect(() => {
    if (!focused) {
      setText(
        formatDisplay
          ? formatDisplay(value)
          : precision > 0
          ? value.toFixed(precision)
          : String(value),
      );
    }
  }, [value, focused, formatDisplay, precision]);

  const commit = (raw: string) => {
    const parsed = parseFloat(raw);
    if (isNaN(parsed)) {
      setText(String(value));
      return;
    }
    const next = clamp(round(parsed, precision), min, max);
    if (!isControlled) setInternal(next);
    onChange?.(next);
    setText(
      formatDisplay ? formatDisplay(next) : precision > 0 ? next.toFixed(precision) : String(next),
    );
  };

  const increment = () => {
    const next = clamp(round(value + step, precision), min, max);
    if (!isControlled) setInternal(next);
    onChange?.(next);
  };

  const decrement = () => {
    const next = clamp(round(value - step, precision), min, max);
    if (!isControlled) setInternal(next);
    onChange?.(next);
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "ArrowUp")   { e.preventDefault(); increment(); }
    if (e.key === "ArrowDown") { e.preventDefault(); decrement(); }
    if (e.key === "Enter")     { commit(text); }
  };

  const canInc = max === undefined || value < max;
  const canDec = min === undefined || value > min;

  return (
    <div
      className={cn(
        "inline-flex items-stretch rounded-input border border-border-default bg-surface-base",
        "focus-within:border-interactive-primary focus-within:ring-2 focus-within:ring-interactive-primary/20",
        "transition-colors overflow-hidden",
        disabled && "opacity-50 cursor-not-allowed",
        className,
      )}
    >
      {prefix && (
        <span className="flex items-center px-2.5 bg-surface-muted border-r border-border-default text-content-muted text-sm flex-shrink-0">
          {prefix}
        </span>
      )}

      <input
        {...rest}
        type="text"
        inputMode="decimal"
        value={focused ? text : (formatDisplay ? formatDisplay(value) : text)}
        onChange={(e) => setText(e.target.value)}
        onFocus={() => { setFocused(true); setText(String(value)); }}
        onBlur={(e) => { setFocused(false); commit(e.target.value); }}
        onKeyDown={onKeyDown}
        disabled={disabled}
        readOnly={readOnly}
        placeholder={placeholder}
        aria-valuemin={min}
        aria-valuemax={max}
        aria-valuenow={value}
        className={cn(
          "flex-1 min-w-0 outline-none bg-transparent text-content-primary",
          "placeholder:text-content-muted",
          sizeClasses[size],
          disabled && "cursor-not-allowed",
        )}
      />

      {suffix && (
        <span className="flex items-center px-2.5 bg-surface-muted border-l border-border-default text-content-muted text-sm flex-shrink-0">
          {suffix}
        </span>
      )}

      {/* Spin buttons */}
      <div className={cn("flex flex-col border-l border-border-default", btnClasses[size])}>
        <button
          type="button"
          tabIndex={-1}
          aria-label="Increment"
          disabled={disabled || readOnly || !canInc}
          onClick={increment}
          className={cn(
            "flex-1 flex items-center justify-center",
            "text-content-muted hover:bg-surface-muted hover:text-content-primary",
            "transition-colors border-b border-border-default",
            (disabled || !canInc) && "cursor-not-allowed opacity-40",
          )}
        >
          <ChevronUp className="w-3 h-3" />
        </button>
        <button
          type="button"
          tabIndex={-1}
          aria-label="Decrement"
          disabled={disabled || readOnly || !canDec}
          onClick={decrement}
          className={cn(
            "flex-1 flex items-center justify-center",
            "text-content-muted hover:bg-surface-muted hover:text-content-primary",
            "transition-colors",
            (disabled || !canDec) && "cursor-not-allowed opacity-40",
          )}
        >
          <ChevronDown className="w-3 h-3" />
        </button>
      </div>
    </div>
  );
}
