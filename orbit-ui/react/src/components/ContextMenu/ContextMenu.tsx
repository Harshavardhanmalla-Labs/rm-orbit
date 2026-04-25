import { useState, useRef, useEffect, useCallback, createContext, useContext } from 'react';
import { Check, ChevronRight } from 'lucide-react';
import { cn } from '@/lib/cn';

// ─── Types ────────────────────────────────────────────────────────────────────

export interface ContextMenuItemProps {
  label: string;
  icon?: React.ReactNode;
  shortcut?: string;
  disabled?: boolean;
  danger?: boolean;
  checked?: boolean;
  onSelect?: () => void;
  /** Sub-items for nested menus */
  children?: ContextMenuItemProps[];
}

export interface ContextMenuProps {
  /** The element that triggers the context menu on right-click */
  children: React.ReactNode;
  /** Menu items */
  items: (ContextMenuItemProps | 'separator')[];
  className?: string;
}

// ─── Context ──────────────────────────────────────────────────────────────────

const CloseCtx = createContext<() => void>(() => {});

// ─── MenuItem ────────────────────────────────────────────────────────────────

interface MenuItemRendererProps {
  item: ContextMenuItemProps | 'separator';
  depth?: number;
}

function MenuItemRenderer({ item, depth = 0 }: MenuItemRendererProps) {
  const close = useContext(CloseCtx);
  const [subOpen, setSubOpen] = useState(false);
  const itemRef = useRef<HTMLDivElement>(null);

  if (item === 'separator') {
    return <div className="my-1 h-px bg-border-subtle" role="separator" />;
  }

  const hasChildren = item.children && item.children.length > 0;

  const handleClick = () => {
    if (item.disabled || hasChildren) return;
    item.onSelect?.();
    close();
  };

  return (
    <div
      ref={itemRef}
      className="relative"
      onMouseEnter={() => hasChildren && setSubOpen(true)}
      onMouseLeave={() => hasChildren && setSubOpen(false)}
    >
      <div
        role="menuitem"
        aria-disabled={item.disabled}
        aria-haspopup={hasChildren ? 'menu' : undefined}
        aria-expanded={hasChildren ? subOpen : undefined}
        tabIndex={item.disabled ? -1 : 0}
        onClick={handleClick}
        onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') handleClick(); }}
        className={cn(
          'flex items-center gap-2 rounded-md px-2.5 py-1.5 text-sm cursor-default outline-none transition-colors',
          item.disabled
            ? 'opacity-40 cursor-not-allowed'
            : item.danger
            ? 'text-danger-600 dark:text-danger-400 hover:bg-danger-50 dark:hover:bg-danger-900/20 focus:bg-danger-50 dark:focus:bg-danger-900/20'
            : 'text-content-primary hover:bg-surface-muted focus:bg-surface-muted',
        )}
      >
        {/* Check / Icon slot */}
        <span className="w-4 shrink-0 flex items-center justify-center">
          {item.checked
            ? <Check size={13} />
            : item.icon
            ? <span className="text-content-muted">{item.icon}</span>
            : null
          }
        </span>
        <span className="flex-1">{item.label}</span>
        {item.shortcut && (
          <kbd className="ml-auto text-[10px] text-content-muted bg-surface-muted px-1.5 py-0.5 rounded font-sans">
            {item.shortcut}
          </kbd>
        )}
        {hasChildren && <ChevronRight size={13} className="text-content-muted ml-1" />}
      </div>

      {/* Sub-menu */}
      {hasChildren && subOpen && (
        <div
          className="absolute left-full top-0 z-50 min-w-[180px] rounded-lg border border-border-default bg-surface-base p-1 shadow-lg"
          style={{ marginLeft: 4 }}
          role="menu"
        >
          {item.children!.map((child, i) => (
            <MenuItemRenderer key={i} item={child} depth={depth + 1} />
          ))}
        </div>
      )}
    </div>
  );
}

// ─── ContextMenu ─────────────────────────────────────────────────────────────

export function ContextMenu({ children, items, className }: ContextMenuProps) {
  const [open, setOpen] = useState(false);
  const [pos, setPos] = useState({ x: 0, y: 0 });
  const menuRef = useRef<HTMLDivElement>(null);

  const close = useCallback(() => setOpen(false), []);

  const onContextMenu = useCallback((e: React.MouseEvent) => {
    e.preventDefault();
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const menuW = 200;
    const menuH = items.length * 32;
    const x = e.clientX + menuW > vw ? e.clientX - menuW : e.clientX;
    const y = e.clientY + menuH > vh ? e.clientY - menuH : e.clientY;
    setPos({ x, y });
    setOpen(true);
  }, [items.length]);

  // Close on outside click
  useEffect(() => {
    if (!open) return;
    const handler = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) close();
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, [open, close]);

  // Close on Escape or scroll
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') close(); };
    const onScroll = () => close();
    document.addEventListener('keydown', onKey);
    window.addEventListener('scroll', onScroll, true);
    return () => {
      document.removeEventListener('keydown', onKey);
      window.removeEventListener('scroll', onScroll, true);
    };
  }, [open, close]);

  return (
    <CloseCtx.Provider value={close}>
      <div onContextMenu={onContextMenu} className={cn('contents', className)}>
        {children}
      </div>
      {open && (
        <div
          ref={menuRef}
          role="menu"
          aria-label="Context menu"
          style={{ position: 'fixed', left: pos.x, top: pos.y, zIndex: 9999 }}
          className="min-w-[180px] rounded-lg border border-border-default bg-surface-base p-1 shadow-lg animate-in fade-in-0 zoom-in-95"
        >
          {items.map((item, i) => (
            <MenuItemRenderer key={i} item={item} />
          ))}
        </div>
      )}
    </CloseCtx.Provider>
  );
}
