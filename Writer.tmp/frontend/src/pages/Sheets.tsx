import { useState, useCallback, useRef, useEffect } from 'react';
import { Download, Plus, Trash2, Sparkles, Search, Filter } from 'lucide-react';

type CellValue = string | number | null;

interface Column {
  id: string;
  label: string;
  type: 'text' | 'number' | 'currency' | 'date' | 'badge';
  width: number;
}

interface Row {
  id: string;
  cells: Record<string, CellValue>;
}

interface Sheet {
  id: string;
  name: string;
  columns: Column[];
  rows: Row[];
}

const INITIAL_SHEETS: Sheet[] = [
  {
    id: 'sheet-1',
    name: 'Q3 Financials',
    columns: [
      { id: 'id',          label: 'ID',          type: 'text',     width: 100 },
      { id: 'description', label: 'Description', type: 'text',     width: 240 },
      { id: 'category',    label: 'Category',    type: 'badge',    width: 130 },
      { id: 'date',        label: 'Date',        type: 'date',     width: 120 },
      { id: 'amount',      label: 'Amount',      type: 'currency', width: 130 },
      { id: 'status',      label: 'Status',      type: 'badge',    width: 110 },
    ],
    rows: [
      { id: 'r1', cells: { id: 'TRX-001', description: 'Q3 Server Infrastructure', category: 'Infrastructure', date: '2024-07-01', amount: 12450,   status: 'Paid'    } },
      { id: 'r2', cells: { id: 'TRX-002', description: 'Enterprise License',        category: 'Software',       date: '2024-07-05', amount: 45000,   status: 'Paid'    } },
      { id: 'r3', cells: { id: 'TRX-003', description: 'Marketing Campaign',        category: 'Marketing',      date: '2024-07-12', amount: 8500,    status: 'Pending' } },
      { id: 'r4', cells: { id: 'TRX-004', description: 'Office Supplies',           category: 'Operations',     date: '2024-07-15', amount: 1200,    status: 'Paid'    } },
      { id: 'r5', cells: { id: 'TRX-005', description: 'AWS Reserved Instances',   category: 'Infrastructure', date: '2024-07-20', amount: 22400,   status: 'Paid'    } },
      { id: 'r6', cells: { id: 'TRX-006', description: 'Sales Conference',         category: 'Marketing',      date: '2024-07-22', amount: 6800,    status: 'Review'  } },
      { id: 'r7', cells: { id: 'TRX-007', description: 'SaaS Subscriptions',       category: 'Software',       date: '2024-08-01', amount: 3200,    status: 'Paid'    } },
      { id: 'r8', cells: { id: 'TRX-008', description: 'Legal Retainer Q3',        category: 'Operations',     date: '2024-08-05', amount: 12000,   status: 'Paid'    } },
      { id: 'r9', cells: { id: 'TRX-009', description: 'Hardware Refresh',         category: 'Infrastructure', date: '2024-08-18', amount: 34600,   status: 'Pending' } },
      { id: 'r10', cells: { id: 'TRX-010', description: 'Contractor Invoices',     category: 'Operations',     date: '2024-09-01', amount: 28000,   status: 'Paid'    } },
      { id: 'r11', cells: { id: 'TRX-011', description: 'Product Design Assets',   category: 'Software',       date: '2024-09-10', amount: 4500,    status: 'Paid'    } },
      { id: 'r12', cells: { id: 'TRX-012', description: 'SEO & Content Agency',    category: 'Marketing',      date: '2024-09-14', amount: 9600,    status: 'Review'  } },
    ],
  },
  {
    id: 'sheet-2',
    name: 'Headcount',
    columns: [
      { id: 'name',       label: 'Name',       type: 'text',     width: 180 },
      { id: 'role',       label: 'Role',       type: 'text',     width: 200 },
      { id: 'department', label: 'Department', type: 'badge',    width: 140 },
      { id: 'start_date', label: 'Start Date', type: 'date',     width: 120 },
      { id: 'salary',     label: 'Salary',     type: 'currency', width: 130 },
      { id: 'status',     label: 'Status',     type: 'badge',    width: 110 },
    ],
    rows: [
      { id: 'r1', cells: { name: 'Arjun Mehta',    role: 'Engineering Lead',       department: 'Engineering', start_date: '2022-03-01', salary: 180000, status: 'Active'   } },
      { id: 'r2', cells: { name: 'Priya Sharma',   role: 'Product Manager',        department: 'Product',     start_date: '2022-06-15', salary: 160000, status: 'Active'   } },
      { id: 'r3', cells: { name: 'David Chen',     role: 'Senior Designer',        department: 'Design',      start_date: '2023-01-10', salary: 140000, status: 'Active'   } },
      { id: 'r4', cells: { name: 'Sara Williams',  role: 'Backend Engineer',       department: 'Engineering', start_date: '2023-04-01', salary: 155000, status: 'Active'   } },
      { id: 'r5', cells: { name: 'Mike Johnson',   role: 'Sales Director',         department: 'Sales',       start_date: '2021-09-01', salary: 200000, status: 'Active'   } },
      { id: 'r6', cells: { name: 'Alice Park',     role: 'Marketing Specialist',   department: 'Marketing',   start_date: '2023-07-01', salary: 95000,  status: 'Active'   } },
    ],
  },
  {
    id: 'sheet-3',
    name: 'KPIs',
    columns: [
      { id: 'metric',    label: 'Metric',    type: 'text',     width: 220 },
      { id: 'q1',        label: 'Q1',        type: 'number',   width: 110 },
      { id: 'q2',        label: 'Q2',        type: 'number',   width: 110 },
      { id: 'q3',        label: 'Q3',        type: 'number',   width: 110 },
      { id: 'target',    label: 'Target',    type: 'number',   width: 110 },
      { id: 'status',    label: 'Status',    type: 'badge',    width: 120 },
    ],
    rows: [
      { id: 'r1', cells: { metric: 'Monthly Recurring Revenue ($K)', q1: 420,  q2: 510,  q3: 640,  target: 600,  status: 'Achieved' } },
      { id: 'r2', cells: { metric: 'Customer Churn Rate (%)',         q1: 2.1,  q2: 1.8,  q3: 1.5,  target: 2.0,  status: 'Achieved' } },
      { id: 'r3', cells: { metric: 'New Logos',                       q1: 12,   q2: 18,   q3: 14,   target: 20,   status: 'At Risk'  } },
      { id: 'r4', cells: { metric: 'Net Promoter Score',              q1: 42,   q2: 46,   q3: 51,   target: 50,   status: 'Achieved' } },
      { id: 'r5', cells: { metric: 'Support Ticket SLA (%)',          q1: 94.2, q2: 96.1, q3: 97.4, target: 95.0, status: 'Achieved' } },
      { id: 'r6', cells: { metric: 'Employee Satisfaction',           q1: 3.8,  q2: 4.1,  q3: 4.0,  target: 4.2,  status: 'At Risk'  } },
    ],
  },
];

