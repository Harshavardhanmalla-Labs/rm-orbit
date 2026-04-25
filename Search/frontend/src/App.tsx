import { useState, useEffect, useRef, useCallback } from 'react';
import { Badge, Skeleton, ThemeToggle } from '@orbit-ui/react';
import OrbitDock from './components/OrbitDock';
import {
  Search, FileText, Calendar, Mail, MessageSquare, BookOpen,
  Globe, Shield, DollarSign, Ticket, Clock, ExternalLink, Zap, X
} from 'lucide-react';
import { searchApi, type SearchResult } from './api/search';
import type { LucideIcon } from 'lucide-react';

// Source → icon + label + color
interface SourceMeta {
  icon: LucideIcon;
  label: string;
  color: string;
  port: number;
}

const SOURCE_META: Record<string, SourceMeta> = {
  atlas:     { icon: Globe,          label: 'Atlas',       color: 'bg-primary-600',  port: 5173  },
  writer:    { icon: FileText,       label: 'Writer',      color: 'bg-violet-600',   port: 45010 },
  learn:     { icon: BookOpen,       label: 'Learn',       color: 'bg-success-600',  port: 45009 },
  calendar:  { icon: Calendar,       label: 'Calendar',    color: 'bg-orange-500',   port: 45005 },
  mail:      { icon: Mail,           label: 'Mail',        color: 'bg-sky-600',      port: 45004 },
  connect:   { icon: MessageSquare,  label: 'Connect',     color: 'bg-indigo-600',   port: 45008 },
  secure:    { icon: Shield,         label: 'Secure',      color: 'bg-danger-600',   port: 45012 },
  capital:   { icon: DollarSign,     label: 'Capital Hub', color: 'bg-yellow-600',   port: 45013 },
  turbotick: { icon: Ticket,         label: 'TurboTick',   color: 'bg-amber-600',    port: 45018 },
  planet:    { icon: Globe,          label: 'Planet',      color: 'bg-emerald-600',  port: 45006 },
};

function resolveUrl(result: SearchResult): string {
  if (result.url) {
    if (result.url.startsWith('/')) {
      const meta = SOURCE_META[result.source];
      if (meta) return `http://localhost:${meta.port}${result.url}`;
    }
    return result.url;
  }
  const meta = SOURCE_META[result.source];
  return meta ? `http://localhost:${meta.port}` : '#';
}

