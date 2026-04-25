import { useState, useEffect, useRef, useCallback } from 'react';
import { useLocation } from 'react-router-dom';
import { getWorkspaceId, writerApi } from '../utils/api';
import {
  Bold, Italic, Underline, Strikethrough, Code, List, ListOrdered,
  Heading1, Heading2, Heading3, Quote, Minus, AlignLeft, AlignCenter, AlignRight,
  Undo, Redo, Save, Clock, Loader2, Plus, Trash2,
} from 'lucide-react';

// ─── Types ────────────────────────────────────────────────────────────────────

type BlockType = 'text' | 'heading1' | 'heading2' | 'heading3' | 'quote' | 'code' | 'bullet' | 'numbered' | 'divider';

interface Block {
  id: string;
  type: BlockType;
  content: { text?: string; html?: string; [key: string]: unknown };
  version: number;
  position_index: number;
}

interface DocumentData {
  id: string;
  title: string;
  root_block_id?: string;
  updated_at: string;
  block_count?: number;
}

interface BlockVersion {
  id: number;
  block_id: string;
  snapshot: {
    version?: number;
    content?: {
      html?: string;
      text?: string;
    };
  };
  created_at: string;
}

// ─── Save status ──────────────────────────────────────────────────────────────

type SaveState = 'saved' | 'unsaved' | 'saving' | 'error';

// ─── Formatting toolbar ───────────────────────────────────────────────────────

interface ToolbarBtn { label: string; cmd: string; arg?: string; icon?: React.ElementType; active?: boolean }

function execFmt(cmd: string, arg?: string) {
  document.execCommand(cmd, false, arg ?? undefined);
}

function ToolbarButton({ label, cmd, arg, icon: Icon, active }: ToolbarBtn) {
  return (
    <button
      type="button"
      title={label}
      onMouseDown={e => { e.preventDefault(); execFmt(cmd, arg); }}
      className={[
        'flex items-center justify-center rounded p-1.5 transition-colors',
        active ? 'bg-primary-100 text-primary-700' : 'text-content-muted hover:bg-surface-muted hover:text-content-primary',
      ].join(' ')}
    >
      {Icon ? <Icon className="h-3.5 w-3.5" /> : <span className="text-xs font-medium">{label}</span>}
    </button>
  );
}

function ToolbarDivider() {
  return <div className="mx-1 h-4 w-px bg-border-default" />;
}

// ─── Block type selector ──────────────────────────────────────────────────────

const BLOCK_TYPE_OPTIONS: { value: BlockType; label: string; icon?: React.ElementType }[] = [
  { value: 'text',     label: 'Paragraph' },
  { value: 'heading1', label: 'Heading 1', icon: Heading1 },
  { value: 'heading2', label: 'Heading 2', icon: Heading2 },
  { value: 'heading3', label: 'Heading 3', icon: Heading3 },
  { value: 'quote',    label: 'Quote',     icon: Quote },
  { value: 'code',     label: 'Code',      icon: Code },
  { value: 'bullet',   label: 'Bullet list', icon: List },
  { value: 'numbered', label: 'Numbered list', icon: ListOrdered },
  { value: 'divider',  label: 'Divider',   icon: Minus },
];

// ─── Block rendering ──────────────────────────────────────────────────────────

const blockTypeClasses: Record<BlockType, string> = {
  text:     'text-base text-content-primary leading-relaxed',
  heading1: 'text-3xl font-bold text-content-primary leading-tight mt-4',
  heading2: 'text-2xl font-semibold text-content-primary leading-tight mt-3',
  heading3: 'text-xl font-medium text-content-primary leading-snug mt-2',
  quote:    'border-l-4 border-primary-400 pl-4 text-base italic text-content-secondary',
  code:     'font-mono text-sm bg-surface-muted rounded-lg p-4 text-content-primary',
  bullet:   'text-base text-content-primary leading-relaxed list-disc pl-6',
  numbered: 'text-base text-content-primary leading-relaxed list-decimal pl-6',
  divider:  '',
};

// ─── Main Document Editor ─────────────────────────────────────────────────────

