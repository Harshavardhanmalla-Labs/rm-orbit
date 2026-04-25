import { ChevronLeft, ChevronRight, MoreHorizontal } from "lucide-react";
import { cn } from "@/lib/cn";

// ─── Types ────────────────────────────────────────────────────────────────────

export type PaginationProps = {
  page:         number;
  totalPages:   number;
  onChange:     (page: number) => void;
  siblingCount?: number;
  showEdges?:   boolean;
  size?:        "sm" | "md" | "lg";
  className?:   string;
};

// ─── Helpers ──────────────────────────────────────────────────────────────────

function range(start: number, end: number): number[] {
  const len = end - start + 1;
  return Array.from({ length: len }, (_, i) => start + i);
}

function buildPages(page: number, total: number, sibling: number): (number | "dots")[] {
  const totalNums = sibling * 2 + 5;
  if (total <= totalNums) return range(1, total);

  const leftSib  = Math.max(page - sibling, 1);
  const rightSib = Math.min(page + sibling, total);
  const showLeft  = leftSib > 2;
  const showRight = rightSib < total - 1;

  if (!showLeft && showRight) {
    const left = range(1, 3 + sibling * 2);
    return [...left, "dots", total];
  }
  if (showLeft && !showRight) {
    const right = range(total - 2 - sibling * 2, total);
    return [1, "dots", ...right];
  }
  return [1, "dots", ...range(leftSib, rightSib), "dots", total];
}

// ─── Component ────────────────────────────────────────────────────────────────

const sizeClasses = {
  sm: "h-7 w-7 text-xs",
  md: "h-8 w-8 text-sm",
  lg: "h-9 w-9 text-sm",
};

const arrowClasses = {
  sm: "h-7 px-2 text-xs",
  md: "h-8 px-2.5 text-sm",
  lg: "h-9 px-3 text-sm",
};

export function Pagination({
  page,
  totalPages,
  onChange,
  siblingCount = 1,
  showEdges = true,
  size = "md",
  className,
}: PaginationProps) {
  const pages = buildPages(page, totalPages, siblingCount);

  const btn = (p: number, label?: string) => {
    const active = p === page;
    return (
      <button
        key={p}
        type="button"
        aria-label={label ?? `Page ${p}`}
        aria-current={active ? "page" : undefined}
        disabled={active}
        onClick={() => onChange(p)}
        className={cn(
          "inline-flex items-center justify-center rounded-button font-medium transition-colors duration-fast border",
          sizeClasses[size],
          active
            ? "bg-interactive-primary text-white border-interactive-primary"
            : "bg-surface-base text-content-primary border-border-default hover:bg-surface-muted",
        )}
      >
        {label ?? p}
      </button>
    );
  };

  const navBtn = (
    type: "prev" | "next",
    disabled: boolean,
    target: number,
  ) => (
    <button
      key={type}
      type="button"
      aria-label={type === "prev" ? "Previous page" : "Next page"}
      disabled={disabled}
      onClick={() => !disabled && onChange(target)}
      className={cn(
        "inline-flex items-center justify-center rounded-button font-medium transition-colors duration-fast border",
        arrowClasses[size],
        disabled
          ? "opacity-40 cursor-not-allowed bg-surface-base border-border-default text-content-muted"
          : "bg-surface-base text-content-primary border-border-default hover:bg-surface-muted",
      )}
    >
      {type === "prev" ? (
        <><ChevronLeft className="w-3.5 h-3.5" /><span className="sr-only">Previous</span></>
      ) : (
        <><span className="sr-only">Next</span><ChevronRight className="w-3.5 h-3.5" /></>
      )}
    </button>
  );

  return (
    <nav aria-label="Pagination" className={cn("flex items-center gap-1", className)}>
      {navBtn("prev", page === 1, page - 1)}

      {showEdges && pages.map((p, i) =>
        p === "dots" ? (
          <span
            key={`dots-${i}`}
            className={cn("inline-flex items-center justify-center text-content-muted", sizeClasses[size])}
          >
            <MoreHorizontal className="w-4 h-4" />
          </span>
        ) : btn(p),
      )}

      {navBtn("next", page === totalPages, page + 1)}
    </nav>
  );
}
