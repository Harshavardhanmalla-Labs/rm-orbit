import * as React from "react";
import { cn } from "@/lib/cn";

type Placement = "top" | "bottom" | "left" | "right";

const placementClasses: Record<Placement, { tooltip: string; arrow: string }> = {
  top: {
    tooltip: "bottom-full left-1/2 -translate-x-1/2 mb-2",
    arrow:   "top-full left-1/2 -translate-x-1/2 border-t-neutral-800 dark:border-t-neutral-200 border-t-4 border-x-4 border-x-transparent border-b-0",
  },
  bottom: {
    tooltip: "top-full left-1/2 -translate-x-1/2 mt-2",
    arrow:   "bottom-full left-1/2 -translate-x-1/2 border-b-neutral-800 dark:border-b-neutral-200 border-b-4 border-x-4 border-x-transparent border-t-0",
  },
  left: {
    tooltip: "right-full top-1/2 -translate-y-1/2 mr-2",
    arrow:   "left-full top-1/2 -translate-y-1/2 border-l-neutral-800 dark:border-l-neutral-200 border-l-4 border-y-4 border-y-transparent border-r-0",
  },
  right: {
    tooltip: "left-full top-1/2 -translate-y-1/2 ml-2",
    arrow:   "right-full top-1/2 -translate-y-1/2 border-r-neutral-800 dark:border-r-neutral-200 border-r-4 border-y-4 border-y-transparent border-l-0",
  },
};

export type TooltipProps = {
  content:    React.ReactNode;
  placement?: Placement;
  delay?:     number;
  disabled?:  boolean;
  children:   React.ReactElement;
  className?: string;
};

export function Tooltip({
  content,
  placement = "top",
  delay     = 300,
  disabled  = false,
  children,
  className,
}: TooltipProps) {
  const [visible, setVisible] = React.useState(false);
  const timerRef = React.useRef<ReturnType<typeof setTimeout>>(undefined);
  const p = placementClasses[placement];

  const show = () => {
    if (disabled) return;
    timerRef.current = setTimeout(() => setVisible(true), delay);
  };
  const hide = () => {
    clearTimeout(timerRef.current);
    setVisible(false);
  };

  React.useEffect(() => () => clearTimeout(timerRef.current), []);

  return (
    <span
      className="relative inline-flex"
      onMouseEnter={show}
      onMouseLeave={hide}
      onFocus={show}
      onBlur={hide}
    >
      {children}
      {visible && content && (
        <span
          role="tooltip"
          className={cn(
            "absolute z-tooltip pointer-events-none",
            "px-2 py-1 rounded-tooltip text-xs font-medium whitespace-nowrap",
            "bg-neutral-800 text-white dark:bg-neutral-100 dark:text-neutral-900",
            "shadow-tooltip animate-scale-in",
            p.tooltip,
            className,
          )}
        >
          {content}
          <span className={cn("absolute w-0 h-0", p.arrow)} />
        </span>
      )}
    </span>
  );
}