function SourceBadge({ source }: { source: string }) {
  const meta = SOURCE_META[source];
  if (!meta) return <Badge color="neutral" size="sm">{source}</Badge>;
  const Icon = meta.icon;
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-white text-xs font-medium ${meta.color}`}>
      <Icon className="w-3 h-3" />
      {meta.label}
    </span>
  );
}

function ResultCard({ result, index, focused, onFocus }: {
  result: SearchResult;
  index: number;
  focused: boolean;
  onFocus: (i: number) => void;
}) {
  const url = resolveUrl(result);
  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      onMouseEnter={() => onFocus(index)}
      className={`
        block px-4 py-3.5 rounded-xl border transition-all group cursor-pointer
        ${focused
          ? 'bg-primary-50 border-primary-200 dark:bg-primary-950/30 dark:border-primary-800'
          : 'bg-surface-card border-border hover:bg-surface-subtle hover:border-border'
        }
      `}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <SourceBadge source={result.source} />
            <span className="text-xs text-muted-foreground capitalize">{result.entity_type}</span>
          </div>
          <p className="text-sm font-semibold text-foreground truncate group-hover:text-primary-700 dark:group-hover:text-primary-400">
            {result.title}
          </p>
          {result.snippet && (
            <p className="text-xs text-muted-foreground mt-1 line-clamp-2 leading-relaxed">
              {result.snippet}
            </p>
          )}
          {result.updated_at && (
            <p className="text-xs text-muted-foreground mt-1.5 flex items-center gap-1">
              <Clock className="w-3 h-3" />
              {new Date(result.updated_at).toLocaleDateString()}
            </p>
          )}
        </div>
        <ExternalLink className={`w-4 h-4 flex-shrink-0 mt-0.5 transition-colors ${focused ? 'text-primary-500' : 'text-muted-foreground opacity-0 group-hover:opacity-100'}`} />
      </div>
    </a>
  );
}

// Group results by source
function groupBySource(results: SearchResult[]): Record<string, SearchResult[]> {
  const groups: Record<string, SearchResult[]> = {};
  for (const r of results) {
    if (!groups[r.source]) groups[r.source] = [];
    groups[r.source].push(r);
  }
  return groups;
}

const POPULAR_SEARCHES = [
  'project status', 'upcoming meetings', 'recent documents', 'open tickets',
  'API keys', 'team members', 'compliance policies', 'expense report',
];

export default function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [took, setTook] = useState<number | null>(null);
  const [total, setTotal] = useState(0);
  const [sources, setSources] = useState<string[]>([]);
  const [activeSource, setActiveSource] = useState<string>('all');
  const [focusedIdx, setFocusedIdx] = useState(-1);
  const [hasSearched, setHasSearched] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | undefined>(undefined);

  // Load available sources on mount
  useEffect(() => {
    searchApi.getSources()
      .then(r => setSources(r.data.sources ?? []))
      .catch(() => {});
    inputRef.current?.focus();
  }, []);

  const doSearch = useCallback(async (q: string, source: string) => {
    if (!q.trim()) {
      setResults([]); setHasSearched(false); return;
    }
    setLoading(true);
    try {
      const srcFilter = source !== 'all' ? [source] : undefined;
      const res = await searchApi.search(q, srcFilter, 30);
      setResults(res.data.results ?? []);
      setTotal(res.data.total ?? 0);
      setTook(res.data.took_ms ?? null);
      setHasSearched(true);
    } catch {
      setResults([]); setTotal(0);
    } finally {
      setLoading(false);
      setFocusedIdx(-1);
    }
  }, []);

  useEffect(() => {
    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => doSearch(query, activeSource), 250);
    return () => clearTimeout(debounceRef.current);
  }, [query, activeSource, doSearch]);

  // Keyboard nav
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        setFocusedIdx(i => Math.min(i + 1, results.length - 1));
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        setFocusedIdx(i => Math.max(i - 1, -1));
      } else if (e.key === 'Enter' && focusedIdx >= 0) {
        const r = results[focusedIdx];
        if (r) window.open(resolveUrl(r), '_blank');
      } else if (e.key === 'Escape') {
        setQuery(''); setResults([]); setHasSearched(false); inputRef.current?.focus();
      } else if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        inputRef.current?.focus();
        inputRef.current?.select();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [results, focusedIdx]);

  const grouped = groupBySource(results);
  const allSources = ['all', ...sources];

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-surface-card sticky top-0 z-10">
        <div className="max-w-3xl mx-auto px-4 h-16 flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center flex-shrink-0">
            <Search className="w-4 h-4 text-white" />
          </div>
          <span className="font-bold text-foreground text-sm hidden sm:block">Orbit Search</span>
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground pointer-events-none" />
            <input
              ref={inputRef}
              value={query}
              onChange={e => setQuery(e.target.value)}
              placeholder="Search everything… (⌘K)"
              className="w-full pl-9 pr-9 py-2 text-sm bg-surface-subtle border border-border rounded-lg text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary-500/30 focus:border-primary-400 transition-colors"
            />
            {query && (
              <button
                onClick={() => { setQuery(''); setResults([]); setHasSearched(false); inputRef.current?.focus(); }}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
          <ThemeToggle />
        </div>
      </header>

      <div className="max-w-3xl mx-auto px-4 py-6 space-y-5">
        {/* Source filter tabs */}
        {sources.length > 0 && (
          <div className="flex gap-2 flex-wrap">
            {allSources.map(src => {
              const meta = SOURCE_META[src];
              return (
                <button
                  key={src}
                  onClick={() => setActiveSource(src)}
                  className={`
                    inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-colors
                    ${activeSource === src
                      ? 'bg-primary-600 text-white'
                      : 'bg-surface-card border border-border text-muted-foreground hover:text-foreground hover:border-primary-300'}
                  `}
                >
                  {meta && <meta.icon className="w-3 h-3" />}
                  {src === 'all' ? 'All Sources' : (meta?.label ?? src)}
                </button>
              );
            })}
          </div>
        )}

        {/* Stats */}
        {hasSearched && !loading && (
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <Zap className="w-3.5 h-3.5 text-primary-500" />
            <span>{total} result{total !== 1 ? 's' : ''}</span>
            {took !== null && <span>· {took}ms</span>}
            {query && <span>· for "<span className="font-medium text-foreground">{query}</span>"</span>}
          </div>
        )}

        {/* Loading skeletons */}
        {loading && (
          <div className="space-y-3">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="bg-surface-card border border-border rounded-xl p-4 space-y-2">
                <div className="flex items-center gap-2">
                  <Skeleton className="h-5 w-16 rounded-full" />
                  <Skeleton className="h-4 w-12" />
                </div>
                <Skeleton className="h-4 w-3/4" />
                <Skeleton className="h-3 w-full" />
                <Skeleton className="h-3 w-4/5" />
              </div>
            ))}
          </div>
        )}

        {/* Results */}
        {!loading && hasSearched && results.length > 0 && (
          activeSource === 'all' ? (
            // Grouped by source
            Object.entries(grouped).map(([src, items]) => {
              const meta = SOURCE_META[src];
              const Icon = meta?.icon ?? Search;
              return (
                <div key={src}>
                  <div className="flex items-center gap-2 mb-3">
                    <div className={`w-5 h-5 rounded flex items-center justify-center ${meta?.color ?? 'bg-neutral-500'}`}>
                      <Icon className="w-3 h-3 text-white" />
                    </div>
                    <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
                      {meta?.label ?? src}
                    </span>
                    <span className="text-xs text-muted-foreground">({items.length})</span>
                  </div>
                  <div className="space-y-2">
                    {items.map((r) => {
                      const globalIdx = results.indexOf(r);
                      return (
                        <ResultCard
                          key={r.id}
                          result={r}
                          index={globalIdx}
                          focused={focusedIdx === globalIdx}
                          onFocus={setFocusedIdx}
                        />
                      );
                    })}
                  </div>
                </div>
              );
            })
          ) : (
            // Flat list for single source
            <div className="space-y-2">
              {results.map((r, i) => (
                <ResultCard
                  key={r.id}
                  result={r}
                  index={i}
                  focused={focusedIdx === i}
                  onFocus={setFocusedIdx}
                />
              ))}
            </div>
          )
        )}

        {/* Empty state */}
        {!loading && hasSearched && results.length === 0 && (
          <div className="py-16 text-center">
            <Search className="w-10 h-10 mx-auto text-muted-foreground opacity-40 mb-4" />
            <p className="text-sm font-medium text-foreground mb-1">No results found</p>
            <p className="text-xs text-muted-foreground">
              Try different keywords or check that the relevant services are running.
            </p>
          </div>
        )}

        {/* Empty / idle state */}
        {!hasSearched && !loading && (
          <div className="py-10 text-center space-y-6">
            <div>
              <div className="w-16 h-16 rounded-2xl bg-primary-600/10 flex items-center justify-center mx-auto mb-4">
                <Search className="w-8 h-8 text-primary-600" />
              </div>
              <h2 className="text-lg font-semibold text-foreground mb-1">Search across RM Orbit</h2>
              <p className="text-sm text-muted-foreground max-w-xs mx-auto">
                Find projects, documents, messages, tickets, emails, and more — all in one place.
              </p>
            </div>

            {/* Popular searches */}
            <div>
              <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-3">Popular searches</p>
              <div className="flex flex-wrap gap-2 justify-center">
                {POPULAR_SEARCHES.map(s => (
                  <button
                    key={s}
                    onClick={() => setQuery(s)}
                    className="px-3 py-1.5 bg-surface-card border border-border rounded-full text-xs text-muted-foreground hover:text-foreground hover:border-primary-300 transition-colors"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>

            {/* Keyboard hint */}
            <p className="text-xs text-muted-foreground">
              <kbd className="px-1.5 py-0.5 bg-surface-subtle border border-border rounded text-xs font-mono">↑</kbd>
              {' '}<kbd className="px-1.5 py-0.5 bg-surface-subtle border border-border rounded text-xs font-mono">↓</kbd>
              {' '}to navigate · {' '}
              <kbd className="px-1.5 py-0.5 bg-surface-subtle border border-border rounded text-xs font-mono">Enter</kbd>
              {' '}to open · {' '}
              <kbd className="px-1.5 py-0.5 bg-surface-subtle border border-border rounded text-xs font-mono">Esc</kbd>
              {' '}to clear
            </p>
          </div>
        )}
      </div>
      <OrbitDock />
    </div>
  );
}
