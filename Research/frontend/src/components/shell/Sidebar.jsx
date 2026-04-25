import { NavLink } from 'react-router-dom'
import { FileText, Settings, FlaskConical } from 'lucide-react'
import BrainStatus from '../BrainStatus'

export default function Sidebar() {
  return (
    <aside className="w-[240px] shrink-0 bg-sidebar border-r border-border flex flex-col">
      {/* Brand block */}
      <div className="px-5 py-4 border-b border-border flex items-center gap-3">
        <div className="w-8 h-8 rounded-lg bg-accent/15 border border-accent/30 flex items-center justify-center">
          <FlaskConical size={16} className="text-accent" />
        </div>
        <div>
          <p className="text-[13px] font-bold text-text">Research</p>
          <p className="text-[9px] text-muted uppercase tracking-wider">RM ORBIT</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-1">
        <NavLink
          to="/papers"
          className={({ isActive }) =>
            `flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-[13px] font-medium transition-all ${
              isActive
                ? 'bg-accent/10 text-accent border-l-2 border-accent'
                : 'text-muted hover:text-text hover:bg-raised/60'
            }`
          }
        >
          <FileText size={16} />
          Papers
        </NavLink>

        <NavLink
          to="/system"
          className={({ isActive }) =>
            `flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-[13px] font-medium transition-all ${
              isActive
                ? 'bg-accent/10 text-accent border-l-2 border-accent'
                : 'text-muted hover:text-text hover:bg-raised/60'
            }`
          }
        >
          <Settings size={16} />
          System
        </NavLink>
      </nav>

      {/* Brain status footer */}
      <div className="px-4 py-4 border-t border-border">
        <BrainStatus />
      </div>
    </aside>
  )
}
