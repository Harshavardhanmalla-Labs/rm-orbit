import { useState, useRef, useCallback, useId } from 'react';
import { Upload, X, File, Image, FileText, FileArchive, CheckCircle2, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/cn';

// ─── Types ────────────────────────────────────────────────────────────────────

export type FileUploadStatus = 'idle' | 'uploading' | 'done' | 'error';

export interface FileItem {
  id: string;
  file: File;
  status: FileUploadStatus;
  progress: number;
  error?: string;
  url?: string;
}

export interface FileUploadProps {
  /** Accepted MIME types or extensions, e.g. "image/*,.pdf" */
  accept?: string;
  /** Allow multiple files */
  multiple?: boolean;
  /** Max file size in bytes */
  maxSize?: number;
  /** Max number of files */
  maxFiles?: number;
  /** Called with the list of accepted File objects */
  onFiles?: (files: File[]) => void;
  /** Custom upload handler. If provided, FileUpload will show progress states. */
  onUpload?: (file: File, onProgress: (pct: number) => void) => Promise<string | void>;
  /** Whether to show the file list below the drop zone */
  showList?: boolean;
  /** Disabled state */
  disabled?: boolean;
  className?: string;
  /** Drop zone label */
  label?: string;
  /** Drop zone sublabel */
  sublabel?: string;
  /** Variant */
  variant?: 'default' | 'compact';
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function getFileIcon(file: File) {
  if (file.type.startsWith('image/')) return Image;
  if (file.type === 'application/pdf' || file.name.endsWith('.pdf')) return FileText;
  if (file.type.includes('zip') || file.type.includes('archive') || file.name.endsWith('.zip')) return FileArchive;
  return File;
}

function genId(): string {
  return Math.random().toString(36).slice(2, 10);
}

// ─── FileUpload ───────────────────────────────────────────────────────────────

export function FileUpload({
  accept,
  multiple = false,
  maxSize,
  maxFiles,
  onFiles,
  onUpload,
  showList = true,
  disabled = false,
  className,
  label = 'Drop files here or click to browse',
  sublabel,
  variant = 'default',
}: FileUploadProps) {
  const inputId = useId();
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [items, setItems] = useState<FileItem[]>([]);
  const [error, setError] = useState<string | null>(null);

  const updateItem = (id: string, patch: Partial<FileItem>) => {
    setItems(prev => prev.map(it => it.id === id ? { ...it, ...patch } : it));
  };

  const processFiles = useCallback(async (rawFiles: FileList | File[]) => {
    setError(null);
    const fileArr = Array.from(rawFiles);

    // Validate
    const remaining = maxFiles ? maxFiles - items.length : Infinity;
    const toProcess = fileArr.slice(0, remaining);

    const rejected: string[] = [];
    const accepted: File[] = [];

    for (const f of toProcess) {
      if (maxSize && f.size > maxSize) {
        rejected.push(`"${f.name}" exceeds ${formatBytes(maxSize)}`);
        continue;
      }
      accepted.push(f);
    }

    if (rejected.length) setError(rejected.join(', '));
    if (!accepted.length) return;

    onFiles?.(accepted);

    // Build items
    const newItems: FileItem[] = accepted.map(f => ({
      id: genId(), file: f, status: 'idle' as FileUploadStatus, progress: 0,
    }));

    setItems(prev => [...prev, ...newItems]);

    if (onUpload) {
      for (const item of newItems) {
        updateItem(item.id, { status: 'uploading' });
        try {
          const url = await onUpload(item.file, (pct) => {
            updateItem(item.id, { progress: pct });
          });
          updateItem(item.id, { status: 'done', progress: 100, url: url ?? undefined });
        } catch (err: unknown) {
          updateItem(item.id, { status: 'error', error: err instanceof Error ? err.message : 'Upload failed' });
        }
      }
    } else {
      // No upload handler — just mark as done
      newItems.forEach(it => updateItem(it.id, { status: 'done', progress: 100 }));
    }
  }, [items.length, maxFiles, maxSize, onFiles, onUpload]);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    if (disabled) return;
    processFiles(e.dataTransfer.files);
  }, [disabled, processFiles]);

  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.length) {
      processFiles(e.target.files);
      e.target.value = '';
    }
  };

  const removeItem = (id: string) => setItems(prev => prev.filter(it => it.id !== id));

  const compact = variant === 'compact';

  return (
    <div className={cn('space-y-3', className)}>
      {/* Drop Zone */}
      <label
        htmlFor={inputId}
        onDragOver={e => { e.preventDefault(); if (!disabled) setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        className={cn(
          'relative flex flex-col items-center justify-center rounded-xl border-2 border-dashed transition-colors cursor-pointer',
          compact ? 'gap-1 p-4' : 'gap-3 p-8',
          disabled ? 'opacity-50 cursor-not-allowed' : 'hover:border-primary/60 hover:bg-primary/5',
          dragging ? 'border-primary bg-primary/5 scale-[1.01]' : 'border-border-default bg-surface-muted',
        )}
      >
        <div className={cn(
          'flex items-center justify-center rounded-full bg-surface-base border border-border-default',
          compact ? 'h-8 w-8' : 'h-12 w-12',
        )}>
          <Upload size={compact ? 14 : 20} className={cn('text-content-muted', dragging && 'text-primary')} />
        </div>
        <div className="text-center">
          <p className={cn('font-medium text-content-primary', compact ? 'text-xs' : 'text-sm')}>{label}</p>
          {sublabel && <p className="mt-0.5 text-xs text-content-muted">{sublabel}</p>}
          {!sublabel && (
            <p className="mt-0.5 text-xs text-content-muted">
              {accept ? `Accepted: ${accept}` : 'All file types accepted'}
              {maxSize ? ` · Max ${formatBytes(maxSize)}` : ''}
            </p>
          )}
        </div>
        <input
          ref={inputRef}
          id={inputId}
          type="file"
          accept={accept}
          multiple={multiple}
          disabled={disabled}
          onChange={onInputChange}
          className="sr-only"
          aria-label={label}
        />
      </label>

      {/* Validation error */}
      {error && (
        <p className="flex items-center gap-1.5 text-xs text-danger-600 dark:text-danger-400">
          <AlertCircle size={13} />
          {error}
        </p>
      )}

      {/* File list */}
      {showList && items.length > 0 && (
        <ul className="space-y-2" role="list">
          {items.map(item => {
            const Icon = getFileIcon(item.file);
            return (
              <li
                key={item.id}
                className="flex items-center gap-3 rounded-lg border border-border-subtle bg-surface-base px-3 py-2"
              >
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-surface-muted text-content-muted">
                  <Icon size={16} />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-medium text-content-primary">{item.file.name}</p>
                  <div className="flex items-center gap-2 mt-0.5">
                    <span className="text-xs text-content-muted">{formatBytes(item.file.size)}</span>
                    {item.status === 'error' && item.error && (
                      <span className="text-xs text-danger-600 dark:text-danger-400">{item.error}</span>
                    )}
                  </div>
                  {item.status === 'uploading' && (
                    <div className="mt-1.5 h-1 w-full rounded-full bg-surface-muted overflow-hidden">
                      <div
                        className="h-full rounded-full bg-primary transition-all duration-300"
                        style={{ width: `${item.progress}%` }}
                      />
                    </div>
                  )}
                </div>
                <div className="shrink-0">
                  {item.status === 'uploading' && (
                    <span className="text-xs text-content-muted">{item.progress}%</span>
                  )}
                  {item.status === 'done' && (
                    <CheckCircle2 size={16} className="text-success-500" />
                  )}
                  {item.status === 'error' && (
                    <AlertCircle size={16} className="text-danger-500" />
                  )}
                </div>
                <button
                  onClick={() => removeItem(item.id)}
                  className="shrink-0 p-1 rounded text-content-muted hover:text-danger-600 hover:bg-danger-50 dark:hover:bg-danger-900/20 transition-colors"
                  aria-label={`Remove ${item.file.name}`}
                >
                  <X size={14} />
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
