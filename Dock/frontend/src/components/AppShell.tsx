import { useState } from 'react'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import {
  Sidebar,
  ThemeToggle,
} from '@orbit-ui/react'
import {
  LayoutGrid,
  User,
  FileKey,
  UserCheck,
  ClipboardList,
  ScrollText,
  Package,
  Menu,
  X,
} from 'lucide-react'

const navItems = [
  { label: 'Catalog', icon: <LayoutGrid />, path: '/catalog' },
  { label: 'My Apps', icon: <User />, path: '/my-apps' },
  { label: 'Licenses', icon: <FileKey />, path: '/licenses' },
  { label: 'Assignments', icon: <UserCheck />, path: '/assignments' },
  { label: 'Requests', icon: <ClipboardList />, path: '/requests' },
  { label: 'Audit Log', icon: <ScrollText />, path: '/audit' },
]

export default function AppShell() {
  const location = useLocation()
  const navigate = useNavigate()
  const [mobileOpen, setMobileOpen] = useState(false)

  const currentPath = '/' + location.pathname.split('/')[1]

  return (
    <div className="flex h-screen bg-surface-base overflow-hidden">
      {/* Mobile overlay */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-40 bg-surface-overlay md:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* Mobile sidebar */}
      <div
        className={`fixed inset-y-0 left-0 z-50 md:hidden transition-transform duration-300 ${
          mobileOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <Sidebar collapsible={false} width="240px" className="h-full">
          <Sidebar.Header>
            <div className="flex items-center gap-2 min-w-0">
              <Package className="size-5 text-primary-500 shrink-0" />
              <span className="font-semibold text-content-primary text-sm truncate">
                RM Dock
              </span>
            </div>
            <button
              onClick={() => setMobileOpen(false)}
              className="ml-auto text-content-muted hover:text-content-primary"
            >
              <X className="size-5" />
            </button>
          </Sidebar.Header>

          <Sidebar.Content>
            <Sidebar.Section>
              {navItems.map((item) => (
                <Sidebar.Item
                  key={item.path}
                  icon={item.icon}
                  label={item.label}
                  active={currentPath === item.path}
                  onClick={() => {
                    navigate(item.path)
                    setMobileOpen(false)
                  }}
                />
              ))}
            </Sidebar.Section>
          </Sidebar.Content>

          <Sidebar.Footer>
            <div className="flex items-center justify-between px-2 py-1">
              <span className="text-xs text-content-muted">Theme</span>
              <ThemeToggle size="sm" />
            </div>
          </Sidebar.Footer>
        </Sidebar>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden md:flex h-full">
        <Sidebar collapsible width="240px" className="h-full">
          <Sidebar.Header>
            <Package className="size-5 text-primary-500 shrink-0" />
            <span className="font-semibold text-content-primary text-sm truncate">
              RM Dock
            </span>
          </Sidebar.Header>

          <Sidebar.Content>
            <Sidebar.Section>
              {navItems.map((item) => (
                <Sidebar.Item
                  key={item.path}
                  icon={item.icon}
                  label={item.label}
                  active={currentPath === item.path}
                  onClick={() => navigate(item.path)}
                />
              ))}
            </Sidebar.Section>
          </Sidebar.Content>

          <Sidebar.Footer>
            <div className="flex items-center justify-between px-2 py-1">
              <span className="text-xs text-content-muted">Theme</span>
              <ThemeToggle size="sm" />
            </div>
          </Sidebar.Footer>
        </Sidebar>
      </div>

      {/* Main content */}
      <div className="flex flex-1 flex-col min-w-0 overflow-hidden">
        {/* Mobile topbar */}
        <div className="md:hidden flex items-center gap-3 px-4 py-3 border-b border-border-default bg-surface-base shrink-0">
          <button
            onClick={() => setMobileOpen(true)}
            className="text-content-muted hover:text-content-primary"
          >
            <Menu className="size-5" />
          </button>
          <Package className="size-5 text-primary-500" />
          <span className="font-semibold text-content-primary text-sm">RM Dock</span>
        </div>

        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
