import { Outlet, NavLink, useMatch } from 'react-router-dom'
import { FlaskConical, FileText, Plus, Settings, UploadCloud, Cpu, Eye, Download } from 'lucide-react'
import BrainStatus from './BrainStatus.jsx'

const PAPER_STEPS = [
  { key: 'upload',   label: 'Upload',   Icon: UploadCloud },
  { key: 'pipeline', label: 'Pipeline', Icon: Cpu },
  { key: 'preview',  label: 'Preview',  Icon: Eye },
  { key: 'export',   label: 'Export',   Icon: Download },
]

export default function Layout() {
  const paperMatch = useMatch('/paper/:paperId/:step')
  const paperId = paperMatch?.params?.paperId
  const currentStep = paperMatch?.params?.step

  return (
    <div className="flex min-h-screen bg-bg">
      {/* Sidebar */}
      <aside className="w-[220px] shrink-0 sticky top-0 h-screen flex flex-col bg-sidebar border-r border-border overflow-y-auto">
        {/* Logo */}
        <div className="px-4 py-5 border-b border-border">
          <NavLink to="/papers" className="flex items-center gap-2.5 no-underline group">
            <div className="w-8 h-8 rounded-xl bg-accent flex items-center justify-center shrink-0 group-hover:bg-accent-hover transition-colors">
              <FlaskConical size={15} color="white" />
            </div>
            <div>
              <p className="text-[13px] font-bold text-text leading-none">Research</p>
              <p className="text-[10px] text-muted tracking-widest mt-0.5">RM ORBIT</p>
            </div>
          </NavLink>
        </div>

        {/* Nav */}
        <nav className="flex-1 px-2 py-3 flex flex-col gap-0.5">
          {/* New Paper */}
          <NavLink to="/new" className="btn btn-primary w-full justify-center mb-3 py-2 text-[13px]">
            <Plus size={14} /> New Paper
          </NavLink>

          <NavItem to="/papers" Icon={FileText} label="Papers" />

          {/* Paper workflow */}
          {paperId && (
            <div className="mt-4">
              <p className="section-title px-3">Current Paper</p>
              {PAPER_STEPS.map(s => (
                <NavItem
                  key={s.key}
                  to={`/paper/${paperId}/${s.key}`}
                  Icon={s.Icon}
                  label={s.label}
                  active={currentStep === s.key}
                  sub
                />
              ))}
            </div>
          )}

          <div className="mt-auto pt-4 border-t border-border">
            <NavItem to="/system" Icon={Settings} label="System" />
          </div>
        </nav>

        {/* Brain status */}
        <div className="px-4 py-3 border-t border-border">
          <BrainStatus compact />
        </div>
      </aside>

      {/* Content */}
      <main className="flex-1 min-w-0 overflow-x-hidden">
        <Outlet />
      </main>
    </div>
  )
}

function NavItem({ to, Icon, label, active, sub }) {
  return (
    <NavLink
      to={to}
      className={({ isActive }) => [
        'flex items-center gap-2.5 px-3 py-2 rounded-xl text-[13px] font-medium no-underline transition-all',
        sub ? 'pl-5 text-[12px]' : '',
        isActive || active
          ? 'bg-accent/10 text-accent border-l-2 border-accent pl-[10px]'
          : 'text-muted hover:text-text hover:bg-raised border-l-2 border-transparent',
      ].join(' ')}
    >
      <Icon size={sub ? 13 : 14} />
      {label}
    </NavLink>
  )
}
