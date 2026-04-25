import { cn } from "@/lib/cn";

const sizeClasses = {
  xs: "size-3 border-[1.5px]",
  sm: "size-4 border-2",
  md: "size-5 border-2",
  lg: "size-8 border-[3px]",
  xl: "size-12 border-4",
} as const;

const colorClasses = {
  primary: "border-primary-200 border-t-primary-500",
  white:   "border-white/30 border-t-white",
  muted:   "border-border-default border-t-content-muted",
} as const;

export type SpinnerProps = {
  size?:      keyof typeof sizeClasses;
  color?:     keyof typeof colorClasses;
  label?:     string;
  className?: string;
};

export function Spinner({ size = "md", color = "primary", label = "Loading…", className }: SpinnerProps) {
  return (
    <span
      role="status"
      aria-label={label}
      className={cn(
        "inline-block rounded-full animate-spin",
        sizeClasses[size],
        colorClasses[color],
        className,
      )}
    />
  );
}

// ─── Full-page overlay loader ────────────────────────────────────────────────

export function PageLoader({ label = "Loading…" }: { label?: string }) {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-surface-overlay z-modal">
      <div className="flex flex-col items-center gap-3">
        <Spinner size="xl" />
        <p className="text-sm text-content-muted animate-fade-in">{label}</p>
      </div>
    </div>
  );
}
