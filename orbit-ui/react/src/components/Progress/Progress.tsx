import { cn } from "@/lib/cn";

// ─── Types ──────────────────────────────────────────────────────────────────

type ProgressVariant = "default" | "success" | "warning" | "danger";
type ProgressSize   = "xs" | "sm" | "md" | "lg";

const trackHeight: Record<ProgressSize, string> = {
  xs: "h-1",
  sm: "h-1.5",
  md: "h-2",
  lg: "h-3",
};

const fillColor: Record<ProgressVariant, string> = {
  default: "bg-primary-500",
  success: "bg-success-500",
  warning: "bg-warning-500",
  danger:  "bg-danger-500",
};

export type ProgressProps = {
  value:       number;          // 0–100
  max?:        number;
  variant?:    ProgressVariant;
  size?:       ProgressSize;
  label?:      string;
  showValue?:  boolean;
  animated?:   boolean;
  className?:  string;
};

export function Progress({
  value,
  max = 100,
  variant  = "default",
  size     = "md",
  label,
  showValue = false,
  animated  = false,
  className,
}: ProgressProps) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));

  return (
    <div className={cn("flex flex-col gap-1.5 w-full", className)}>
      {(label || showValue) && (
        <div className="flex justify-between items-center">
          {label && (
            <span className="text-sm font-medium text-content-primary">{label}</span>
          )}
          {showValue && (
            <span className="text-xs text-content-muted tabular-nums">
              {Math.round(pct)}%
            </span>
          )}
        </div>
      )}
      <div
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
        aria-label={label}
        className={cn(
          "w-full rounded-full bg-surface-muted overflow-hidden",
          trackHeight[size],
        )}
      >
        <div
          className={cn(
            "h-full rounded-full transition-[width] duration-500 ease-out",
            fillColor[variant],
            animated && "animate-pulse",
          )}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

// ─── Stacked / multi-segment variant ─────────────────────────────────────────

export type ProgressSegment = {
  value:   number;
  variant: ProgressVariant;
  label?:  string;
};

export type ProgressStackedProps = {
  segments: ProgressSegment[];
  size?:    ProgressSize;
  className?:string;
};

export function ProgressStacked({
  segments,
  size = "md",
  className,
}: ProgressStackedProps) {
  const total = segments.reduce((s, seg) => s + seg.value, 0);

  return (
    <div
      className={cn(
        "flex w-full rounded-full overflow-hidden bg-surface-muted",
        trackHeight[size],
        className,
      )}
      role="progressbar"
    >
      {segments.map((seg, i) => (
        <div
          key={i}
          className={cn(
            "h-full transition-[width] duration-500 ease-out",
            fillColor[seg.variant],
            i > 0 && "ml-px",
          )}
          style={{ width: `${(seg.value / total) * 100}%` }}
          aria-label={seg.label}
        />
      ))}
    </div>
  );
}
