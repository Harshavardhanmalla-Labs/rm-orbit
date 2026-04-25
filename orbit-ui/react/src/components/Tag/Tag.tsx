import * as React from "react";
import { X } from "lucide-react";
import { cn } from "@/lib/cn";

// ─── Tag / Chip ───────────────────────────────────────────────────────────────

export type TagVariant = "default" | "primary" | "success" | "warning" | "danger" | "info";
export type TagSize    = "sm" | "md" | "lg";

export type TagProps = {
  variant?:    TagVariant;
  size?:       TagSize;
  removable?:  boolean;
  onRemove?:   () => void;
  icon?:       React.ReactNode;
  dot?:        boolean;
  children:    React.ReactNode;
  className?:  string;
  onClick?:    React.MouseEventHandler<HTMLSpanElement>;
};

const variantMap: Record<TagVariant, string> = {
  default: "bg-surface-muted text-content-secondary border-border-default",
  primary: "bg-interactive-primary/10 text-interactive-primary border-interactive-primary/30",
  success: "bg-status-success/10 text-status-success border-status-success/30",
  warning: "bg-status-warning/10 text-status-warning border-status-warning/30",
  danger:  "bg-status-danger/10 text-status-danger border-status-danger/30",
  info:    "bg-status-info/10 text-status-info border-status-info/30",
};

const dotColorMap: Record<TagVariant, string> = {
  default: "bg-content-muted",
  primary: "bg-interactive-primary",
  success: "bg-status-success",
  warning: "bg-status-warning",
  danger:  "bg-status-danger",
  info:    "bg-status-info",
};

const sizeMap: Record<TagSize, string> = {
  sm: "h-5 px-1.5 text-xs gap-1",
  md: "h-6 px-2 text-xs gap-1.5",
  lg: "h-7 px-2.5 text-sm gap-1.5",
};

export function Tag({
  variant = "default",
  size = "md",
  removable = false,
  onRemove,
  icon,
  dot = false,
  children,
  className,
  onClick,
}: TagProps) {
  return (
    <span
      onClick={onClick}
      className={cn(
        "inline-flex items-center rounded-full border font-medium select-none",
        variantMap[variant],
        sizeMap[size],
        onClick && "cursor-pointer",
        className,
      )}
    >
      {dot && (
        <span
          aria-hidden="true"
          className={cn("w-1.5 h-1.5 rounded-full flex-shrink-0", dotColorMap[variant])}
        />
      )}
      {icon && <span className="flex-shrink-0 [&_svg]:w-3 [&_svg]:h-3">{icon}</span>}
      {children}
      {removable && (
        <button
          type="button"
          onClick={(e) => { e.stopPropagation(); onRemove?.(); }}
          aria-label="Remove"
          className={cn(
            "flex-shrink-0 rounded-full p-0.5 -mr-0.5",
            "hover:bg-black/10 dark:hover:bg-white/20 transition-colors",
            "[&_svg]:w-2.5 [&_svg]:h-2.5",
          )}
        >
          <X />
        </button>
      )}
    </span>
  );
}

// ─── TagInput ─────────────────────────────────────────────────────────────────

export type TagInputProps = {
  value?:       string[];
  defaultValue?: string[];
  onChange?:    (tags: string[]) => void;
  placeholder?: string;
  variant?:     TagVariant;
  size?:        TagSize;
  disabled?:    boolean;
  maxTags?:     number;
  className?:   string;
};

export function TagInput({
  value: controlledValue,
  defaultValue = [],
  onChange,
  placeholder = "Add tag…",
  variant = "primary",
  size = "md",
  disabled = false,
  maxTags,
  className,
}: TagInputProps) {
  const isControlled = controlledValue !== undefined;
  const [internal, setInternal] = React.useState<string[]>(defaultValue);
  const tags = isControlled ? controlledValue! : internal;
  const [input, setInput] = React.useState("");

  const setTags = (next: string[]) => {
    if (!isControlled) setInternal(next);
    onChange?.(next);
  };

  const add = (raw: string) => {
    const tag = raw.trim();
    if (!tag || tags.includes(tag)) return;
    if (maxTags && tags.length >= maxTags) return;
    setTags([...tags, tag]);
    setInput("");
  };

  const remove = (i: number) => {
    setTags(tags.filter((_, idx) => idx !== i));
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      add(input);
    } else if (e.key === "Backspace" && !input && tags.length) {
      remove(tags.length - 1);
    }
  };

  return (
    <div
      className={cn(
        "flex flex-wrap gap-1.5 items-center min-h-[38px] px-3 py-1.5",
        "border border-border-default rounded-input bg-surface-base",
        "focus-within:border-interactive-primary focus-within:ring-2 focus-within:ring-interactive-primary/20",
        "transition-colors",
        disabled && "opacity-50 cursor-not-allowed",
        className,
      )}
    >
      {tags.map((tag, i) => (
        <Tag key={tag} variant={variant} size={size} removable={!disabled} onRemove={() => remove(i)}>
          {tag}
        </Tag>
      ))}
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={onKeyDown}
        onBlur={() => { if (input) add(input); }}
        disabled={disabled}
        placeholder={tags.length === 0 ? placeholder : ""}
        className={cn(
          "flex-1 min-w-[80px] outline-none bg-transparent text-sm",
          "text-content-primary placeholder:text-content-muted",
          disabled && "cursor-not-allowed",
        )}
      />
    </div>
  );
}
