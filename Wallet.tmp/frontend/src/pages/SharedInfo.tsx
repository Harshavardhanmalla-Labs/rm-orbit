import { useState, useEffect, useCallback } from 'react'
import { Eye, EyeOff, Info } from 'lucide-react'
import { Badge, Input, Select, Skeleton, useToast } from '@orbit-ui/react'
import { sharedInfoApi, type SharedInfo } from '../api/wallet'
import { formatRelativeTime } from '../lib/utils'

type BadgeColor = 'primary' | 'warning' | 'info' | 'success' | 'neutral'

const CATEGORY_BADGE: Record<string, BadgeColor> = {
  domain: 'primary',
  cloudflare: 'warning',
  misc: 'neutral',
}

export default function SharedInfoPage() {
  const { toast } = useToast()
  const [items, setItems] = useState<SharedInfo[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('')
  const [revealed, setRevealed] = useState<Set<string>>(new Set())

  const fetchItems = useCallback(async () => {
    setLoading(true)
    try {
      const res = await sharedInfoApi.list({
        search: search || undefined,
        category: category || undefined,
      })
      setItems(res.data)
    } catch {
      toast({ variant: 'error', title: 'Failed to load shared info' })
    } finally {
      setLoading(false)
    }
  }, [search, category, toast])

  useEffect(() => {
    void fetchItems()
  }, [fetchItems])

  const toggleReveal = (id: string) => {
    setRevealed((prev) => {
      const next = new Set(prev)
      if (next.has(id)) {
        next.delete(id)
      } else {
        next.add(id)
      }
      return next
    })
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-bold text-content-primary">Shared Info</h1>
        <p className="text-sm text-content-muted mt-0.5">
          Organizational shared information registry
        </p>
      </div>

      {/* Info banner */}
      <div className="flex items-start gap-2.5 p-3.5 rounded-xl bg-info-50 dark:bg-info-950 border border-info-200 dark:border-info-800">
        <Info size={16} className="text-info-600 dark:text-info-400 mt-0.5 shrink-0" />
        <p className="text-sm text-info-700 dark:text-info-300">
          This is a read-only registry of shared organizational information.
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="flex-1">
          <Input
            placeholder="Search shared info..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div className="w-full sm:w-48">
          <Select value={category} onChange={(e) => setCategory(e.target.value)}>
            <option value="">All Categories</option>
            <option value="domain">Domain</option>
            <option value="cloudflare">Cloudflare</option>
            <option value="misc">Misc</option>
          </Select>
        </div>
      </div>

      {/* Table */}
      <div className="bg-surface-elevated border border-border-default rounded-xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border-subtle bg-surface-muted/50">
                <th className="text-left px-4 py-3 font-semibold text-content-secondary text-xs uppercase tracking-wide">
                  Title
                </th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary text-xs uppercase tracking-wide">
                  Category
                </th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary text-xs uppercase tracking-wide">
                  Value
                </th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary text-xs uppercase tracking-wide hidden md:table-cell">
                  Environment
                </th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary text-xs uppercase tracking-wide hidden lg:table-cell">
                  Owner Team
                </th>
                <th className="text-left px-4 py-3 font-semibold text-content-secondary text-xs uppercase tracking-wide hidden sm:table-cell">
                  Updated
                </th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                Array.from({ length: 4 }).map((_, i) => (
                  <tr key={i} className="border-b border-border-subtle last:border-0">
                    <td className="px-4 py-3"><Skeleton className="h-4 w-36" /></td>
                    <td className="px-4 py-3"><Skeleton className="h-5 w-20" /></td>
                    <td className="px-4 py-3"><Skeleton className="h-4 w-32" /></td>
                    <td className="px-4 py-3 hidden md:table-cell"><Skeleton className="h-5 w-20" /></td>
                    <td className="px-4 py-3 hidden lg:table-cell"><Skeleton className="h-4 w-24" /></td>
                    <td className="px-4 py-3 hidden sm:table-cell"><Skeleton className="h-4 w-20" /></td>
                  </tr>
                ))
              ) : items.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-4 py-12 text-center text-content-muted text-sm">
                    No shared info found.
                  </td>
                </tr>
              ) : (
                items.map((item) => {
                  const isRevealed = revealed.has(item.id)
                  return (
                    <tr
                      key={item.id}
                      className="border-b border-border-subtle last:border-0 hover:bg-surface-muted/40 transition-colors"
                    >
                      <td className="px-4 py-3">
                        <p className="font-medium text-content-primary">{item.title}</p>
                      </td>
                      <td className="px-4 py-3">
                        <Badge
                          color={CATEGORY_BADGE[item.category] ?? 'neutral'}
                          variant="subtle"
                        >
                          {item.category}
                        </Badge>
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-sm text-content-primary">
                            {isRevealed ? item.value : '••••••••'}
                          </span>
                          <button
                            onClick={() => toggleReveal(item.id)}
                            className="text-content-muted hover:text-content-primary transition-colors"
                            aria-label={isRevealed ? 'Hide value' : 'Show value'}
                          >
                            {isRevealed ? <EyeOff size={14} /> : <Eye size={14} />}
                          </button>
                        </div>
                      </td>
                      <td className="px-4 py-3 hidden md:table-cell">
                        {item.environment ? (
                          <Badge color="info" variant="outline" size="sm">
                            {item.environment}
                          </Badge>
                        ) : (
                          <span className="text-content-muted text-xs">—</span>
                        )}
                      </td>
                      <td className="px-4 py-3 hidden lg:table-cell">
                        <span className="text-content-secondary text-sm">
                          {item.owner_team ?? <span className="text-content-muted">—</span>}
                        </span>
                      </td>
                      <td className="px-4 py-3 hidden sm:table-cell">
                        <span className="text-xs text-content-muted">
                          {formatRelativeTime(item.updated_at)}
                        </span>
                      </td>
                    </tr>
                  )
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
