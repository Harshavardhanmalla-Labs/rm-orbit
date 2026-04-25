import * as React from "react";
import { X } from "lucide-react";
import { cn } from "@/lib/cn";

const variantColor = {
  primary: {
    solid:  "bg-primary-500 text-white",
    subtle: "bg-primary-100 text-primary-700 dark:bg-primary-950 dark:text-primary-300",
    outline:"border border-primary-300 text-primary-700 dark:border-primary-700 dark:text-primary-300",
  },
  success: {
    solid:  "bg-success-500 text-white",
    subtle: "bg-success-100 text-success-700 dark:bg-success-950 dark:text-success-300",
    outline:"border border-success-300 text-success-700",
  },
  warning: {
    solid:  "bg-warning-500 text-white",
    subtle: "bg-warning-100 text-warning-700 dark:bg-warning-950 dark:text-warning-300",
    outline:"border border-warning-300 text-warning-700",
  },
  danger: {
    solid:  "bg-danger-500 text-white",
    subtle: "bg-danger-100 text-danger-700 dark:bg-danger-950 dark:text-danger-300",
    outline:"border border-danger-300 text-danger-700",
  },
  info: {
    solid:  "bg-info-500 text-white",
    subtle: "bg-info-100 text-info-700 dark:bg-info-950 dark:text-info-300",
    outline:"border border-info-300 text-info-700",
  },
  neutral: {
    solid:  "bg-neutral-600 text-white dark:bg-neutral-700",
    subtle: "bg-neutral-100 text-neutral-700 dark:bg-neutral-800 dark:text-neutral-300",
    outline:"border border-neutral-300 text-neutral-600 dark:border-neutral-600 dark:text-neutral-400",
  },
} as const;

const sizeClasses = {
  sm: "h-5 px-1.5 text-[11px] gap-1",
  md: "h-6 px-2 text-xs gap-1",
  lg: "h-7 px-2.5 text-sm gap-1.5",
} as const;

export type BadgeProps = {
  color?:     keyof typeof variantColor;
  variant?:   "solid" | "subtle" | "outline";
  size?:      keyof typeof sizeClasses;
  dot?:       boolean;       // small status dot (no text)
  removable?: boolean;
  onRemove?:  () => void;
  children?:  React.ReactNode;
  className?: string;
};

export function Badge({
  color   = "neutral",
  variant = "subtle",
  size    = "md",
  dot     = false,
  removable,
  onRemove,
  children,
  className,
}: BadgeProps) {
  if (dot) {
    return (
      <span
        className={cn(
          "inline-block rounded-full",
          size === "sm" ? "size-1.5" : size === "md" ? "size-2" : "size-2.5",
          // Use background color from solid variant for dot
          variantColor[color].solid.split(" ")[0],
          className,
        )}
      />
    );
  }

  return (
    <span
      className={cn(
        "inline-flex items-center justify-center font-semibold rounded-badge whitespace-nowrap",
        variantColor[color][variant],
        sizeClasses[size],
        className,
      )}
    >
      {children}
      {removable && (
        <button
          type="button"
          onClick={onRemove}
          className="ml-0.5 rounded-full hover:bg-black/10 dark:hover:bg-white/10 p-0.5 focus:outline-none"
          aria-label="Remove"
        >
          <X className="size-2.5" />
        </button>
      )}
    </span>
  );
}
