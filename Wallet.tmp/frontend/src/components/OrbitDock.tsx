import { useState, useRef, useEffect } from 'react';

const APPS = [
  { id: 'calendar', label: 'Calendar', icon: 'calendar_today', url: 'https://calendar.freedomlabs.in' },
  { id: 'meet', label: 'Meet', icon: 'videocam', url: 'https://meet.freedomlabs.in' },
  { id: 'mail', label: 'Mail', icon: 'mail', url: 'https://mail.freedomlabs.in' },
  { id: 'connect', label: 'Connect', icon: 'chat', url: 'https://chat.freedomlabs.in' },
  { id: 'planet', label: 'Planet CRM', icon: 'public', url: 'https://planet.freedomlabs.in' },
  { id: 'writer', label: 'Writer', icon: 'edit_document', url: 'https://docs.freedomlabs.in' },
  { id: 'atlas', label: 'Atlas', icon: 'hub', url: 'https://atlas.freedomlabs.in' },
  { id: 'turbotick', label: 'TurboTick', icon: 'confirmation_number', url: 'https://turbotick.freedomlabs.in' },
  { id: 'learn', label: 'Learn', icon: 'school', url: 'https://learn.freedomlabs.in' },
  { id: 'secure', label: 'Secure', icon: 'shield', url: 'https://secure.freedomlabs.in' },
  { id: 'capital-hub', label: 'Capital Hub', icon: 'account_balance', url: 'https://capital.freedomlabs.in' },
  { id: 'fitterme', label: 'FitterMe', icon: 'fitness_center', url: 'https://ecosystem.freedomlabs.in' },
  { id: 'scribe', label: 'Scribe', icon: 'auto_stories', url: 'https://scribe.freedomlabs.in' },
  { id: 'wallet', label: 'Wallet', icon: 'account_balance_wallet', url: 'https://wallet.freedomlabs.in' },
  { id: 'dock', label: 'Dock', icon: 'apps', url: 'https://dock.freedomlabs.in' },
  { id: 'search', label: 'Search', icon: 'search', url: 'https://search.freedomlabs.in' },
  { id: 'control-center', label: 'Settings', icon: 'settings', url: 'https://center.freedomlabs.in' },
];

const ACTIVE_APP = 'wallet';

const OrbitDock: React.FC = () => {
  const [visible, setVisible] = useState(false);
  const [hoveredApp, setHoveredApp] = useState<string | null>(null);
  const hideTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => { if (hideTimer.current) clearTimeout(hideTimer.current); };
  }, []);

  const scheduleHide = () => {
    if (hideTimer.current) clearTimeout(hideTimer.current);
    hideTimer.current = setTimeout(() => {
      setVisible(false);
      setHoveredApp(null);
    }, 500);
  };

  const cancelHide = () => {
    if (hideTimer.current) { clearTimeout(hideTimer.current); hideTimer.current = null; }
  };

  return (
    <>
      {/* Invisible hover trigger on right edge */}
      <div
        className="fixed right-0 top-0 w-[6px] h-full z-[9998]"
        onMouseEnter={() => { cancelHide(); setVisible(true); }}
      />

      {/* Dock container */}
      <div
        onMouseEnter={() => { cancelHide(); setVisible(true); }}
        onMouseLeave={scheduleHide}
        style={{
          transform: visible ? 'translateX(0)' : 'translateX(calc(100% + 8px))',
          opacity: visible ? 1 : 0,
          transition: 'transform 0.25s cubic-bezier(0.4,0,0.2,1), opacity 0.2s ease',
        }}
        className="fixed right-2 top-0 h-full flex items-center z-[9999]"
      >
        <div className="flex flex-col items-center gap-[3px] bg-white/80 dark:bg-slate-900/90 backdrop-blur-xl border border-slate-200/50 dark:border-slate-700/50 rounded-2xl py-2.5 px-[5px] shadow-2xl shadow-black/8">
          {APPS.map((app) => {
            const isActive = app.id === ACTIVE_APP;
            return (
              <button
                key={app.id}
                onClick={() => {
                  if (!isActive) window.open(app.url, '_blank');
                }}
                onMouseEnter={() => setHoveredApp(app.id)}
                onMouseLeave={() => setHoveredApp(null)}
                className={`relative w-9 h-9 rounded-[10px] flex items-center justify-center transition-all duration-150 ${
                  hoveredApp === app.id ? 'scale-[1.35]' : ''
                } ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                    : 'text-slate-500 dark:text-slate-400 hover:text-blue-600 hover:bg-slate-100 dark:hover:bg-slate-800'
                }`}
              >
                <span className="material-symbols-outlined text-[18px]">{app.icon}</span>
                {isActive && (
                  <span className="absolute -left-[5px] top-1/2 -translate-y-1/2 w-[3px] h-[3px] rounded-full bg-sky-400 shadow-[0_0_6px_rgba(56,189,248,0.8)]" />
                )}
                {hoveredApp === app.id && (
                  <div className="absolute right-full mr-3 top-1/2 -translate-y-1/2 px-2.5 py-1.5 bg-slate-800 dark:bg-white text-white dark:text-slate-800 text-[11px] font-medium rounded-lg whitespace-nowrap shadow-lg pointer-events-none">
                    {app.label}
                  </div>
                )}
              </button>
            );
          })}
        </div>
      </div>
    </>
  );
};

export default OrbitDock;
