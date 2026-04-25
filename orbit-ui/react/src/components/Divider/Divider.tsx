import * as React from "react";
import { cn } from "@/lib/cn";

export type DividerProps = {
  orientation?: "horizontal" | "vertical";
  variant?:     "default" | "strong" | "subtle";
  label?:       React.ReactNode;
  className?:   string;
};

const colorClass = {
  default: "border-border-default",
  strong:  "border-border-strong",
  subtle:  "border-border-subtle",
} as const;

export function Divider({
  orientation = "horizontal",
  variant     = "default",
  label,
  className,
}: DividerProps) {
  if (orientation === "vertical") {
    return (
      <div
        role="separator"
        aria-orientation="vertical"
        className={cn(
          "inline-block self-stretch w-px border-l",
          colorClass[variant],
          className,
        )}
      />
    );
  }

  if (label) {
    return (
      <div
        role="separator"
        aria-orientation="horizontal"
        className={cn("flex items-center gap-3 w-full", className)}
      >
        <div className={cn("flex-1 border-t", colorClass[variant])} />
        <span className="text-xs text-content-muted whitespace-nowrap font-medium">
          {label}
        </span>
        <div className={cn("flex-1 border-t", colorClass[variant])} />
      </div>
    );
  }

  return (
    <hr
      role="separator"
      className={cn("border-t w-full", colorClass[variant], className)}
    />
  );
}
