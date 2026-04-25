import * as React from "react";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/cn";

// ─── Types ────────────────────────────────────────────────────────────────────

export type AccordionItem = {
  id:       string;
  trigger:  React.ReactNode;
  content:  React.ReactNode;
  disabled?: boolean;
  icon?:    React.ReactNode;
};

export type AccordionProps = {
  items:     AccordionItem[];
  type?:     "single" | "multiple";
  defaultOpen?: string | string[];
  value?:    string | string[];
  onChange?: (value: string | string[]) => void;
  variant?:  "default" | "bordered" | "flush";
  size?:     "sm" | "md" | "lg";
  className?: string;
};

// ─── Context ──────────────────────────────────────────────────────────────────

type AccordionCtx = {
  openIds: Set<string>;
  toggle:  (id: string) => void;
  variant: "default" | "bordered" | "flush";
  size:    "sm" | "md" | "lg";
};

const AccordionContext = React.createContext<AccordionCtx | null>(null);

// ─── Accordion ────────────────────────────────────────────────────────────────

const triggerSize = { sm: "py-2.5 text-sm", md: "py-3.5 text-sm", lg: "py-4 text-base" };
const contentSize = { sm: "text-sm", md: "text-sm", lg: "text-base" };

export function Accordion({
  items,
  type = "single",
  defaultOpen,
  value: controlledValue,
  onChange,
  variant = "default",
  size = "md",
  className,
}: AccordionProps) {
  const normalize = (v: string | string[] | undefined): Set<string> => {
    if (!v) return new Set();
    return new Set(Array.isArray(v) ? v : [v]);
  };

  const isControlled = controlledValue !== undefined;
  const [internal, setInternal] = React.useState<Set<string>>(normalize(defaultOpen));
  const openIds = isControlled ? normalize(controlledValue) : internal;

  const toggle = React.useCallback(
    (id: string) => {
      const next = new Set(openIds);
      if (next.has(id)) {
        next.delete(id);
      } else {
        if (type === "single") next.clear();
        next.add(id);
      }
      if (!isControlled) setInternal(next);
      const arr = [...next];
      onChange?.(type === "single" ? arr[0] ?? "" : arr);
    },
    [openIds, type, isControlled, onChange],
  );

  const wrapperClass = cn(
    variant === "default" && "divide-y divide-border-subtle rounded-panel border border-border-default overflow-hidden",
    variant === "bordered" && "space-y-2",
    variant === "flush" && "divide-y divide-border-subtle",
    className,
  );

  return (
    <AccordionContext.Provider value={{ openIds, toggle, variant, size }}>
      <div className={wrapperClass}>
        {items.map((item) => (
          <AccordionItemEl key={item.id} item={item} />
        ))}
      </div>
    </AccordionContext.Provider>
  );
}

// ─── AccordionItem ────────────────────────────────────────────────────────────

function AccordionItemEl({ item }: { item: AccordionItem }) {
  const ctx = React.useContext(AccordionContext)!;
  const { openIds, toggle, variant, size } = ctx;
  const isOpen = openIds.has(item.id);

  const itemClass = cn(
    variant === "bordered" && "rounded-panel border border-border-default overflow-hidden",
  );

  return (
    <div className={itemClass} data-state={isOpen ? "open" : "closed"}>
      <button
        type="button"
        id={`acc-trigger-${item.id}`}
        aria-expanded={isOpen}
        aria-controls={`acc-content-${item.id}`}
        disabled={item.disabled}
        onClick={() => !item.disabled && toggle(item.id)}
        className={cn(
          "w-full flex items-center gap-3 px-4 font-medium text-left",
          "text-content-primary bg-surface-base hover:bg-surface-muted",
          "transition-colors duration-fast focus-ring",
          item.disabled && "opacity-50 cursor-not-allowed",
          triggerSize[size],
        )}
      >
        {item.icon && <span className="[&_svg]:w-4 [&_svg]:h-4 text-content-muted">{item.icon}</span>}
        <span className="flex-1">{item.trigger}</span>
        <ChevronDown
          aria-hidden="true"
          className={cn(
            "w-4 h-4 text-content-muted flex-shrink-0 transition-transform duration-200",
            isOpen && "rotate-180",
          )}
        />
      </button>

      <div
        id={`acc-content-${item.id}`}
        role="region"
        aria-labelledby={`acc-trigger-${item.id}`}
        hidden={!isOpen}
        className={cn(
          "overflow-hidden bg-surface-base",
          isOpen && "animate-accordion-down",
        )}
      >
        <div
          className={cn(
            "px-4 pb-4 pt-1 text-content-secondary",
            contentSize[size],
          )}
        >
          {item.content}
        </div>
      </div>
    </div>
  );
}
