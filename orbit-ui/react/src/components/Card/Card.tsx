import * as React from "react";
import { cn } from "@/lib/cn";

// ─── Card Root ───────────────────────────────────────────────────────────────

type CardVariant = "default" | "elevated" | "glass" | "flat" | "interactive";

const variantClasses: Record<CardVariant, string> = {
  default:     "bg-surface-base border border-border-default shadow-card",
  elevated:    "bg-surface-elevated border border-border-default shadow-lg",
  glass:       "glass border",
  flat:        "bg-surface-subtle border border-border-subtle",
  interactive: [
    "bg-surface-base border border-border-default shadow-card cursor-pointer",
    "hover:shadow-card-hover hover:border-border-strong",
    "active:shadow-card active:scale-[0.995]",
    "transition-all duration-fast",
  ].join(" "),
};

export type CardProps = {
  variant?:  CardVariant;
  padding?:  "none" | "sm" | "md" | "lg";
  className?:string;
  children:  React.ReactNode;
} & React.HTMLAttributes<HTMLDivElement>;

const paddingClasses = {
  none: "",
  sm:   "p-3",
  md:   "p-4",
  lg:   "p-6",
};

export function Card({
  variant = "default",
  padding = "md",
  className,
  children,
  ...props
}: CardProps) {
  return (
    <div
      className={cn(
        "rounded-card overflow-hidden",
        variantClasses[variant],
        paddingClasses[padding],
        className,
      )}
      {...props}
    >
      {children}
    </div>
  );
}

// ─── Card.Header ─────────────────────────────────────────────────────────────

export type CardHeaderProps = {
  className?: string;
  children:   React.ReactNode;
};

Card.Header = function CardHeader({ className, children }: CardHeaderProps) {
  return (
    <div className={cn("flex items-start justify-between gap-3 mb-4", className)}>
      {children}
    </div>
  );
};

// ─── Card.Title ──────────────────────────────────────────────────────────────

Card.Title = function CardTitle({
  className,
  children,
}: { className?: string; children: React.ReactNode }) {
  return (
    <h3 className={cn("text-base font-semibold text-content-primary", className)}>
      {children}
    </h3>
  );
};

// ─── Card.Description ────────────────────────────────────────────────────────

Card.Description = function CardDescription({
  className,
  children,
}: { className?: string; children: React.ReactNode }) {
  return (
    <p className={cn("text-sm text-content-muted mt-0.5", className)}>
      {children}
    </p>
  );
};

// ─── Card.Body ───────────────────────────────────────────────────────────────

Card.Body = function CardBody({
  className,
  children,
}: { className?: string; children: React.ReactNode }) {
  return <div className={cn("", className)}>{children}</div>;
};

// ─── Card.Footer ─────────────────────────────────────────────────────────────

Card.Footer = function CardFooter({
  className,
  children,
}: { className?: string; children: React.ReactNode }) {
  return (
    <div
      className={cn(
        "flex items-center gap-2 mt-4 pt-4 border-t border-border-subtle",
        className,
      )}
    >
      {children}
    </div>
  );
};

// ─── Card.Divider ────────────────────────────────────────────────────────────

Card.Divider = function CardDivider({ className }: { className?: string }) {
  return <hr className={cn("border-border-subtle my-4", className)} />;
};
