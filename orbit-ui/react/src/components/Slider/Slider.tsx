import * as React from "react";
import { cn } from "@/lib/cn";

// ─── Types ────────────────────────────────────────────────────────────────────

export type SliderProps = {
  value?:         number | [number, number];
  defaultValue?:  number | [number, number];
  onChange?:      (value: number | [number, number]) => void;
  min?:           number;
  max?:           number;
  step?:          number;
  size?:          "sm" | "md" | "lg";
  disabled?:      boolean;
  showTooltip?:   boolean;
  showTicks?:     boolean;
  marks?:         { value: number; label?: string }[];
  formatValue?:   (v: number) => string;
  className?:     string;
};

// ─── Sizes ────────────────────────────────────────────────────────────────────

const trackH  = { sm: "h-1",   md: "h-1.5",  lg: "h-2" };
const thumbSz = { sm: "w-3.5 h-3.5", md: "w-4 h-4", lg: "w-5 h-5" };

// ─── Slider ───────────────────────────────────────────────────────────────────

export function Slider({
  value: controlledValue,
  defaultValue,
  onChange,
  min = 0,
  max = 100,
  step = 1,
  size = "md",
  disabled = false,
  showTooltip = true,
  showTicks: _showTicks = false,
  marks,
  formatValue,
  className,
}: SliderProps) {
  const isRange    = Array.isArray(controlledValue) || Array.isArray(defaultValue);
  const isControlled = controlledValue !== undefined;

  const initValue = (): number | [number, number] => {
    if (defaultValue !== undefined) return defaultValue;
    return isRange ? [min, max] : min;
  };

  const [internal, setInternal] = React.useState<number | [number, number]>(initValue);
  const val = isControlled ? controlledValue! : internal;

  const singleVal  = isRange ? 0 : (val as number);
  const [lo, hi]   = isRange ? (val as [number, number]) : [min, max];

  const pct  = (v: number) => ((v - min) / (max - min)) * 100;
  const fmt  = (v: number) => formatValue ? formatValue(v) : String(v);

  const commit = (next: number | [number, number]) => {
    if (!isControlled) setInternal(next);
    onChange?.(next);
  };

  const clampStep = (v: number) =>
    Math.round(Math.min(max, Math.max(min, v)) / step) * step;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>, which: "lo" | "hi" | "single") => {
    const raw = parseFloat(e.target.value);
    if (which === "single") { commit(clampStep(raw)); return; }
    if (which === "lo") {
      const next: [number, number] = [Math.min(clampStep(raw), hi - step), hi];
      commit(next);
    } else {
      const next: [number, number] = [lo, Math.max(clampStep(raw), lo + step)];
      commit(next);
    }
  };

  const rangeLeft  = isRange ? pct(lo)  : 0;
  const rangeRight = isRange ? pct(hi)  : pct(singleVal);
  const fillLeft   = isRange ? rangeLeft : 0;
  const fillWidth  = isRange ? rangeRight - rangeLeft : rangeRight;

  const trackStyle: React.CSSProperties = {
    background: `linear-gradient(to right,
      var(--color-border-default, #e5e7eb) 0% ${fillLeft}%,
      var(--color-interactive-primary, #2563eb) ${fillLeft}% ${fillLeft + fillWidth}%,
      var(--color-border-default, #e5e7eb) ${fillLeft + fillWidth}% 100%
    )`,
  };

  const inputBase = cn(
    "absolute inset-0 w-full opacity-0 cursor-pointer",
    "h-full appearance-none",
    disabled && "cursor-not-allowed",
  );

  return (
    <div className={cn("w-full", className)}>
      <div className="relative flex items-center py-3">
        {/* Track */}
        <div
          className={cn("w-full rounded-full", trackH[size])}
          style={trackStyle}
        />

        {/* Range input(s) */}
        {!isRange ? (
          <input
            type="range"
            min={min}
            max={max}
            step={step}
            value={singleVal}
            disabled={disabled}
            onChange={(e) => handleChange(e, "single")}
            className={inputBase}
            aria-valuemin={min}
            aria-valuemax={max}
            aria-valuenow={singleVal}
            aria-valuetext={fmt(singleVal)}
          />
        ) : (
          <>
            <input
              type="range"
              min={min}
              max={max}
              step={step}
              value={lo}
              disabled={disabled}
              onChange={(e) => handleChange(e, "lo")}
              className={inputBase}
              style={{ zIndex: lo > max - step ? 5 : 3 }}
              aria-label="Lower bound"
            />
            <input
              type="range"
              min={min}
              max={max}
              step={step}
              value={hi}
              disabled={disabled}
              onChange={(e) => handleChange(e, "hi")}
              className={cn(inputBase, "z-4")}
              style={{ zIndex: 4 }}
              aria-label="Upper bound"
            />
          </>
        )}

        {/* Thumbs (visual only) */}
        {!isRange ? (
          <span
            aria-hidden="true"
            className={cn(
              "absolute pointer-events-none rounded-full border-2 border-interactive-primary bg-white shadow",
              "transition-shadow hover:shadow-interactive-primary/30",
              thumbSz[size],
            )}
            style={{ left: `calc(${pct(singleVal)}% - 8px)` }}
          >
            {showTooltip && (
              <span className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-1.5 py-0.5 rounded text-xs font-medium bg-neutral-800 text-white whitespace-nowrap opacity-0 group-hover:opacity-100 pointer-events-none">
                {fmt(singleVal)}
              </span>
            )}
          </span>
        ) : (
          <>
            <span
              aria-hidden="true"
              className={cn(
                "absolute pointer-events-none rounded-full border-2 border-interactive-primary bg-white shadow",
                thumbSz[size],
              )}
              style={{ left: `calc(${pct(lo)}% - 8px)` }}
            />
            <span
              aria-hidden="true"
              className={cn(
                "absolute pointer-events-none rounded-full border-2 border-interactive-primary bg-white shadow",
                thumbSz[size],
              )}
              style={{ left: `calc(${pct(hi)}% - 8px)` }}
            />
          </>
        )}
      </div>

      {/* Value labels */}
      {!marks && (
        <div className="flex justify-between text-xs text-content-muted">
          <span>{fmt(min)}</span>
          <span>{isRange ? `${fmt(lo)} – ${fmt(hi)}` : fmt(singleVal)}</span>
          <span>{fmt(max)}</span>
        </div>
      )}

      {/* Marks */}
      {marks && (
        <div className="relative w-full">
          {marks.map((mark) => (
            <span
              key={mark.value}
              className="absolute -translate-x-1/2 text-xs text-content-muted mt-1"
              style={{ left: `${pct(mark.value)}%` }}
            >
              {mark.label ?? fmt(mark.value)}
            </span>
          ))}
          <div className="h-4" />
        </div>
      )}
    </div>
  );
}
