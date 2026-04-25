import { useState, useRef, useEffect, useCallback } from 'react';
import { ChevronLeft, ChevronRight, Calendar, X } from 'lucide-react';
import { cn } from '@/lib/cn';

// ─── Types ────────────────────────────────────────────────────────────────────

export type DatePickerMode = 'single' | 'range';

export interface DateRange {
  from: Date | null;
  to: Date | null;
}

export interface DatePickerProps {
  /** 'single' (default) or 'range' */
  mode?: DatePickerMode;
  /** Controlled value for single mode */
  value?: Date | null;
  /** Controlled value for range mode */
  rangeValue?: DateRange;
  /** Called when a date is selected (single mode) */
  onChange?: (date: Date | null) => void;
  /** Called when a range is selected (range mode) */
  onRangeChange?: (range: DateRange) => void;
  /** Minimum selectable date */
  minDate?: Date;
  /** Maximum selectable date */
  maxDate?: Date;
  /** Display placeholder in the input trigger */
  placeholder?: string;
  /** Disable the entire picker */
  disabled?: boolean;
  /** Show a clear button when a value is selected */
  clearable?: boolean;
  /** Format function for display in the trigger */
  formatDate?: (date: Date) => string;
  className?: string;
  /** Locale for month/day names */
  locale?: string;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

const DAYS = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];

function defaultFormat(date: Date, locale = 'en-US'): string {
  return date.toLocaleDateString(locale, { month: 'short', day: 'numeric', year: 'numeric' });
}

function isSameDay(a: Date, b: Date) {
  return a.getFullYear() === b.getFullYear() &&
    a.getMonth() === b.getMonth() &&
    a.getDate() === b.getDate();
}

function isBefore(a: Date, b: Date) {
  return a.getTime() < b.getTime();
}

function isInRange(date: Date, from: Date | null, to: Date | null) {
  if (!from || !to) return false;
  const t = date.getTime();
  const f = Math.min(from.getTime(), to.getTime());
  const e = Math.max(from.getTime(), to.getTime());
  return t >= f && t <= e;
}

function startOfMonth(year: number, month: number): Date {
  return new Date(year, month, 1);
}

function getDaysInMonth(year: number, month: number): number {
  return new Date(year, month + 1, 0).getDate();
}

function buildCalendar(year: number, month: number): (Date | null)[] {
  const first = startOfMonth(year, month).getDay(); // 0=Sun
  const days = getDaysInMonth(year, month);
  const cells: (Date | null)[] = [];
  for (let i = 0; i < first; i++) cells.push(null);
  for (let d = 1; d <= days; d++) cells.push(new Date(year, month, d));
  return cells;
}

const MONTH_NAMES = ['January','February','March','April','May','June','July','August','September','October','November','December'];

// ─── Calendar Panel ──────────────────────────────────────────────────────────

interface CalendarProps {
  year: number;
  month: number;
  onYearMonthChange: (y: number, m: number) => void;
  selected?: Date | null;
  rangeFrom?: Date | null;
  rangeTo?: Date | null;
  hoverDate?: Date | null;
  onDayClick: (d: Date) => void;
  onDayHover?: (d: Date | null) => void;
  minDate?: Date;
  maxDate?: Date;
}

