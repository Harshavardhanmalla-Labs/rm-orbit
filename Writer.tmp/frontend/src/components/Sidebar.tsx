import { Link, useLocation } from 'react-router-dom';
import { ThemeToggle } from '@orbit-ui/react';

const NavButton = ({ to, icon, label, exact = false, onClick }: { to: string, icon: string, label: string, exact?: boolean, onClick?: () => void }) => {
    const location = useLocation();
    const isActive = exact ? location.pathname === to : location.pathname.startsWith(to);
    const baseClasses = "flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all group";
    const activeClasses = "bg-surface-base border border-border-default shadow-sm text-primary";
    const inactiveClasses = "hover:bg-surface-base hover:shadow-sm text-content-secondary hover:text-content-primary";

    return (
        <Link to={to} onClick={onClick} className={`${baseClasses} ${isActive ? activeClasses : inactiveClasses}`}>
            <span className={`material-symbols-outlined transition-colors ${isActive ? 'text-primary' : 'text-slate-400 group-hover:text-primary'}`}>{icon}</span>
            <span className="text-sm font-medium">{label}</span>
        </Link>
    );
};

export const Sidebar = ({ mobileOpen, setMobileOpen }: { mobileOpen: boolean, setMobileOpen: (open: boolean) => void }) => (
    <>
        {/* Mobile Overlay */}
        {mobileOpen && (
            <div 
                className="fixed inset-0 bg-black/40 z-40 lg:hidden"
                onClick={() => setMobileOpen(false)}
            />
        )}
        
        {/* Sidebar Container */}
        <div className={`fixed inset-y-0 left-0 z-50 flex w-64 flex-col border-r border-border-default bg-surface-base py-4 px-3 flex-shrink-0 h-screen overflow-y-auto transition-transform duration-300 transform lg:relative lg:translate-x-0 ${mobileOpen ? 'translate-x-0' : '-translate-x-full'}`}>
            <div className="flex items-center gap-3 px-2 mb-8 mt-2 justify-between">
                <div className="flex items-center gap-3">
                    <div className="flex items-center justify-center size-10 rounded-lg bg-primary text-white shadow-md shadow-primary/20">
                        <span className="material-symbols-outlined text-2xl">draw</span>
                    </div>
                    <div className="flex flex-col">
                        <h1 className="text-content-primary text-base font-bold leading-tight">RM Writer</h1>
                        <p className="text-content-muted text-xs font-medium">Enterprise</p>
                    </div>
                </div>
                <button
                  onClick={() => setMobileOpen(false)}
                  className="lg:hidden p-1 text-content-muted hover:text-content-primary rounded-md"
                >
                  <span className="material-symbols-outlined text-lg">close</span>
                </button>
            </div>
            <nav className="flex flex-col gap-1 flex-1">
                <NavButton to="/" icon="dashboard" label="Dashboard" exact onClick={() => setMobileOpen(false)} />
                <NavButton to="/document" icon="description" label="Document View" onClick={() => setMobileOpen(false)} />
                <NavButton to="/split-view" icon="vertical_split" label="Split Editor" onClick={() => setMobileOpen(false)} />
                <NavButton to="/collab" icon="group_work" label="Real-time Collab" onClick={() => setMobileOpen(false)} />
                <NavButton to="/sheets" icon="table_chart" label="Sheets Data" onClick={() => setMobileOpen(false)} />
                <NavButton to="/slides" icon="slideshow" label="Presentation" onClick={() => setMobileOpen(false)} />
                <NavButton to="/infinite-canvas" icon="gesture" label="Infinite Canvas" onClick={() => setMobileOpen(false)} />
                <NavButton to="/lasso" icon="arrow_selector_tool" label="AI Lasso" onClick={() => setMobileOpen(false)} />
                <NavButton to="/graph" icon="hub" label="Knowledge Graph" onClick={() => setMobileOpen(false)} />
                <NavButton to="/workflow" icon="memory" label="AI Studio" onClick={() => setMobileOpen(false)} />
                <NavButton to="/templates" icon="grid_view" label="Templates" onClick={() => setMobileOpen(false)} />
                <NavButton to="/history" icon="history" label="Version History" onClick={() => setMobileOpen(false)} />
                <NavButton to="/admin" icon="admin_panel_settings" label="Admin" onClick={() => setMobileOpen(false)} />
            </nav>
            <div className="mt-auto pt-4 border-t border-border-subtle space-y-1">
                <div className="flex items-center justify-between px-3 py-1.5">
                  <span className="text-xs text-content-muted">Theme</span>
                  <ThemeToggle size="sm" />
                </div>
                <Link to="/command" onClick={() => setMobileOpen(false)} className="flex items-center gap-3 px-3 py-2 text-sm text-content-muted hover:text-primary transition-colors">
                <span className="material-symbols-outlined">search</span> AI Command
                </Link>
                <Link to="/export" onClick={() => setMobileOpen(false)} className="flex items-center gap-3 px-3 py-2 text-sm text-content-muted hover:text-primary transition-colors">
                <span className="material-symbols-outlined">ios_share</span> Export Dialog
                </Link>
            </div>
        </div>
    </>
);
