import * as React from "react";
import { Check, X } from "lucide-react";
import { cn } from "@/lib/cn";

// ─── Types ────────────────────────────────────────────────────────────────────

export type StepStatus = "complete" | "current" | "upcoming" | "error";

export type StepItem = {
  id:          string;
  label:       React.ReactNode;
  description?: React.ReactNode;
  icon?:       React.ReactNode;
  status?:     StepStatus;
};

export type StepsProps = {
  steps:        StepItem[];
  currentStep?: number;
  orientation?: "horizontal" | "vertical";
  size?:        "sm" | "md" | "lg";
  variant?:     "default" | "dots" | "numbered";
  className?:   string;
  onChange?:    (index: number) => void;
};

// ─── Helpers ──────────────────────────────────────────────────────────────────

function resolveStatus(index: number, current: number, override?: StepStatus): StepStatus {
  if (override) return override;
  if (index < current)  return "complete";
  if (index === current) return "current";
  return "upcoming";
}

// ─── Step indicator ───────────────────────────────────────────────────────────

const indicatorSize = { sm: "w-6 h-6 text-xs", md: "w-8 h-8 text-sm", lg: "w-10 h-10 text-base" };
const iconSize      = { sm: "w-3 h-3",          md: "w-4 h-4",         lg: "w-5 h-5" };

function StepIndicator({
  status,
  index,
  icon,
  variant,
  size,
}: {
  status:  StepStatus;
  index:   number;
  icon?:   React.ReactNode;
  variant: "default" | "dots" | "numbered";
  size:    "sm" | "md" | "lg";
}) {
  if (variant === "dots") {
    return (
      <span
        className={cn(
          "rounded-full flex-shrink-0 transition-all duration-200",
          size === "sm" ? "w-2 h-2" : size === "md" ? "w-2.5 h-2.5" : "w-3 h-3",
          status === "complete" && "bg-interactive-primary",
          status === "current"  && "bg-interactive-primary ring-4 ring-interactive-primary/25",
          status === "upcoming" && "bg-border-strong",
          status === "error"    && "bg-status-danger",
        )}
      />
    );
  }

  return (
    <span
      className={cn(
        "rounded-full flex items-center justify-center flex-shrink-0 font-semibold transition-all duration-200",
        indicatorSize[size],
        status === "complete" && "bg-interactive-primary text-white",
        status === "current"  && "bg-interactive-primary text-white ring-4 ring-interactive-primary/25",
        status === "upcoming" && "bg-surface-muted text-content-muted border-2 border-border-default",
        status === "error"    && "bg-status-danger text-white",
      )}
    >
      {status === "complete" && !icon && <Check aria-hidden="true" className={iconSize[size]} />}
      {status === "error"    && !icon && <X    aria-hidden="true" className={iconSize[size]} />}
      {(status === "current" || status === "upcoming") && !icon && (
        <span>{index + 1}</span>
      )}
      {icon && <span className={cn("[&_svg]:w-full [&_svg]:h-full p-1.5")}>{icon}</span>}
    </span>
  );
}

// ─── Steps ────────────────────────────────────────────────────────────────────

export function Steps({
  steps,
  currentStep = 0,
  orientation = "horizontal",
  size = "md",
  variant = "default",
  className,
  onChange,
}: StepsProps) {
  const isHoriz = orientation === "horizontal";

  return (
    <nav aria-label="Progress" className={className}>
      <ol
        className={cn(
          isHoriz ? "flex items-start" : "flex flex-col",
        )}
      >
        {steps.map((step, i) => {
          const status  = resolveStatus(i, currentStep, step.status);
          const isLast  = i === steps.length - 1;
          const clickable = onChange && status !== "current";

          return (
            <li
              key={step.id}
              className={cn(
                isHoriz ? "flex items-start flex-1" : "flex",
                !isLast && (isHoriz ? "pr-4" : "pb-6"),
              )}
            >
              {/* Step with connector */}
              <div className={cn("flex", isHoriz ? "flex-col items-center w-full" : "flex-row gap-4")}>

                {/* Indicator row */}
                <div className={cn("flex items-center", isHoriz ? "w-full" : "flex-col")}>
                  <button
                    type="button"
                    onClick={() => clickable && onChange(i)}
                    disabled={!clickable}
                    className={cn(
                      "rounded-full transition-opacity",
                      clickable ? "cursor-pointer" : "cursor-default",
                    )}
                  >
                    <StepIndicator
                      status={status}
                      index={i}
                      icon={step.icon}
                      variant={variant}
                      size={size}
                    />
                  </button>

                  {/* Connector line */}
                  {!isLast && (
                    <div
                      aria-hidden="true"
                      className={cn(
                        "transition-colors duration-200",
                        isHoriz ? "flex-1 h-0.5 mx-2" : "w-0.5 h-full mt-2 ml-auto mr-auto",
                        // Calculate which side: complete or upcoming
                        i < currentStep
                          ? "bg-interactive-primary"
                          : "bg-border-default",
                      )}
                    />
                  )}
                </div>

                {/* Label */}
                <div
                  className={cn(
                    isHoriz ? "text-center mt-2" : "pt-1 pb-2 min-w-0 flex-1",
                    variant === "dots" && isHoriz && "hidden",
                  )}
                >
                  <p
                    className={cn(
                      "font-medium text-sm leading-tight",
                      status === "upcoming" ? "text-content-muted" : "text-content-primary",
                    )}
                  >
                    {step.label}
                  </p>
                  {step.description && (
                    <p className="mt-0.5 text-xs text-content-muted">{step.description}</p>
                  )}
                </div>
              </div>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
