import * as React from "react";
import { Search, ChevronRight, Command } from "lucide-react";
import { cn } from "@/lib/cn";

// ─── Types ────────────────────────────────────────────────────────────────────

export type CommandItem = {
  id:       string;
  label:    string;
  description?: string;
  icon?:    React.ReactNode;
  shortcut?: string[];
  onSelect: () => void;
  group?:   string;
  keywords?: string[];
  disabled?: boolean;
};

export type CommandPaletteProps = {
  open:        boolean;
  onClose:     () => void;
  items:       CommandItem[];
  placeholder?: string;
  emptyText?:  string;
  className?:  string;
};

// ─── Helpers ──────────────────────────────────────────────────────────────────

function normalize(s: string) {
  return s.toLowerCase().trim();
}

function scoreMatch(item: CommandItem, query: string): number {
  const q = normalize(query);
  if (!q) return 1;
  const label = normalize(item.label);
  const desc  = normalize(item.description ?? "");
  const kws   = (item.keywords ?? []).join(" ").toLowerCase();
  if (label.startsWith(q))       return 3;
  if (label.includes(q))         return 2;
  if (desc.includes(q) || kws.includes(q)) return 1;
  return 0;
}

function filterItems(items: CommandItem[], query: string): CommandItem[] {
  return items
    .map((item) => ({ item, score: scoreMatch(item, query) }))
    .filter(({ score }) => score > 0)
    .sort((a, b) => b.score - a.score)
    .map(({ item }) => item);
}

function groupItems(items: CommandItem[]): [string, CommandItem[]][] {
  const groups = new Map<string, CommandItem[]>();
  items.forEach((item) => {
    const g = item.group ?? "";
    if (!groups.has(g)) groups.set(g, []);
    groups.get(g)!.push(item);
  });
  return [...groups.entries()];
}

// ─── CommandPalette ───────────────────────────────────────────────────────────

