import { useState, useMemo } from 'react'
import { Outlet, Link, useLocation } from 'react-router-dom'
import { Lock, KeyRound, Globe, ScrollText, Menu, X } from 'lucide-react'
import { ThemeToggle } from '@orbit-ui/react'

const navItems = [
  { name: 'Secrets', href: '/secrets', icon: KeyRound },
  { name: 'Shared Info', href: '/shared-info', icon: Globe },
  { name: 'Audit Log', href: '/audit', icon: ScrollText },
]

export default function AppShell() {
  const [mobileOpen, setMobileOpen] = useState(false)
  const location = useLocation()

  const activeNav = useMemo(
    () =>
      navItems.find(
        (item) =>
          location.pathname === item.href ||
          location.pathname.startsWith(`${item.href}/`),
      ) ?? navItems[0],
    [location.pathname],
  )

  return (
    <div className="flex min-h-screen relative bg-surface-base">
      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-40 lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed inset-y-0 left-0 z-50 w-64 flex flex-col bg-surface-base border-r border-border-default transition-transform duration-300 lg:relative lg:translate-x-0 ${
          mobileOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand */}
        <div className="flex items-center justify-between gap-3 px-4 py-4 border-b border-border-default">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center shadow-sm">
              <Lock size={16} className="text-white" />
            </div>
            <div>
              <p className="font-bold text-sm text-content-primary leading-none">RM Wallet</p>
              <p className="text-[11px] text-content-muted mt-0.5">Secrets Vault</p>
            </div>
          </div>
          <button
            onClick={() => setMobileOpen(false)}
            className="lg:hidden p-1.5 text-content-muted hover:text-content-primary hover:bg-surface-muted rounded-md"
          >
            <X size={18} />
          </button>
        </div>

        {/* Nav */}
        <nav className="flex-1 px-2 py-3 space-y-0.5 overflow-y-auto">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive =
              location.pathname === item.href ||
              location.pathname.startsWith(`${item.href}/`)
            return (
              <Link
                key={item.href}
                to={item.href}
                onClick={() => setMobileOpen(false)}
                className={`flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-100 ${
                  isActive
                    ? 'bg-primary-50 text-primary-700 dark:bg-primary-950 dark:text-primary-300'
                    : 'text-content-secondary hover:bg-surface-muted hover:text-content-primary'
                }`}
              >
                <Icon
                  size={17}
                  className={isActive ? 'text-primary-600 dark:text-primary-400' : ''}
                />
                <span>{item.name}</span>
              </Link>
            )
          })}
        </nav>

        {/* Footer */}
        <div className="px-4 py-3 border-t border-border-subtle">
          <p className="text-[11px] text-content-muted">
            All values encrypted at rest
          </p>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col min-h-screen min-w-0">
        {/* Header */}
        <header className="h-14 bg-surface-base border-b border-border-default flex items-center justify-between px-4 lg:px-6 shrink-0">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setMobileOpen(true)}
              className="lg:hidden p-1.5 -ml-1.5 text-content-muted hover:bg-surface-muted rounded-lg"
            >
              <Menu size={20} />
            </button>
            <p className="text-sm font-semibold text-content-primary">{activeNav.name}</p>
          </div>

          <div className="flex items-center gap-2">
            <ThemeToggle size="sm" />
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-auto p-4 md:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
