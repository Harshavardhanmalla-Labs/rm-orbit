import * as React from "react";
import { cn } from "@/lib/cn";

export type SkeletonProps = {
  className?: string;
  width?:     string | number;
  height?:    string | number;
  circle?:    boolean;
  style?:     React.CSSProperties;
};

export function Skeleton({ className, width, height, circle }: SkeletonProps) {
  return (
    <span
      aria-hidden="true"
      className={cn("skeleton inline-block", circle && "rounded-full", className)}
      style={{ width, height }}
    />
  );
}

// ─── Skeleton presets ────────────────────────────────────────────────────────

export function SkeletonText({ lines = 3, className }: { lines?: number; className?: string }) {
  return (
    <div className={cn("flex flex-col gap-2", className)}>
      {Array.from({ length: lines }, (_, i) => (
        <Skeleton
          key={i}
          height={14}
          className="rounded"
          style={{ width: i === lines - 1 ? "65%" : "100%" } as React.CSSProperties}
        />
      ))}
    </div>
  );
}

export function SkeletonCard({ className }: { className?: string }) {
  return (
    <div className={cn("rounded-card border border-border-default p-4 flex flex-col gap-3", className)}>
      <div className="flex items-center gap-3">
        <Skeleton circle width={40} height={40} />
        <div className="flex-1 flex flex-col gap-1.5">
          <Skeleton height={14} className="rounded w-1/3" />
          <Skeleton height={12} className="rounded w-1/2" />
        </div>
      </div>
      <SkeletonText lines={2} />
    </div>
  );
}