export function CommandPalette({
  open,
  onClose,
  items,
  placeholder = "Search commands…",
  emptyText = "No results found.",
  className,
}: CommandPaletteProps) {
  const [query,   setQuery]   = React.useState("");
  const [active,  setActive]  = React.useState(0);
  const inputRef              = React.useRef<HTMLInputElement>(null);
  const listRef               = React.useRef<HTMLUListElement>(null);

  const filtered = React.useMemo(() => filterItems(items, query), [items, query]);
  const grouped  = React.useMemo(() => groupItems(filtered), [filtered]);

  // Reset on open/close
  React.useEffect(() => {
    if (open) {
      setQuery("");
      setActive(0);
      setTimeout(() => inputRef.current?.focus(), 10);
    }
  }, [open]);

  // Keep active in range
  React.useEffect(() => {
    setActive((a) => Math.min(a, Math.max(filtered.length - 1, 0)));
  }, [filtered]);

  const selectItem = (item: CommandItem) => {
    if (item.disabled) return;
    item.onSelect();
    onClose();
  };

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive((a) => Math.min(a + 1, filtered.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive((a) => Math.max(a - 1, 0));
    } else if (e.key === "Enter") {
      e.preventDefault();
      const item = filtered[active];
      if (item) selectItem(item);
    } else if (e.key === "Escape") {
      onClose();
    }
  };

  // Scroll active item into view
  React.useEffect(() => {
    const el = listRef.current?.querySelector(`[data-active="true"]`);
    el?.scrollIntoView({ block: "nearest" });
  }, [active]);

  if (!open) return null;

  let flatIndex = 0;

  return (
    <>
      {/* Backdrop */}
      <div
        aria-hidden="true"
        onClick={onClose}
        className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm"
      />

      {/* Panel */}
      <div
        role="dialog"
        aria-label="Command palette"
        aria-modal="true"
        onKeyDown={onKeyDown}
        className={cn(
          "fixed z-50 left-1/2 top-[15vh] -translate-x-1/2",
          "w-full max-w-xl",
          "rounded-2xl border border-border-default bg-surface-base shadow-2xl",
          "overflow-hidden",
          className,
        )}
      >
        {/* Search input */}
        <div className="flex items-center gap-3 px-4 py-3 border-b border-border-subtle">
          <Search className="w-4 h-4 text-content-muted flex-shrink-0" aria-hidden="true" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => { setQuery(e.target.value); setActive(0); }}
            placeholder={placeholder}
            aria-label={placeholder}
            className={cn(
              "flex-1 bg-transparent text-sm text-content-primary placeholder:text-content-muted",
              "outline-none",
            )}
          />
          <kbd className="hidden sm:inline-flex items-center gap-1 px-1.5 py-0.5 rounded text-xs font-medium bg-surface-muted text-content-muted border border-border-default">
            <Command className="w-3 h-3" />K
          </kbd>
        </div>

        {/* Results */}
        <ul
          ref={listRef}
          role="listbox"
          aria-label="Commands"
          className="max-h-80 overflow-y-auto py-2"
        >
          {filtered.length === 0 ? (
            <li className="px-4 py-8 text-center text-sm text-content-muted">{emptyText}</li>
          ) : (
            grouped.map(([groupLabel, groupItems]) => (
              <li key={groupLabel} role="presentation">
                {groupLabel && (
                  <p className="px-4 pt-2 pb-1 text-xs font-semibold uppercase tracking-wider text-content-muted">
                    {groupLabel}
                  </p>
                )}
                <ul role="group" aria-label={groupLabel || "Results"}>
                  {groupItems.map((item) => {
                    const idx      = flatIndex++;
                    const isActive = idx === active;
                    return (
                      <li
                        key={item.id}
                        role="option"
                        aria-selected={isActive}
                        data-active={isActive}
                        onClick={() => selectItem(item)}
                        className={cn(
                          "flex items-center gap-3 mx-2 px-3 py-2.5 rounded-lg cursor-pointer",
                          "transition-colors duration-fast",
                          isActive
                            ? "bg-interactive-primary text-white"
                            : "text-content-primary hover:bg-surface-muted",
                          item.disabled && "opacity-40 cursor-not-allowed",
                        )}
                      >
                        {item.icon && (
                          <span
                            className={cn(
                              "[&_svg]:w-4 [&_svg]:h-4 flex-shrink-0",
                              isActive ? "text-white" : "text-content-muted",
                            )}
                          >
                            {item.icon}
                          </span>
                        )}
                        <span className="flex-1 min-w-0">
                          <span className="block text-sm font-medium truncate">{item.label}</span>
                          {item.description && (
                            <span
                              className={cn(
                                "block text-xs truncate",
                                isActive ? "text-white/70" : "text-content-muted",
                              )}
                            >
                              {item.description}
                            </span>
                          )}
                        </span>
                        {item.shortcut && (
                          <span className="flex items-center gap-0.5">
                            {item.shortcut.map((k, ki) => (
                              <kbd
                                key={ki}
                                className={cn(
                                  "px-1.5 py-0.5 rounded text-xs font-medium border",
                                  isActive
                                    ? "bg-white/20 border-white/30 text-white"
                                    : "bg-surface-muted border-border-default text-content-muted",
                                )}
                              >
                                {k}
                              </kbd>
                            ))}
                          </span>
                        )}
                        {!item.shortcut && isActive && (
                          <ChevronRight className="w-4 h-4 text-white/70 flex-shrink-0" aria-hidden="true" />
                        )}
                      </li>
                    );
                  })}
                </ul>
              </li>
            ))
          )}
        </ul>

        {/* Footer hint */}
        <div className="flex items-center justify-end gap-4 px-4 py-2 border-t border-border-subtle bg-surface-muted">
          <span className="text-xs text-content-muted flex items-center gap-1">
            <kbd className="px-1 py-0.5 rounded text-xs bg-surface-base border border-border-default">↑↓</kbd>
            navigate
          </span>
          <span className="text-xs text-content-muted flex items-center gap-1">
            <kbd className="px-1 py-0.5 rounded text-xs bg-surface-base border border-border-default">↵</kbd>
            select
          </span>
          <span className="text-xs text-content-muted flex items-center gap-1">
            <kbd className="px-1 py-0.5 rounded text-xs bg-surface-base border border-border-default">Esc</kbd>
            close
          </span>
        </div>
      </div>
    </>
  );
}

// ─── useCommandPalette hook ───────────────────────────────────────────────────

export function useCommandPalette(hotkey?: string) {
  const [open, setOpen] = React.useState(false);

  React.useEffect(() => {
    const onKeyDown = (e: KeyboardEvent) => {
      if (!hotkey) {
        // Default: Cmd+K / Ctrl+K
        if ((e.metaKey || e.ctrlKey) && e.key === "k") {
          e.preventDefault();
          setOpen((v) => !v);
        }
        return;
      }
      // Custom hotkey like "ctrl+space"
      const parts = hotkey.toLowerCase().split("+");
      const key   = parts[parts.length - 1];
      const ctrl  = parts.includes("ctrl") || parts.includes("cmd");
      const shift = parts.includes("shift");
      const alt   = parts.includes("alt");
      if (
        e.key.toLowerCase() === key &&
        (!ctrl  || (e.ctrlKey || e.metaKey)) &&
        (!shift || e.shiftKey) &&
        (!alt   || e.altKey)
      ) {
        e.preventDefault();
        setOpen((v) => !v);
      }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [hotkey]);

  return { open, setOpen, toggle: () => setOpen((v) => !v) };
}