const BADGE_COLORS: Record<string, string> = {
  Infrastructure: 'bg-blue-100   text-blue-700   dark:bg-blue-900/30   dark:text-blue-400',
  Software:       'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400',
  Marketing:      'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400',
  Operations:     'bg-cyan-100   text-cyan-700   dark:bg-cyan-900/30   dark:text-cyan-400',
  Paid:           'bg-green-100  text-green-700  dark:bg-green-900/30  dark:text-green-400',
  Active:         'bg-green-100  text-green-700  dark:bg-green-900/30  dark:text-green-400',
  Achieved:       'bg-green-100  text-green-700  dark:bg-green-900/30  dark:text-green-400',
  Pending:        'bg-amber-100  text-amber-700  dark:bg-amber-900/30  dark:text-amber-400',
  'At Risk':      'bg-amber-100  text-amber-700  dark:bg-amber-900/30  dark:text-amber-400',
  Review:         'bg-amber-100  text-amber-700  dark:bg-amber-900/30  dark:text-amber-400',
  Engineering:    'bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-400',
  Product:        'bg-violet-100 text-violet-700 dark:bg-violet-900/30 dark:text-violet-400',
  Design:         'bg-pink-100   text-pink-700   dark:bg-pink-900/30   dark:text-pink-400',
  Sales:          'bg-teal-100   text-teal-700   dark:bg-teal-900/30   dark:text-teal-400',
};

function formatCurrency(value: CellValue): string {
  if (value === null || value === '') return '';
  const num = typeof value === 'number' ? value : parseFloat(String(value));
  if (isNaN(num)) return String(value);
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(num);
}

function formatNumber(value: CellValue): string {
  if (value === null || value === '') return '';
  const num = typeof value === 'number' ? value : parseFloat(String(value));
  if (isNaN(num)) return String(value);
  return new Intl.NumberFormat('en-US').format(num);
}

