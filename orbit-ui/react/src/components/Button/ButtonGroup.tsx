import * as React from "react";
import { cn } from "@/lib/cn";

// ─── Types ────────────────────────────────────────────────────────────────────

export type ButtonGroupProps = {
  children:     React.ReactNode;
  orientation?: "horizontal" | "vertical";
  size?:        "sm" | "md" | "lg";
  variant?:     "default" | "outline" | "ghost";
  attached?:    boolean;
  className?:   string;
};

// ─── ButtonGroup ──────────────────────────────────────────────────────────────

export function ButtonGroup({
  children,
  orientation = "horizontal",
  attached = true,
  className,
}: ButtonGroupProps) {
  const isHoriz = orientation === "horizontal";

  return (
    <div
      role="group"
      className={cn(
        "inline-flex",
        isHoriz ? "flex-row" : "flex-col",
        attached && [
          isHoriz
            ? "[&>*:not(:first-child)]:rounded-l-none [&>*:not(:last-child)]:rounded-r-none [&>*:not(:first-child)]:-ml-px"
            : "[&>*:not(:first-child)]:rounded-t-none [&>*:not(:last-child)]:rounded-b-none [&>*:not(:first-child)]:-mt-px",
        ],
        className,
      )}
    >
      {children}
    </div>
  );
}