export default function Document() {
  const location = useLocation();
  const [workspaceId] = useState(location.state?.workspaceId || getWorkspaceId());
  const [documentId, setDocumentId] = useState<string | null>(location.state?.documentId || null);
  const [documentTitle, setDocumentTitle] = useState<string>(location.state?.documentTitle || 'Untitled');
  const [doc, setDoc] = useState<DocumentData | null>(null);
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [selectedBlockId, setSelectedBlockId] = useState<string | null>(null);
  const [saveState, setSaveState] = useState<SaveState>('saved');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [blockMenuOpen, setBlockMenuOpen] = useState(false);
  const [versions, setVersions] = useState<BlockVersion[]>([]);
  const [editingTitle, setEditingTitle] = useState(false);

  const blockRefs = useRef<Record<string, HTMLDivElement | null>>({});
  const saveTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const pendingContent = useRef<Record<string, string>>({});

  // ── Load ──────────────────────────────────────────────────────────────────
  const loadDocument = useCallback(async (docId?: string | null) => {
    setLoading(true);
    setError('');
    try {
      const id = docId ?? documentId;
      let resolvedId = id;
      if (!resolvedId) {
        const docs = await writerApi<DocumentData[]>('/documents?limit=1', { workspaceId });
        if (!docs.length) { setLoading(false); return; }
        resolvedId = docs[0].id;
        setDocumentId(resolvedId);
        setDocumentTitle(docs[0].title);
      }

      const [docData, docBlocks] = await Promise.all([
        writerApi<DocumentData>(`/documents/${resolvedId}`, { workspaceId }),
        writerApi<Block[]>(`/documents/${resolvedId}/blocks`, { workspaceId }),
      ]);

      setDoc(docData);
      setDocumentTitle(docData.title);
      const sorted = [...docBlocks].sort((a, b) => (a.position_index ?? 0) - (b.position_index ?? 0));
      setBlocks(sorted);
      if (sorted.length > 0) {
        setSelectedBlockId(prev => prev ?? sorted[0].id);
      }
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : 'Could not load document.';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [workspaceId, documentId]);

  useEffect(() => { void loadDocument(); }, [loadDocument]);

  // ── Versions ──────────────────────────────────────────────────────────────
  const loadVersions = useCallback(async (blockId: string) => {
    try {
      const hist = await writerApi<BlockVersion[]>(`/blocks/${blockId}/versions`, { workspaceId });
      setVersions(hist);
    } catch { setVersions([]); }
  }, [workspaceId]);

  useEffect(() => {
    if (selectedBlockId) {
      void loadVersions(selectedBlockId);
    }
  }, [selectedBlockId, loadVersions]);

  // ── Auto-save on content change ───────────────────────────────────────────
  const scheduleBlockSave = useCallback((blockId: string, html: string) => {
    pendingContent.current[blockId] = html;
    setSaveState('unsaved');
    if (saveTimer.current) clearTimeout(saveTimer.current);
    saveTimer.current = setTimeout(async () => {
      setSaveState('saving');
      try {
        await Promise.all(
          Object.entries(pendingContent.current).map(async ([id, content]) => {
            const block = blocks.find(b => b.id === id);
            if (!block) return;
            const updated = await writerApi<Block>(`/blocks/${id}`, {
              method: 'PATCH',
              workspaceId,
              body: { content: { html: content, text: stripHtml(content) } },
            });
            setBlocks(prev => prev.map(b => b.id === id ? { ...b, ...updated } : b));
          })
        );
        pendingContent.current = {};
        setSaveState('saved');
      } catch {
        setSaveState('error');
      }
    }, 1200);
  }, [blocks, workspaceId]);

  function stripHtml(html: string): string {
    return html.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim();
  }

  // ── Title save ────────────────────────────────────────────────────────────
  const saveTitle = async () => {
    if (!documentId || !documentTitle.trim()) return;
    setEditingTitle(false);
    try {
      await writerApi<DocumentData>(`/documents/${documentId}`, {
        method: 'PATCH',
        workspaceId,
        body: { title: documentTitle.trim() },
      });
    } catch { /* best effort */ }
  };

  // ── Add block ─────────────────────────────────────────────────────────────
  const addBlock = async (type: BlockType = 'text') => {
    if (!doc) return;
    setBlockMenuOpen(false);
    const maxPos = blocks.length ? Math.max(...blocks.map(b => b.position_index ?? 0)) : 0;
    try {
      const created = await writerApi<Block>(`/documents/${doc.id}/blocks`, {
        method: 'POST',
        workspaceId,
        body: {
          parent_block_id: selectedBlockId || doc.root_block_id || null,
          type,
          content: { html: '', text: '' },
          position_index: maxPos + 10,
        },
      });
      setBlocks(prev => [...prev, { ...created, type: type as BlockType }]);
      setSelectedBlockId(created.id);
      setTimeout(() => blockRefs.current[created.id]?.focus(), 80);
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : 'Could not create block.';
      setError(message);
    }
  };

  // ── Delete block ──────────────────────────────────────────────────────────
  const deleteBlock = async (id: string) => {
    try {
      await writerApi(`/blocks/${id}`, { method: 'DELETE', workspaceId });
      setBlocks(prev => prev.filter(b => b.id !== id));
      setSelectedBlockId(prev => {
        if (prev !== id) return prev;
        const remaining = blocks.filter(b => b.id !== id);
        return remaining[remaining.length - 1]?.id ?? null;
      });
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : 'Could not delete block.';
      setError(message);
    }
  };

  // ── Force save ────────────────────────────────────────────────────────────
  const forceSave = useCallback(() => {
    if (saveTimer.current) clearTimeout(saveTimer.current);
    Object.entries(pendingContent.current).forEach(([id, html]) => scheduleBlockSave(id, html));
  }, [scheduleBlockSave]);

  const selectedBlock = blocks.find(b => b.id === selectedBlockId) ?? null;

  // ── Keyboard shortcuts ────────────────────────────────────────────────────
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 's') { e.preventDefault(); forceSave(); }
    };
    document.addEventListener('keydown', onKey);
    return () => document.removeEventListener('keydown', onKey);
  }, [forceSave]);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-content-muted" />
      </div>
    );
  }

  if (!doc && !loading) {
    return (
      <div className="flex h-full flex-col items-center justify-center gap-4 text-center px-8">
        <p className="text-content-secondary text-sm font-medium">No document found in this workspace.</p>
        <p className="text-xs text-content-muted">Create a document from the Dashboard.</p>
      </div>
    );
  }

  // ─────────────────────────────────────────────────────────────────────────

  return (
    <div className="flex h-full overflow-hidden bg-surface-base">

      {/* ── Sidebar: Block tree ── */}
      <aside className="hidden lg:flex w-56 flex-none flex-col border-r border-border-default bg-surface-muted/50">
        <div className="border-b border-border-default px-3 py-3 flex items-center gap-2">
          <span className="flex-1 text-xs font-semibold text-content-secondary uppercase tracking-wider">Blocks</span>
          <button onClick={() => setBlockMenuOpen(v => !v)}
            className="rounded p-1 text-content-muted hover:bg-surface-muted hover:text-content-primary transition-colors">
            <Plus className="h-3.5 w-3.5" />
          </button>
        </div>

        {/* Block type dropdown */}
        {blockMenuOpen && (
          <div className="border-b border-border-default bg-surface-base shadow-md">
            {BLOCK_TYPE_OPTIONS.map(opt => (
              <button key={opt.value} onClick={() => addBlock(opt.value)}
                className="flex w-full items-center gap-2 px-3 py-1.5 text-xs text-content-secondary hover:bg-surface-muted hover:text-content-primary transition-colors">
                {opt.icon ? <opt.icon className="h-3.5 w-3.5" /> : <span className="h-3.5 w-3.5" />}
                {opt.label}
              </button>
            ))}
          </div>
        )}

        <nav className="flex-1 overflow-y-auto py-2 px-2 space-y-0.5">
          {blocks.map((block, i) => (
            <button key={block.id} onClick={() => { setSelectedBlockId(block.id); blockRefs.current[block.id]?.focus(); }}
              className={[
                'w-full text-left px-2.5 py-1.5 rounded-md text-[11px] transition-colors flex items-center gap-2 group',
                selectedBlockId === block.id
                  ? 'bg-primary-50 text-primary-700 dark:bg-primary-950/30 dark:text-primary-400 font-medium'
                  : 'text-content-muted hover:text-content-primary hover:bg-surface-muted',
              ].join(' ')}>
              <span className="w-4 text-[9px] text-content-muted font-mono">{i + 1}</span>
              <span className="truncate flex-1">{block.type.toUpperCase()} {stripHtml(block.content?.html || block.content?.text || '').slice(0, 16) || '…'}</span>
            </button>
          ))}
        </nav>
      </aside>

      {/* ── Main editor area ── */}
      <div className="flex flex-1 flex-col overflow-hidden">

        {/* Format toolbar */}
        <div className="flex items-center gap-0.5 border-b border-border-default bg-surface-base px-3 py-2 flex-wrap shrink-0">
          <ToolbarButton label="Bold" cmd="bold" icon={Bold} />
          <ToolbarButton label="Italic" cmd="italic" icon={Italic} />
          <ToolbarButton label="Underline" cmd="underline" icon={Underline} />
          <ToolbarButton label="Strikethrough" cmd="strikeThrough" icon={Strikethrough} />
          <ToolbarDivider />
          <ToolbarButton label="Heading 1" cmd="formatBlock" arg="h1" icon={Heading1} />
          <ToolbarButton label="Heading 2" cmd="formatBlock" arg="h2" icon={Heading2} />
          <ToolbarButton label="Heading 3" cmd="formatBlock" arg="h3" icon={Heading3} />
          <ToolbarDivider />
          <ToolbarButton label="Bullet list" cmd="insertUnorderedList" icon={List} />
          <ToolbarButton label="Numbered list" cmd="insertOrderedList" icon={ListOrdered} />
          <ToolbarButton label="Blockquote" cmd="formatBlock" arg="blockquote" icon={Quote} />
          <ToolbarButton label="Inline code" cmd="formatBlock" arg="pre" icon={Code} />
          <ToolbarDivider />
          <ToolbarButton label="Align left" cmd="justifyLeft" icon={AlignLeft} />
          <ToolbarButton label="Align center" cmd="justifyCenter" icon={AlignCenter} />
          <ToolbarButton label="Align right" cmd="justifyRight" icon={AlignRight} />
          <ToolbarDivider />
          <ToolbarButton label="Undo" cmd="undo" icon={Undo} />
          <ToolbarButton label="Redo" cmd="redo" icon={Redo} />
          <div className="flex-1" />
          {/* Save status */}
          <div className="flex items-center gap-1.5 text-[11px] ml-2">
            {saveState === 'saving' && <><Loader2 className="h-3 w-3 animate-spin text-content-muted" /><span className="text-content-muted">Saving…</span></>}
            {saveState === 'saved' && <><Clock className="h-3 w-3 text-success-500" /><span className="text-success-600">Saved</span></>}
            {saveState === 'unsaved' && <span className="text-warning-600">Unsaved</span>}
            {saveState === 'error' && <span className="text-danger-600">Save error</span>}
          </div>
          <button onClick={forceSave} title="Save (Ctrl+S)"
            className="ml-2 flex items-center gap-1 rounded-lg bg-primary-600 px-2.5 py-1 text-[11px] font-medium text-white hover:bg-primary-700 transition-colors">
            <Save className="h-3 w-3" /> Save
          </button>
        </div>

        {/* Document content */}
        <main className="flex-1 overflow-y-auto">
          <div className="mx-auto max-w-[720px] px-8 py-10 pb-32">

            {/* Document title */}
            {editingTitle ? (
              <input
                autoFocus
                value={documentTitle}
                onChange={e => setDocumentTitle(e.target.value)}
                onBlur={saveTitle}
                onKeyDown={e => { if (e.key === 'Enter') saveTitle(); if (e.key === 'Escape') { setEditingTitle(false); setDocumentTitle(doc?.title || ''); } }}
                className="mb-6 w-full text-4xl font-bold text-content-primary bg-transparent border-none outline-none focus:ring-0 placeholder-content-muted"
                placeholder="Untitled"
              />
            ) : (
              <h1
                className="mb-6 text-4xl font-bold text-content-primary cursor-text hover:opacity-80 transition-opacity"
                onClick={() => setEditingTitle(true)}
              >
                {documentTitle || 'Untitled'}
              </h1>
            )}

            {error && (
              <div className="mb-4 rounded-lg border border-danger-200 bg-danger-50 px-4 py-2.5 text-sm text-danger-700">{error}</div>
            )}

            {/* Blocks */}
            <div className="space-y-1">
              {blocks.map(block => {
                const isSelected = selectedBlockId === block.id;
                if (block.type === 'divider') {
                  return (
                    <div key={block.id} className="group relative flex items-center py-2">
                      <hr className="w-full border-border-default" />
                      {isSelected && (
                        <button onClick={() => deleteBlock(block.id)}
                          className="absolute right-0 hidden group-hover:flex items-center justify-center h-5 w-5 rounded text-danger-400 hover:text-danger-600 hover:bg-danger-50 transition-colors">
                          <Trash2 className="h-3 w-3" />
                        </button>
                      )}
                    </div>
                  );
                }

                return (
                  <div key={block.id} className="group relative">
                    <div
                      ref={el => { blockRefs.current[block.id] = el; }}
                      contentEditable
                      suppressContentEditableWarning
                      spellCheck
                      data-block-id={block.id}
                      dangerouslySetInnerHTML={{ __html: block.content?.html || block.content?.text || '' }}
                      onFocus={() => setSelectedBlockId(block.id)}
                      onInput={e => scheduleBlockSave(block.id, (e.target as HTMLDivElement).innerHTML)}
                      onKeyDown={e => {
                        // Ctrl+Enter: add new block after
                        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                          e.preventDefault(); addBlock('text');
                        }
                        // Backspace on empty block: delete
                        if (e.key === 'Backspace') {
                          const el = e.target as HTMLDivElement;
                          if (!el.textContent?.trim() && !el.innerHTML?.replace(/<br\s*\/?>/gi, '').trim()) {
                            e.preventDefault(); deleteBlock(block.id);
                          }
                        }
                      }}
                      className={[
                        'min-h-[1.5rem] w-full rounded-lg px-1 py-0.5 outline-none transition-colors focus:bg-primary-50/40 dark:focus:bg-primary-950/10',
                        blockTypeClasses[block.type] || blockTypeClasses.text,
                        isSelected ? 'ring-1 ring-primary-200' : '',
                        'empty:before:content-[attr(data-placeholder)] empty:before:text-content-muted empty:before:pointer-events-none',
                      ].join(' ')}
                      data-placeholder={block.type === 'text' ? 'Write something, or press / for commands…' : `${block.type}…`}
                    />
                    {/* Block actions on hover */}
                    <div className="absolute right-0 top-1 hidden items-center gap-1 group-hover:flex">
                      <button onClick={() => deleteBlock(block.id)}
                        className="flex items-center justify-center h-5 w-5 rounded text-content-muted hover:text-danger-600 hover:bg-danger-50 transition-colors">
                        <Trash2 className="h-3 w-3" />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Add block CTA */}
            <div className="mt-4">
              <button onClick={() => addBlock('text')}
                className="flex items-center gap-2 text-xs text-content-muted hover:text-content-secondary transition-colors">
                <Plus className="h-3.5 w-3.5" /> Add block
              </button>
            </div>
          </div>
        </main>
      </div>

      {/* ── Right panel: Version history ── */}
      <aside className="hidden xl:flex w-72 flex-none flex-col border-l border-border-default bg-surface-muted/30">
        <div className="border-b border-border-default px-4 py-3">
          <h3 className="text-xs font-semibold text-content-secondary uppercase tracking-wider">Version History</h3>
          {selectedBlock && <p className="mt-0.5 text-[11px] text-content-muted truncate">Block: {selectedBlock.type} · v{selectedBlock.version}</p>}
        </div>
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          {!selectedBlock && (
            <p className="text-[11px] text-content-muted px-1">Click a block to see its versions.</p>
          )}
          {selectedBlock && versions.length === 0 && (
            <p className="text-[11px] text-content-muted px-1">No snapshots yet. Save this block to create one.</p>
          )}
          {versions.map(v => (
            <div key={v.id} className="rounded-lg border border-border-default bg-surface-base p-3 shadow-sm">
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-semibold text-content-primary">v{v.snapshot?.version ?? '?'}</span>
                <span className="text-[10px] text-content-muted">{new Date(v.created_at).toLocaleTimeString()}</span>
              </div>
              <p className="mt-1 text-[10px] text-content-muted">{new Date(v.created_at).toLocaleDateString()}</p>
              <button
                onClick={() => {
                  if (!selectedBlockId) return;
                  const html = v.snapshot?.content?.html || v.snapshot?.content?.text || '';
                  const el = blockRefs.current[selectedBlockId];
                  if (el) { el.innerHTML = html; scheduleBlockSave(selectedBlockId, html); }
                }}
                className="mt-1.5 text-[10px] font-medium text-primary-600 hover:underline"
              >
                Restore this version
              </button>
            </div>
          ))}
        </div>
      </aside>
    </div>
  );
}
