import * as React from "react";
import { ChevronUp, ChevronDown, ChevronsUpDown } from "lucide-react";
import { cn } from "@/lib/cn";

// ─── Types ────────────────────────────────────────────────────────────────────

export type SortDir = "asc" | "desc" | null;

export type Column<T> = {
  key:         string;
  header:      React.ReactNode;
  cell?:       (row: T, index: number) => React.ReactNode;
  accessor?:   keyof T;
  sortable?:   boolean;
  width?:      string;
  align?:      "left" | "center" | "right";
  className?:  string;
  headerClassName?: string;
};

export type TableProps<T> = {
  columns:       Column<T>[];
  data:          T[];
  keyExtractor:  (row: T, index: number) => string | number;
  sortKey?:      string;
  sortDir?:      SortDir;
  onSort?:       (key: string, dir: SortDir) => void;
  stickyHeader?: boolean;
  striped?:      boolean;
  compact?:      boolean;
  bordered?:     boolean;
  hoverable?:    boolean;
  onRowClick?:   (row: T, index: number) => void;
  loading?:      boolean;
  empty?:        React.ReactNode;
  footer?:       React.ReactNode;
  className?:    string;
  tableClassName?: string;
};

// ─── Alignment ────────────────────────────────────────────────────────────────

const alignClass: Record<"left" | "center" | "right", string> = {
  left:   "text-left",
  center: "text-center",
  right:  "text-right",
};

// ─── Sort icon ────────────────────────────────────────────────────────────────

function SortIcon({ dir }: { dir: SortDir | undefined }) {
  if (dir === "asc")  return <ChevronUp   className="w-3.5 h-3.5 flex-shrink-0" />;
  if (dir === "desc") return <ChevronDown  className="w-3.5 h-3.5 flex-shrink-0" />;
  return <ChevronsUpDown className="w-3.5 h-3.5 flex-shrink-0 opacity-40" />;
}

// ─── Table ────────────────────────────────────────────────────────────────────

export function Table<T>({
  columns,
  data,
  keyExtractor,
  sortKey,
  sortDir,
  onSort,
  stickyHeader = false,
  striped = false,
  compact = false,
  bordered = false,
  hoverable = true,
  onRowClick,
  loading = false,
  empty,
  footer,
  className,
  tableClassName,
}: TableProps<T>) {
  const handleSort = (col: Column<T>) => {
    if (!col.sortable || !onSort) return;
    if (sortKey !== col.key) { onSort(col.key, "asc"); return; }
    if (sortDir === "asc")   { onSort(col.key, "desc"); return; }
    onSort(col.key, null);
  };

  const cellPad = compact ? "px-3 py-1.5" : "px-4 py-3";
  const thPad   = compact ? "px-3 py-2"   : "px-4 py-3";

  return (
    <div
      className={cn(
        "w-full overflow-auto rounded-panel border border-border-default",
        className,
      )}
    >
      <table
        className={cn(
          "w-full border-collapse text-sm",
          tableClassName,
        )}
      >
        <thead
          className={cn(
            "bg-surface-muted",
            stickyHeader && "sticky top-0 z-10",
          )}
        >
          <tr>
            {columns.map((col) => {
              const isActive = sortKey === col.key;
              const dir = isActive ? sortDir : null;
              return (
                <th
                  key={col.key}
                  scope="col"
                  style={col.width ? { width: col.width } : undefined}
                  className={cn(
                    thPad,
                    "text-xs font-semibold text-content-muted uppercase tracking-wider",
                    "border-b border-border-default",
                    bordered && "border-r last:border-r-0",
                    alignClass[col.align ?? "left"],
                    col.sortable && "cursor-pointer select-none hover:text-content-primary",
                    col.headerClassName,
                  )}
                  onClick={() => handleSort(col)}
                  aria-sort={
                    col.sortable && isActive
                      ? dir === "asc" ? "ascending" : "descending"
                      : undefined
                  }
                >
                  <span className="inline-flex items-center gap-1">
                    {col.header}
                    {col.sortable && <SortIcon dir={dir} />}
                  </span>
                </th>
              );
            })}
          </tr>
        </thead>

        <tbody className="divide-y divide-border-subtle">
          {loading ? (
            <tr>
              <td colSpan={columns.length} className="py-12 text-center text-content-muted">
                <span className="inline-flex items-center gap-2">
                  <span className="w-4 h-4 rounded-full border-2 border-interactive-primary border-t-transparent animate-spin" />
                  Loading…
                </span>
              </td>
            </tr>
          ) : data.length === 0 ? (
            <tr>
              <td colSpan={columns.length} className="py-12 text-center text-content-muted">
                {empty ?? "No results found."}
              </td>
            </tr>
          ) : (
            data.map((row, rowIndex) => (
              <tr
                key={keyExtractor(row, rowIndex)}
                onClick={() => onRowClick?.(row, rowIndex)}
                className={cn(
                  "transition-colors duration-fast",
                  striped && rowIndex % 2 === 1 && "bg-surface-muted/40",
                  hoverable && "hover:bg-surface-muted",
                  onRowClick && "cursor-pointer",
                )}
              >
                {columns.map((col) => {
                  const value = col.accessor ? (row[col.accessor] as React.ReactNode) : null;
                  const cell  = col.cell ? col.cell(row, rowIndex) : value;
                  return (
                    <td
                      key={col.key}
                      className={cn(
                        cellPad,
                        "text-content-primary",
                        bordered && "border-r last:border-r-0 border-border-subtle",
                        alignClass[col.align ?? "left"],
                        col.className,
                      )}
                    >
                      {cell}
                    </td>
                  );
                })}
              </tr>
            ))
          )}
        </tbody>

        {footer && (
          <tfoot className="bg-surface-muted border-t border-border-default">
            {footer}
          </tfoot>
        )}
      </table>
    </div>
  );
}
