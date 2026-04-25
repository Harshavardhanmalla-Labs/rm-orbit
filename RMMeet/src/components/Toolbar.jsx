/**
 * Toolbar.jsx — Fixed bottom-center pill with mic, camera, and leave controls.
 * Uses inline SVGs — no icon library dependency.
 */

// ── SVG icons ────────────────────────────────────────────────────────────────

function IconMic() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <rect x="9" y="2" width="6" height="12" rx="3" />
      <path d="M5 10a7 7 0 0 0 14 0" />
      <line x1="12" y1="19" x2="12" y2="22" />
      <line x1="9" y1="22" x2="15" y2="22" />
    </svg>
  );
}

function IconMicOff() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="2" y1="2" x2="22" y2="22" />
      <path d="M18.89 13.23A7.12 7.12 0 0 0 19 12" />
      <path d="M5 10a7 7 0 0 0 12.66 3.76" />
      <path d="M15 9.34V4a3 3 0 0 0-5.68-1.33" />
      <rect x="9" y="2" width="6" height="8" rx="3" clipPath="inset(0 0 0 100%)" />
      <path d="M9 9v3a3 3 0 0 0 5.12 2.12" />
      <line x1="12" y1="19" x2="12" y2="22" />
      <line x1="9" y1="22" x2="15" y2="22" />
    </svg>
  );
}

function IconCamera() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" />
      <circle cx="12" cy="13" r="3" />
    </svg>
  );
}

function IconCameraOff() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="2" y1="2" x2="22" y2="22" />
      <path d="M7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16" />
      <path d="M9.5 4h5L17 7h3a2 2 0 0 1 2 2v7.5" />
      <path d="M14.121 15.121A3 3 0 1 1 9.88 10.88" />
    </svg>
  );
}

function IconHangUp() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
      <path d="M6.6 10.8c1.4 2.8 3.8 5.1 6.6 6.6l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02L6.6 10.8z"/>
    </svg>
  );
}

// ── Component ─────────────────────────────────────────────────────────────────

export default function Toolbar({ isMuted, isCameraOff, onToggleMic, onToggleCamera, onLeave }) {
  return (
    <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50">
      <div
        className="flex items-center gap-2 px-4 py-3 rounded-full shadow-2xl"
        style={{
          background: 'rgba(30, 30, 30, 0.92)',
          backdropFilter: 'blur(16px)',
          WebkitBackdropFilter: 'blur(16px)',
          border: '1px solid rgba(255,255,255,0.08)',
        }}
      >
        {/* Mic toggle */}
        <ToolbarButton
          onClick={onToggleMic}
          active={!isMuted}
          label={isMuted ? 'Unmute' : 'Mute'}
          danger={isMuted}
        >
          {isMuted ? <IconMicOff /> : <IconMic />}
        </ToolbarButton>

        {/* Camera toggle */}
        <ToolbarButton
          onClick={onToggleCamera}
          active={!isCameraOff}
          label={isCameraOff ? 'Turn camera on' : 'Turn camera off'}
          danger={isCameraOff}
        >
          {isCameraOff ? <IconCameraOff /> : <IconCamera />}
        </ToolbarButton>

        {/* Divider */}
        <div className="w-px h-8 bg-white/10 mx-1" />

        {/* Leave */}
        <button
          onClick={onLeave}
          aria-label="Leave meeting"
          title="Leave meeting"
          className="flex items-center justify-center w-12 h-12 rounded-full text-white cursor-pointer"
          style={{ background: '#dc2626' }}
          onMouseEnter={(e) => (e.currentTarget.style.background = '#b91c1c')}
          onMouseLeave={(e) => (e.currentTarget.style.background = '#dc2626')}
        >
          <IconHangUp />
        </button>
      </div>
    </div>
  );
}

function ToolbarButton({ onClick, active, label, danger, children }) {
  const bg = active
    ? 'rgba(99,102,241,0.15)'
    : danger
    ? 'rgba(220,38,38,0.2)'
    : 'rgba(255,255,255,0.06)';

  const color = active ? '#a5b4fc' : danger ? '#fca5a5' : '#a1a1aa';

  return (
    <button
      onClick={onClick}
      aria-label={label}
      title={label}
      className="flex items-center justify-center w-12 h-12 rounded-full cursor-pointer transition-colors"
      style={{ background: bg, color }}
      onMouseEnter={(e) => {
        e.currentTarget.style.background = active
          ? 'rgba(99,102,241,0.25)'
          : danger
          ? 'rgba(220,38,38,0.35)'
          : 'rgba(255,255,255,0.12)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.background = bg;
      }}
    >
      {children}
    </button>
  );
}
