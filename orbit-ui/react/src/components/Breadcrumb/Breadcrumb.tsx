import * as React from "react";
import { ChevronRight, MoreHorizontal } from "lucide-react";
import { cn } from "@/lib/cn";

// ─── Types ────────────────────────────────────────────────────────────────────

export type BreadcrumbItem = {
  label:    React.ReactNode;
  href?:    string;
  icon?:    React.ReactNode;
  current?: boolean;
};

export type BreadcrumbProps = {
  items:        BreadcrumbItem[];
  separator?:   React.ReactNode;
  maxItems?:    number;
  className?:   string;
  renderLink?:  (item: BreadcrumbItem, children: React.ReactNode) => React.ReactNode;
};

// ─── Breadcrumb ───────────────────────────────────────────────────────────────

export function Breadcrumb({
  items,
  separator,
  maxItems,
  className,
  renderLink,
}: BreadcrumbProps) {
  const [expanded, setExpanded] = React.useState(false);

  const sep = separator ?? (
    <ChevronRight className="w-3.5 h-3.5 text-content-muted flex-shrink-0" aria-hidden="true" />
  );

  let visible = items;
  let collapsed = false;

  if (maxItems && items.length > maxItems && !expanded) {
    const keep = Math.max(maxItems - 1, 1);
    visible = [items[0], ...items.slice(items.length - keep + 1)];
    collapsed = true;
  }

  const defaultLink = (item: BreadcrumbItem, children: React.ReactNode) =>
    item.href ? (
      <a
        href={item.href}
        className="hover:text-content-primary transition-colors duration-fast"
        aria-current={item.current ? "page" : undefined}
      >
        {children}
      </a>
    ) : (
      <span aria-current={item.current ? "page" : undefined}>{children}</span>
    );

  const linkFn = renderLink ?? defaultLink;

  return (
    <nav aria-label="Breadcrumb" className={cn("flex items-center", className)}>
      <ol className="flex items-center gap-1.5 flex-wrap">
        {visible.map((item, i) => {
          const isFirst   = i === 0;
          const isLast    = i === visible.length - 1;
          const isEllipsis = collapsed && i === 1;

          const content = (
            <span className="inline-flex items-center gap-1">
              {item.icon && (
                <span className="[&_svg]:w-3.5 [&_svg]:h-3.5">{item.icon}</span>
              )}
              {item.label}
            </span>
          );

          return (
            <React.Fragment key={i}>
              {!isFirst && <li aria-hidden="true" className="flex items-center">{sep}</li>}
              {isEllipsis ? (
                <li>
                  <button
                    type="button"
                    onClick={() => setExpanded(true)}
                    aria-label="Show full path"
                    className={cn(
                      "inline-flex items-center px-1 rounded",
                      "text-content-muted hover:text-content-primary hover:bg-surface-muted",
                      "transition-colors duration-fast",
                    )}
                  >
                    <MoreHorizontal className="w-4 h-4" />
                  </button>
                </li>
              ) : (
                <li
                  className={cn(
                    "text-sm",
                    isLast || item.current
                      ? "text-content-primary font-medium"
                      : "text-content-muted",
                  )}
                >
                  {linkFn(item, content)}
                </li>
              )}
            </React.Fragment>
          );
        })}
      </ol>
    </nav>
  );
}