function CalendarPanel({
  year, month, onYearMonthChange,
  selected, rangeFrom, rangeTo, hoverDate,
  onDayClick, onDayHover, minDate, maxDate,
}: CalendarProps) {
  const cells = buildCalendar(year, month);

  const prevMonth = () => {
    if (month === 0) onYearMonthChange(year - 1, 11);
    else onYearMonthChange(year, month - 1);
  };
  const nextMonth = () => {
    if (month === 11) onYearMonthChange(year + 1, 0);
    else onYearMonthChange(year, month + 1);
  };

  return (
    <div className="w-[280px] p-3 select-none">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <button
          onClick={prevMonth}
          className="p-1.5 rounded-md hover:bg-surface-muted text-content-secondary hover:text-content-primary transition-colors"
          aria-label="Previous month"
        >
          <ChevronLeft size={16} />
        </button>
        <span className="text-sm font-semibold text-content-primary">
          {MONTH_NAMES[month]} {year}
        </span>
        <button
          onClick={nextMonth}
          className="p-1.5 rounded-md hover:bg-surface-muted text-content-secondary hover:text-content-primary transition-colors"
          aria-label="Next month"
        >
          <ChevronRight size={16} />
        </button>
      </div>

      {/* Day-of-week headers */}
      <div className="grid grid-cols-7 mb-1">
        {DAYS.map(d => (
          <div key={d} className="h-8 flex items-center justify-center text-xs font-medium text-content-muted">{d}</div>
        ))}
      </div>

      {/* Cells */}
      <div className="grid grid-cols-7 gap-y-0.5">
        {cells.map((date, i) => {
          if (!date) return <div key={`e-${i}`} />;

          const isSelected = selected ? isSameDay(date, selected) : false;
          const isFrom = rangeFrom ? isSameDay(date, rangeFrom) : false;
          const isTo = rangeTo ? isSameDay(date, rangeTo) : false;
          const isEndpoint = isFrom || isTo;
          const today = isSameDay(date, new Date());
          const disabled =
            (minDate ? isBefore(date, minDate) && !isSameDay(date, minDate) : false) ||
            (maxDate ? isBefore(maxDate, date) && !isSameDay(date, maxDate) : false);

          // Range highlight: use hoverDate as temporary "to" if rangeTo not set yet
          const effectiveTo = rangeTo ?? hoverDate ?? null;
          const inRange = !isEndpoint && isInRange(date, rangeFrom ?? null, effectiveTo);

          return (
            <button
              key={date.toISOString()}
              disabled={disabled}
              onClick={() => !disabled && onDayClick(date)}
              onMouseEnter={() => onDayHover?.(date)}
              onMouseLeave={() => onDayHover?.(null)}
              className={cn(
                'h-8 w-full flex items-center justify-center text-xs rounded-md transition-colors',
                disabled && 'opacity-30 cursor-not-allowed',
                !disabled && 'hover:bg-surface-muted cursor-pointer',
                (isSelected || isEndpoint) && 'bg-primary text-white hover:bg-primary/90 font-semibold',
                inRange && !isEndpoint && 'bg-primary/10 text-primary rounded-none',
                today && !isSelected && !isEndpoint && 'font-bold text-primary',
              )}
            >
              {date.getDate()}
            </button>
          );
        })}
      </div>
    </div>
  );
}

// ─── DatePicker ──────────────────────────────────────────────────────────────