function CellDisplay({ col, value }: { col: Column; value: CellValue }) {
  if (value === null || value === undefined || value === '') {
    return <span className="text-content-muted">—</span>;
  }
  if (col.type === 'badge') {
    const cls = BADGE_COLORS[String(value)] ?? 'bg-surface-muted text-content-secondary';
    return <span className={`inline-flex items-center rounded px-2 py-0.5 text-xs font-medium ${cls}`}>{String(value)}</span>;
  }
  if (col.type === 'currency') return <span className="font-mono tabular-nums">{formatCurrency(value)}</span>;
  if (col.type === 'number') return <span className="font-mono tabular-nums">{formatNumber(value)}</span>;
  return <span>{String(value)}</span>;
}

interface EditingCell { rowId: string; colId: string }

export default function Sheets() {
  const [sheets, setSheets]           = useState<Sheet[]>(INITIAL_SHEETS);
  const [activeSheetId, setActiveSheetId] = useState(INITIAL_SHEETS[0].id);
  const [editing, setEditing]         = useState<EditingCell | null>(null);
  const [editValue, setEditValue]     = useState('');
  const [search, setSearch]           = useState('');
  const [selected, setSelected]       = useState<Set<string>>(new Set());
  const [aiPanel, setAiPanel]         = useState(false);
  const [aiQuery, setAiQuery]         = useState('');
  const [aiAnswer, setAiAnswer]       = useState('');
  const inputRef = useRef<HTMLInputElement>(null);
  const nextRowId = useRef(1000);

  const sheet = sheets.find(s => s.id === activeSheetId)!;

  const filteredRows = search.trim()
    ? sheet.rows.filter(row =>
        Object.values(row.cells).some(v =>
          String(v ?? '').toLowerCase().includes(search.toLowerCase())
        )
      )
    : sheet.rows;

  const startEdit = (rowId: string, colId: string, value: CellValue) => {
    setEditing({ rowId, colId });
    setEditValue(String(value ?? ''));
  };

  useEffect(() => {
    if (editing) inputRef.current?.focus();
  }, [editing]);

  const commitEdit = useCallback(() => {
    if (!editing) return;
    setSheets(prev => prev.map(s => {
      if (s.id !== activeSheetId) return s;
      return {
        ...s,
        rows: s.rows.map(r => {
          if (r.id !== editing.rowId) return r;
          const col = s.columns.find(c => c.id === editing.colId)!;
          let parsed: CellValue = editValue;
          if (col.type === 'number' || col.type === 'currency') {
            const n = parseFloat(editValue.replace(/[,$]/g, ''));
            parsed = isNaN(n) ? editValue : n;
          }
          return { ...r, cells: { ...r.cells, [editing.colId]: parsed } };
        }),
      };
    }));
    setEditing(null);
  }, [editing, editValue, activeSheetId]);

  const addRow = () => {
    const newId = `r${nextRowId.current}`;
    nextRowId.current += 1;
    const cells: Record<string, CellValue> = {};
    sheet.columns.forEach(c => { cells[c.id] = null; });
    if (sheet.columns.find(c => c.id === 'id')) {
      cells['id'] = `TRX-${String(sheet.rows.length + 1).padStart(3, '0')}`;
    }
    setSheets(prev => prev.map(s =>
      s.id === activeSheetId ? { ...s, rows: [...s.rows, { id: newId, cells }] } : s
    ));
  };

  const deleteSelected = () => {
    setSheets(prev => prev.map(s =>
      s.id !== activeSheetId ? s : { ...s, rows: s.rows.filter(r => !selected.has(r.id)) }
    ));
    setSelected(new Set());
  };

  const toggleSelect = (id: string) => {
    setSelected(prev => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const toggleSelectAll = () => {
    if (selected.size === filteredRows.length) {
      setSelected(new Set());
    } else {
      setSelected(new Set(filteredRows.map(r => r.id)));
    }
  };

  const exportCsv = () => {
    const header = sheet.columns.map(c => c.label).join(',');
    const rows = sheet.rows.map(r =>
      sheet.columns.map(c => {
        const v = r.cells[c.id];
        const s = String(v ?? '');
        return s.includes(',') ? `"${s}"` : s;
      }).join(',')
    );
    const csv = [header, ...rows].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = `${sheet.name}.csv`; a.click();
    URL.revokeObjectURL(url);
  };

  // Compute summary stats
  const currencyCols = sheet.columns.filter(c => c.type === 'currency');
  const summaryStats = currencyCols.map(col => {
    const total = sheet.rows.reduce((sum, r) => {
      const v = r.cells[col.id];
      return sum + (typeof v === 'number' ? v : 0);
    }, 0);
    return { label: `Total ${col.label}`, value: formatCurrency(total) };
  });
  const numberCols = sheet.columns.filter(c => c.type === 'number');
  numberCols.forEach(col => {
    const vals = sheet.rows.map(r => r.cells[col.id]).filter(v => typeof v === 'number') as number[];
    if (vals.length) {
      const avg = vals.reduce((a, b) => a + b, 0) / vals.length;
      summaryStats.push({ label: `Avg ${col.label}`, value: avg.toFixed(1) });
    }
  });

  const handleAiQuery = () => {
    if (!aiQuery.trim()) return;
    // Mock AI analysis
    setAiAnswer(
      `Based on the ${sheet.name} sheet with ${sheet.rows.length} records: ${summaryStats.map(s => `${s.label} is ${s.value}`).join(', ')}. ` +
      `The data shows ${sheet.rows.filter(r => r.cells['status'] === 'Pending' || r.cells['status'] === 'Review').length} items awaiting action. ` +
      `Consider reviewing pending items to improve cash flow efficiency.`
    );
  };

  return (
    <div className="flex flex-col h-full bg-surface-base">
      {/* Toolbar */}
      <header className="flex items-center justify-between border-b border-border-default px-4 py-2.5 bg-surface-base shrink-0 gap-3">
        <div className="flex items-center gap-2 min-w-0">
          <h2 className="text-content-primary text-base font-semibold truncate">{sheet.name}</h2>
          <span className="text-xs text-content-muted bg-surface-muted px-2 py-0.5 rounded">{sheet.rows.length} rows</span>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <div className="relative hidden sm:block">
            <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-content-muted" />
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="Search..."
              className="h-8 w-44 rounded-lg bg-surface-muted pl-8 pr-3 text-sm text-content-primary placeholder:text-content-muted focus:outline-none focus:ring-2 focus:ring-primary/40 border border-border-default"
            />
          </div>
          <button
            onClick={() => setAiPanel(p => !p)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary/10 text-primary hover:bg-primary/20 transition-colors text-xs font-semibold"
          >
            <Sparkles size={14} />
            AI Insights
          </button>
          {selected.size > 0 && (
            <button onClick={deleteSelected} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-danger-50 text-danger-600 hover:bg-danger-100 dark:bg-danger-900/20 dark:text-danger-400 transition-colors text-xs font-medium">
              <Trash2 size={14} />
              Delete ({selected.size})
            </button>
          )}
          <button onClick={exportCsv} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-border-default bg-surface-base hover:bg-surface-muted text-content-secondary text-xs font-medium transition-colors">
            <Download size={14} />
            Export
          </button>
          <button onClick={addRow} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary text-white hover:bg-primary/90 text-xs font-semibold transition-colors">
            <Plus size={14} />
            Add Row
          </button>
        </div>
      </header>

      {/* Sheet Tabs */}
      <div className="flex items-center gap-0 border-b border-border-default bg-surface-muted px-4 shrink-0 overflow-x-auto">
        {sheets.map(s => (
          <button
            key={s.id}
            onClick={() => { setActiveSheetId(s.id); setEditing(null); setSelected(new Set()); }}
            className={[
              'px-4 py-2 text-xs font-medium border-b-2 transition-colors whitespace-nowrap',
              activeSheetId === s.id
                ? 'border-primary text-primary bg-surface-base'
                : 'border-transparent text-content-secondary hover:text-content-primary hover:bg-surface-muted/60',
            ].join(' ')}
          >
            {s.name}
          </button>
        ))}
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Spreadsheet */}
        <div className="flex-1 overflow-auto">
          <table className="w-full border-collapse text-sm select-none">
            <thead className="sticky top-0 z-10 bg-surface-muted border-b border-border-default">
              <tr>
                {/* Row number + checkbox col */}
                <th className="w-10 px-2 py-2 text-center border-r border-border-subtle">
                  <input
                    type="checkbox"
                    checked={filteredRows.length > 0 && selected.size === filteredRows.length}
                    onChange={toggleSelectAll}
                    className="rounded border-border-strong accent-primary"
                  />
                </th>
                <th className="w-10 px-2 py-2 text-center text-xs text-content-muted font-normal border-r border-border-subtle">#</th>
                {sheet.columns.map(col => (
                  <th
                    key={col.id}
                    style={{ minWidth: col.width }}
                    className="px-3 py-2 text-left text-xs font-semibold text-content-muted uppercase tracking-wide border-r border-border-subtle last:border-r-0"
                  >
                    <div className="flex items-center gap-1">
                      {col.label}
                      <Filter size={10} className="text-content-muted/50" />
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filteredRows.map((row, rowIdx) => (
                <tr
                  key={row.id}
                  className={[
                    'group border-b border-border-subtle transition-colors',
                    selected.has(row.id) ? 'bg-primary/5 dark:bg-primary/10' : 'hover:bg-surface-muted/40',
                  ].join(' ')}
                >
                  <td className="w-10 px-2 py-1.5 text-center border-r border-border-subtle">
                    <input
                      type="checkbox"
                      checked={selected.has(row.id)}
                      onChange={() => toggleSelect(row.id)}
                      className="rounded border-border-strong accent-primary"
                    />
                  </td>
                  <td className="w-10 px-2 py-1.5 text-center text-xs text-content-muted border-r border-border-subtle">{rowIdx + 1}</td>
                  {sheet.columns.map(col => {
                    const isEditing = editing?.rowId === row.id && editing?.colId === col.id;
                    return (
                      <td
                        key={col.id}
                        style={{ minWidth: col.width }}
                        className="px-3 py-1.5 border-r border-border-subtle last:border-r-0 text-content-primary"
                        onDoubleClick={() => startEdit(row.id, col.id, row.cells[col.id])}
                      >
                        {isEditing ? (
                          <input
                            ref={inputRef}
                            value={editValue}
                            onChange={e => setEditValue(e.target.value)}
                            onBlur={commitEdit}
                            onKeyDown={e => { if (e.key === 'Enter') commitEdit(); if (e.key === 'Escape') setEditing(null); }}
                            className="w-full rounded border border-primary bg-surface-base px-1.5 py-0.5 text-sm text-content-primary outline-none focus:ring-1 focus:ring-primary/50"
                          />
                        ) : (
                          <CellDisplay col={col} value={row.cells[col.id]} />
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
              {filteredRows.length === 0 && (
                <tr>
                  <td colSpan={sheet.columns.length + 2} className="py-12 text-center text-sm text-content-muted">
                    {search ? 'No rows match your search.' : 'No rows yet. Click "Add Row" to get started.'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>

        {/* AI Panel */}
        {aiPanel && (
          <div className="w-72 shrink-0 border-l border-border-default bg-surface-base flex flex-col">
            <div className="flex items-center justify-between px-4 py-3 border-b border-border-default">
              <div className="flex items-center gap-2 text-sm font-semibold text-content-primary">
                <Sparkles size={14} className="text-primary" />
                Sheet Insights
              </div>
              <button onClick={() => setAiPanel(false)} className="text-content-muted hover:text-content-primary text-xs">✕</button>
            </div>
            {/* Summary stats */}
            <div className="p-4 border-b border-border-subtle space-y-2">
              {summaryStats.slice(0, 3).map((stat, i) => (
                <div key={i} className="flex items-center justify-between">
                  <span className="text-xs text-content-muted">{stat.label}</span>
                  <span className="text-sm font-bold text-content-primary">{stat.value}</span>
                </div>
              ))}
              <div className="flex items-center justify-between">
                <span className="text-xs text-content-muted">Total Rows</span>
                <span className="text-sm font-bold text-content-primary">{sheet.rows.length}</span>
              </div>
            </div>
            {/* AI Query */}
            <div className="flex-1 p-4 flex flex-col gap-3">
              <p className="text-xs text-content-muted">Ask a question about this sheet:</p>
              <textarea
                value={aiQuery}
                onChange={e => setAiQuery(e.target.value)}
                placeholder="e.g. What is the average spend per category?"
                className="w-full h-20 rounded-lg border border-border-default bg-surface-muted px-3 py-2 text-xs text-content-primary placeholder:text-content-muted resize-none focus:outline-none focus:ring-2 focus:ring-primary/40"
              />
              <button
                onClick={handleAiQuery}
                disabled={!aiQuery.trim()}
                className="w-full flex items-center justify-center gap-2 rounded-lg bg-primary px-3 py-2 text-xs font-semibold text-white hover:bg-primary/90 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
              >
                <Sparkles size={12} />
                Analyze
              </button>
              {aiAnswer && (
                <div className="rounded-lg border border-primary/20 bg-primary/5 p-3 text-xs text-content-primary leading-relaxed">
                  {aiAnswer}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Status bar */}
      <div className="flex items-center gap-4 border-t border-border-default bg-surface-muted px-4 py-1.5 text-xs text-content-muted shrink-0">
        <span>{sheet.rows.length} rows · {sheet.columns.length} columns</span>
        {selected.size > 0 && <span className="text-primary">{selected.size} selected</span>}
        {search && <span>Showing {filteredRows.length} of {sheet.rows.length}</span>}
        <span className="ml-auto">Double-click to edit</span>
      </div>
    </div>
  );
}
