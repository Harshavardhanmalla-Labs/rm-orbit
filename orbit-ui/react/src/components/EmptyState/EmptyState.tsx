import * as React from "react";
import { cn } from "@/lib/cn";

export type EmptyStateProps = {
  icon?:        React.ReactNode;
  title:        string;
  description?: string;
  action?:      React.ReactNode;
  size?:        "sm" | "md" | "lg";
  className?:   string;
};

const sizeClasses = {
  sm: { wrapper: "py-8 gap-2",    icon: "size-10 mb-1", title: "text-sm",  desc: "text-xs" },
  md: { wrapper: "py-12 gap-3",   icon: "size-12 mb-2", title: "text-base",desc: "text-sm" },
  lg: { wrapper: "py-16 gap-4",   icon: "size-16 mb-3", title: "text-lg",  desc: "text-base" },
};

export function EmptyState({ icon, title, description, action, size = "md", className }: EmptyStateProps) {
  const s = sizeClasses[size];
  return (
    <div className={cn("flex flex-col items-center justify-center text-center", s.wrapper, className)}>
      {icon && (
        <span className={cn("text-content-muted [&_svg]:size-full", s.icon)}>
          {icon}
        </span>
      )}
      <p className={cn("font-semibold text-content-primary", s.title)}>{title}</p>
      {description && (
        <p className={cn("text-content-muted max-w-xs", s.desc)}>{description}</p>
      )}
      {action && <div className="mt-2">{action}</div>}
    </div>
  );
}