export function DatePicker({
  mode = 'single',
  value,
  rangeValue,
  onChange,
  onRangeChange,
  minDate,
  maxDate,
  placeholder = 'Select date...',
  disabled = false,
  clearable = true,
  formatDate,
  className,
  locale = 'en-US',
}: DatePickerProps) {
  const today = new Date();
  const [open, setOpen] = useState(false);
  const [year, setYear] = useState(
    (mode === 'range' ? rangeValue?.from : value)?.getFullYear() ?? today.getFullYear()
  );
  const [month, setMonth] = useState(
    (mode === 'range' ? rangeValue?.from : value)?.getMonth() ?? today.getMonth()
  );
  const [hoverDate, setHoverDate] = useState<Date | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Close on outside click
  useEffect(() => {
    if (!open) return;
    const handler = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, [open]);

  // Escape key
  useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false); };
    document.addEventListener('keydown', handler);
    return () => document.removeEventListener('keydown', handler);
  }, [open]);

  const handleDayClick = useCallback((date: Date) => {
    if (mode === 'single') {
      onChange?.(date);
      setOpen(false);
    } else {
      const current = rangeValue ?? { from: null, to: null };
      if (!current.from || (current.from && current.to)) {
        // Start new range
        onRangeChange?.({ from: date, to: null });
      } else {
        // Complete range
        const from = current.from;
        if (isSameDay(date, from)) {
          onRangeChange?.({ from: date, to: date });
        } else if (isBefore(date, from)) {
          onRangeChange?.({ from: date, to: from });
        } else {
          onRangeChange?.({ from, to: date });
        }
        setOpen(false);
      }
    }
  }, [mode, onChange, onRangeChange, rangeValue]);

  const fmt = formatDate ?? ((d: Date) => defaultFormat(d, locale));

  let displayValue = '';
  if (mode === 'single' && value) {
    displayValue = fmt(value);
  } else if (mode === 'range' && rangeValue) {
    const { from, to } = rangeValue;
    if (from && to) displayValue = `${fmt(from)} – ${fmt(to)}`;
    else if (from) displayValue = `${fmt(from)} – ...`;
  }

  const handleClear = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (mode === 'single') onChange?.(null);
    else onRangeChange?.({ from: null, to: null });
  };

  return (
    <div ref={containerRef} className={cn('relative inline-block', className)}>
      {/* Trigger */}
      <button
        type="button"
        disabled={disabled}
        onClick={() => setOpen(p => !p)}
        className={cn(
          'flex h-9 min-w-[200px] items-center justify-between gap-2 rounded-lg border border-border-default bg-surface-base px-3 text-sm transition-colors',
          'hover:border-border-strong focus:outline-none focus:ring-2 focus:ring-primary/40',
          disabled && 'opacity-50 cursor-not-allowed',
          open && 'border-primary ring-2 ring-primary/30',
          displayValue ? 'text-content-primary' : 'text-content-muted',
        )}
        aria-haspopup="dialog"
        aria-expanded={open}
      >
        <span className="flex items-center gap-2 truncate">
          <Calendar size={15} className="text-content-muted shrink-0" />
          <span className="truncate">{displayValue || placeholder}</span>
        </span>
        {clearable && displayValue && (
          <span
            role="button"
            aria-label="Clear date"
            onClick={handleClear}
            className="shrink-0 text-content-muted hover:text-content-primary transition-colors"
          >
            <X size={14} />
          </span>
        )}
      </button>

      {/* Calendar popup */}
      {open && (
        <div
          role="dialog"
          aria-label="Date picker calendar"
          className={cn(
            'absolute z-50 mt-1 rounded-xl border border-border-default bg-surface-base shadow-lg',
            'animate-in fade-in-0 zoom-in-95',
            mode === 'range' ? 'flex' : '',
          )}
        >
          <CalendarPanel
            year={year}
            month={month}
            onYearMonthChange={(y, m) => { setYear(y); setMonth(m); }}
            selected={mode === 'single' ? value ?? null : undefined}
            rangeFrom={mode === 'range' ? rangeValue?.from ?? null : undefined}
            rangeTo={mode === 'range' ? rangeValue?.to ?? null : undefined}
            hoverDate={mode === 'range' ? hoverDate : undefined}
            onDayClick={handleDayClick}
            onDayHover={mode === 'range' ? setHoverDate : undefined}
            minDate={minDate}
            maxDate={maxDate}
          />
          {/* Second calendar for range mode */}
          {mode === 'range' && (
            <div className="border-l border-border-subtle">
              <CalendarPanel
                year={month === 11 ? year + 1 : year}
                month={month === 11 ? 0 : month + 1}
                onYearMonthChange={(y, m) => { setYear(m === 0 ? y - 1 : y); setMonth(m === 0 ? 11 : m - 1); }}
                rangeFrom={rangeValue?.from ?? null}
                rangeTo={rangeValue?.to ?? null}
                hoverDate={hoverDate}
                onDayClick={handleDayClick}
                onDayHover={setHoverDate}
                minDate={minDate}
                maxDate={maxDate}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
