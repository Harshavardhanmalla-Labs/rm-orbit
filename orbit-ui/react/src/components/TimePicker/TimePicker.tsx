import { useState, useRef, useEffect, useCallback, useId } from 'react';
import { Clock, X, ChevronUp, ChevronDown } from 'lucide-react';
import { cn } from '@/lib/cn';

// ─── Types ────────────────────────────────────────────────────────────────────

export interface TimeValue {
  hours: number;   // 0-23
  minutes: number; // 0-59
  seconds?: number; // 0-59
}

export interface TimePickerProps {
  value?: TimeValue | null;
  onChange?: (value: TimeValue | null) => void;
  /** 12 or 24 hour format */
  format?: 12 | 24;
  /** Show seconds column */
  showSeconds?: boolean;
  /** Minute step */
  minuteStep?: number;
  /** Second step */
  secondStep?: number;
  placeholder?: string;
  disabled?: boolean;
  clearable?: boolean;
  className?: string;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function pad(n: number) { return String(n).padStart(2, '0'); }

function formatTime(v: TimeValue, format: 12 | 24, showSeconds: boolean): string {
  const h24 = v.hours;
  const mm = pad(v.minutes);
  const ss = showSeconds && v.seconds !== undefined ? `:${pad(v.seconds)}` : '';

  if (format === 24) return `${pad(h24)}:${mm}${ss}`;

  const ampm = h24 >= 12 ? 'PM' : 'AM';
  const h12 = h24 % 12 === 0 ? 12 : h24 % 12;
  return `${pad(h12)}:${mm}${ss} ${ampm}`;
}

// ─── Column ──────────────────────────────────────────────────────────────────

interface ColumnProps {
  items: number[];
  selected: number;
  onSelect: (v: number) => void;
  format?: (v: number) => string;
  label: string;
}

function ScrollColumn({ items, selected, onSelect, format = pad, label }: ColumnProps) {
  const listRef = useRef<HTMLDivElement>(null);

  // Scroll selected item into center on mount and selection change
  useEffect(() => {
    const list = listRef.current;
    if (!list) return;
    const idx = items.indexOf(selected);
    if (idx < 0) return;
    const itemH = 36;
    list.scrollTo({ top: idx * itemH - (list.clientHeight / 2) + itemH / 2, behavior: 'smooth' });
  }, [selected, items]);

  const inc = () => {
    const idx = items.indexOf(selected);
    onSelect(items[(idx + 1) % items.length]);
  };
  const dec = () => {
    const idx = items.indexOf(selected);
    onSelect(items[(idx - 1 + items.length) % items.length]);
  };

  return (
    <div className="flex flex-col items-center">
      <span className="text-[10px] font-semibold uppercase tracking-wider text-content-muted mb-1">{label}</span>
      <button
        onClick={dec}
        className="p-1 rounded text-content-muted hover:text-content-primary hover:bg-surface-muted transition-colors"
        aria-label={`Decrease ${label}`}
      >
        <ChevronUp size={14} />
      </button>
      <div
        ref={listRef}
        className="h-[144px] overflow-y-auto overflow-x-hidden scrollbar-none"
        style={{ scrollbarWidth: 'none' }}
      >
        {items.map(v => (
          <button
            key={v}
            onClick={() => onSelect(v)}
            className={cn(
              'flex h-9 w-12 items-center justify-center rounded-md text-sm font-medium transition-colors',
              v === selected
                ? 'bg-primary text-white'
                : 'text-content-secondary hover:bg-surface-muted hover:text-content-primary',
            )}
          >
            {format(v)}
          </button>
        ))}
      </div>
      <button
        onClick={inc}
        className="p-1 rounded text-content-muted hover:text-content-primary hover:bg-surface-muted transition-colors"
        aria-label={`Increase ${label}`}
      >
        <ChevronDown size={14} />
      </button>
    </div>
  );
}

// ─── TimePicker ──────────────────────────────────────────────────────────────

export function TimePicker({
  value,
  onChange,
  format = 24,
  showSeconds = false,
  minuteStep = 1,
  secondStep = 1,
  placeholder = 'Select time...',
  disabled = false,
  clearable = true,
  className,
}: TimePickerProps) {
  const id = useId();
  const [open, setOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  // Internal state for when no controlled value
  const [internal, setInternal] = useState<TimeValue>({ hours: 12, minutes: 0, seconds: 0 });
  const current = value !== undefined ? (value ?? internal) : internal;
  const [period, setPeriod] = useState<'AM' | 'PM'>(current.hours >= 12 ? 'PM' : 'AM');

  const hours24 = Array.from({ length: 24 }, (_, i) => i);
  const hours12 = Array.from({ length: 12 }, (_, i) => i + 1); // 1-12
  const minutes = Array.from({ length: Math.ceil(60 / minuteStep) }, (_, i) => i * minuteStep);
  const seconds = Array.from({ length: Math.ceil(60 / secondStep) }, (_, i) => i * secondStep);

  const notify = useCallback((v: TimeValue) => {
    setInternal(v);
    onChange?.(v);
  }, [onChange]);

  const setHours = (h: number) => {
    let h24 = h;
    if (format === 12) {
      h24 = period === 'PM' ? (h === 12 ? 12 : h + 12) : (h === 12 ? 0 : h);
    }
    notify({ ...current, hours: h24 });
  };

  const setMinutes = (m: number) => notify({ ...current, minutes: m });
  const setSeconds = (s: number) => notify({ ...current, minutes: current.minutes, seconds: s });

  const togglePeriod = () => {
    const next = period === 'AM' ? 'PM' : 'AM';
    setPeriod(next);
    const h12 = current.hours % 12 === 0 ? 12 : current.hours % 12;
    const h24 = next === 'PM' ? (h12 === 12 ? 12 : h12 + 12) : (h12 === 12 ? 0 : h12);
    notify({ ...current, hours: h24 });
  };

  // Displayed hours for 12h format
  const displayHour = format === 12
    ? (current.hours % 12 === 0 ? 12 : current.hours % 12)
    : current.hours;

  // Close on outside click / Escape
  useEffect(() => {
    if (!open) return;
    const handler = (e: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) setOpen(false);
    };
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false); };
    document.addEventListener('mousedown', handler);
    document.addEventListener('keydown', onKey);
    return () => {
      document.removeEventListener('mousedown', handler);
      document.removeEventListener('keydown', onKey);
    };
  }, [open]);

  const displayValue = value !== undefined && value !== null
    ? formatTime(value, format, showSeconds)
    : open || internal.hours !== 12 || internal.minutes !== 0
    ? formatTime(current, format, showSeconds)
    : '';

  const handleClear = (e: React.MouseEvent) => {
    e.stopPropagation();
    onChange?.(null);
    setInternal({ hours: 12, minutes: 0, seconds: 0 });
  };

  return (
    <div ref={containerRef} className={cn('relative inline-block', className)}>
      <button
        type="button"
        id={id}
        disabled={disabled}
        onClick={() => setOpen(p => !p)}
        className={cn(
          'flex h-9 min-w-[160px] items-center justify-between gap-2 rounded-lg border border-border-default bg-surface-base px-3 text-sm transition-colors',
          'hover:border-border-strong focus:outline-none focus:ring-2 focus:ring-primary/40',
          disabled && 'opacity-50 cursor-not-allowed',
          open && 'border-primary ring-2 ring-primary/30',
          displayValue ? 'text-content-primary' : 'text-content-muted',
        )}
        aria-haspopup="dialog"
        aria-expanded={open}
      >
        <span className="flex items-center gap-2">
          <Clock size={15} className="text-content-muted shrink-0" />
          <span>{displayValue || placeholder}</span>
        </span>
        {clearable && displayValue && (
          <span
            role="button"
            aria-label="Clear time"
            onClick={handleClear}
            className="shrink-0 text-content-muted hover:text-content-primary"
          >
            <X size={14} />
          </span>
        )}
      </button>

      {open && (
        <div
          role="dialog"
          aria-label="Time picker"
          className="absolute z-50 mt-1 rounded-xl border border-border-default bg-surface-base p-4 shadow-lg"
        >
          <div className="flex items-start gap-3">
            {/* Hours */}
            <ScrollColumn
              items={format === 12 ? hours12 : hours24}
              selected={displayHour}
              onSelect={setHours}
              label="HH"
            />
            <div className="flex h-full items-center pt-8 text-lg font-bold text-content-muted">:</div>
            {/* Minutes */}
            <ScrollColumn
              items={minutes}
              selected={current.minutes}
              onSelect={setMinutes}
              label="MM"
            />
            {/* Seconds */}
            {showSeconds && (
              <>
                <div className="flex h-full items-center pt-8 text-lg font-bold text-content-muted">:</div>
                <ScrollColumn
                  items={seconds}
                  selected={current.seconds ?? 0}
                  onSelect={setSeconds}
                  label="SS"
                />
              </>
            )}
            {/* AM/PM */}
            {format === 12 && (
              <div className="flex flex-col items-center gap-1 pt-6 ml-1">
                <span className="text-[10px] font-semibold uppercase tracking-wider text-content-muted mb-1">·</span>
                <button
                  onClick={() => setPeriod('AM') !== undefined && period !== 'AM' && togglePeriod()}
                  className={cn(
                    'w-12 rounded-md py-1.5 text-xs font-semibold transition-colors',
                    period === 'AM' ? 'bg-primary text-white' : 'text-content-secondary hover:bg-surface-muted',
                  )}
                >
                  AM
                </button>
                <button
                  onClick={() => period !== 'PM' && togglePeriod()}
                  className={cn(
                    'w-12 rounded-md py-1.5 text-xs font-semibold transition-colors',
                    period === 'PM' ? 'bg-primary text-white' : 'text-content-secondary hover:bg-surface-muted',
                  )}
                >
                  PM
                </button>
              </div>
            )}
          </div>
          {/* Apply button */}
          <div className="mt-3 flex justify-end">
            <button
              onClick={() => setOpen(false)}
              className="rounded-lg bg-primary px-4 py-1.5 text-xs font-semibold text-white hover:bg-primary/90 transition-colors"
            >
              Apply
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
