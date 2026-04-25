/**
 * RoomPage.jsx — Live meeting room.
 *
 * Flow:
 *   1. Read displayName from location state (set by JoinPage). If missing,
 *      redirect back to /join/:roomId so the user enters their name.
 *   2. Call POST /api/guest/session → get { token, user }.
 *   3. Pass token + roomId + displayName to useWebRTC hook.
 *   4. Render video grid + local video PIP + Toolbar.
 *
 * The useWebRTC hook owns all Socket.IO and RTCPeerConnection lifecycle.
 */

import { useEffect, useState, useCallback, useRef } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { createGuestSession } from '../api.js';
import { useWebRTC } from '../hooks/useWebRTC.js';
import VideoTile from '../components/VideoTile.jsx';
import Toolbar from '../components/Toolbar.jsx';

// ── Loading / error states ────────────────────────────────────────────────────

function Spinner() {
  return (
    <div className="flex flex-col items-center gap-4">
      <div
        className="w-10 h-10 rounded-full border-2 border-indigo-500 border-t-transparent animate-spin"
      />
      <p className="text-zinc-400 text-sm">Connecting…</p>
    </div>
  );
}

function FatalError({ message, onRetry, onHome }) {
  return (
    <div className="flex flex-col items-center gap-4 text-center max-w-sm px-4">
      <div
        className="w-12 h-12 rounded-full flex items-center justify-center"
        style={{ background: 'rgba(220,38,38,0.15)' }}
      >
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ef4444" strokeWidth="2" strokeLinecap="round">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
      </div>
      <div>
        <p className="text-white font-semibold mb-1">Could not join meeting</p>
        <p className="text-zinc-400 text-sm">{message}</p>
      </div>
      <div className="flex gap-3">
        <button
          onClick={onRetry}
          className="px-4 py-2 rounded-lg text-white text-sm font-medium cursor-pointer"
          style={{ background: '#6366f1' }}
        >
          Try again
        </button>
        <button
          onClick={onHome}
          className="px-4 py-2 rounded-lg text-zinc-300 text-sm cursor-pointer"
          style={{ background: 'rgba(255,255,255,0.06)' }}
        >
          Home
        </button>
      </div>
    </div>
  );
}

// ── Video grid ────────────────────────────────────────────────────────────────

function VideoGrid({ peers }) {
  const peerList = Array.from(peers.entries()); // [[userId, { stream, displayName }]]
  const count = peerList.length;

  if (count === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-3 select-none">
        <div
          className="w-16 h-16 rounded-full flex items-center justify-center"
          style={{ background: 'rgba(99,102,241,0.15)' }}
        >
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#6366f1" strokeWidth="1.5" strokeLinecap="round">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
            <circle cx="9" cy="7" r="4" />
            <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
            <path d="M16 3.13a4 4 0 0 1 0 7.75" />
          </svg>
        </div>
        <p className="text-zinc-500 text-sm">Waiting for others to join…</p>
        <p className="text-zinc-700 text-xs">Share the meeting link to invite participants</p>
      </div>
    );
  }

  return (
    <div className="video-grid p-2" data-count={Math.min(count, 9).toString()}>
      {peerList.slice(0, 9).map(([userId, peer]) => (
        <VideoTile
          key={userId}
          stream={peer.stream}
          displayName={peer.displayName}
        />
      ))}
      {count > 9 && (
        <div className="flex items-center justify-center rounded-xl bg-tile text-zinc-400 text-sm">
          +{count - 9} more
        </div>
      )}
    </div>
  );
}

// ── Room header / info bar ────────────────────────────────────────────────────

function RoomHeader({ roomId, participantCount, onCopyLink }) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      onCopyLink?.();
    }
  }

  return (
    <div
      className="flex items-center justify-between px-4 py-2.5 shrink-0"
      style={{
        background: 'rgba(22,22,22,0.9)',
        borderBottom: '1px solid rgba(255,255,255,0.05)',
        backdropFilter: 'blur(8px)',
      }}
    >
      {/* Left: wordmark */}
      <div className="flex items-center gap-2">
        <div
          className="w-7 h-7 rounded-lg flex items-center justify-center"
          style={{ background: 'linear-gradient(135deg, #6366f1, #4f46e5)' }}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="white">
            <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" />
          </svg>
        </div>
        <span className="text-white text-sm font-semibold hidden sm:block">RM Meet</span>
      </div>

      {/* Center: room code */}
      <div className="flex items-center gap-2">
        <span
          className="font-mono text-zinc-400 text-xs bg-zinc-800 px-2.5 py-1 rounded select-all"
        >
          {roomId}
        </span>
        <span className="text-zinc-600 text-xs">{participantCount} participant{participantCount !== 1 ? 's' : ''}</span>
      </div>

      {/* Right: copy link */}
      <button
        onClick={handleCopy}
        className="flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg cursor-pointer transition-colors"
        style={{
          color: copied ? '#86efac' : '#a1a1aa',
          background: copied ? 'rgba(134,239,172,0.1)' : 'rgba(255,255,255,0.06)',
          border: '1px solid rgba(255,255,255,0.08)',
        }}
      >
        {copied ? (
          <>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round"><polyline points="20 6 9 17 4 12" /></svg>
            Copied!
          </>
        ) : (
          <>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><rect x="9" y="9" width="13" height="13" rx="2" /><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" /></svg>
            Copy link
          </>
        )}
      </button>
    </div>
  );
}

// ── Local video PIP ───────────────────────────────────────────────────────────

function LocalVideoPip({ stream, displayName, isCameraOff }) {
  const videoRef = useRef(null);

  useEffect(() => {
    const el = videoRef.current;
    if (!el) return;
    el.srcObject = stream || null;
  }, [stream]);

  return (
    <div
      className="fixed bottom-24 right-4 z-40 rounded-xl overflow-hidden shadow-2xl"
      style={{
        width: '192px',
        height: '128px',
        border: '2px solid #6366f1',
        background: '#1a1a1a',
      }}
    >
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className={`w-full h-full object-cover ${isCameraOff ? 'opacity-0' : 'opacity-100'}`}
      />
      {isCameraOff && (
        <div className="absolute inset-0 flex items-center justify-center">
          <div
            className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-semibold text-white"
            style={{ background: 'linear-gradient(135deg, #6366f1, #4f46e5)' }}
          >
            {(displayName || 'Y')[0].toUpperCase()}
          </div>
        </div>
      )}
      <div className="absolute bottom-0 left-0 right-0 px-2 py-1 bg-gradient-to-t from-black/60 to-transparent">
        <span className="text-white text-xs font-medium">You</span>
      </div>
    </div>
  );
}

// ── Main RoomPage ─────────────────────────────────────────────────────────────

export default function RoomPage() {
  const { roomId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();

  const displayName = location.state?.displayName;

  // Redirect to pre-join if no name was provided
  useEffect(() => {
    if (!displayName) {
      navigate(`/join/${roomId}`, { replace: true });
    }
  }, [displayName, roomId, navigate]);

  const [token, setToken] = useState(null);
  const [orgId, setOrgId] = useState(null);
  const [sessionError, setSessionError] = useState(null);
  const [sessionLoading, setSessionLoading] = useState(true);
  const [retryCount, setRetryCount] = useState(0);

  // Obtain guest session token
  useEffect(() => {
    if (!displayName) return;

    let cancelled = false;
    setSessionLoading(true);
    setSessionError(null);

    createGuestSession({ name: displayName })
      .then((data) => {
        if (cancelled) return;
        setToken(data.token);
        setOrgId(data.user?.org_id || null);
        setSessionLoading(false);
      })
      .catch((err) => {
        if (cancelled) return;
        console.error('[RoomPage] Guest session error:', err);
        setSessionError(err.message || 'Failed to create guest session');
        setSessionLoading(false);
      });

    return () => { cancelled = true; };
  }, [displayName, retryCount]);

  // WebRTC hook — only runs when we have a valid token
  const {
    localStream,
    peers,
    isMuted,
    isCameraOff,
    toggleMic,
    toggleCamera,
    leave,
    error: rtcError,
    status,
  } = useWebRTC(
    token
      ? { roomId, displayName, token, orgId }
      : { roomId: null, displayName: null, token: null, orgId: null }
  );

  const handleLeave = useCallback(() => {
    leave();
    navigate('/', { replace: true });
  }, [leave, navigate]);

  function handleRetry() {
    setRetryCount((n) => n + 1);
  }

  // Guard: no name
  if (!displayName) return null;

  // Loading state
  if (sessionLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: '#0a0a0a' }}>
        <Spinner />
      </div>
    );
  }

  // Session error
  if (sessionError) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: '#0a0a0a' }}>
        <FatalError
          message={sessionError}
          onRetry={handleRetry}
          onHome={() => navigate('/')}
        />
      </div>
    );
  }

  // RTC connecting (brief)
  if (status === 'connecting' && peers.size === 0 && !rtcError) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ background: '#0a0a0a' }}>
        <Spinner />
      </div>
    );
  }

  const totalParticipants = peers.size + 1; // +1 for self

  return (
    <div className="h-screen flex flex-col overflow-hidden" style={{ background: '#0a0a0a' }}>
      {/* Top bar */}
      <RoomHeader
        roomId={roomId}
        participantCount={totalParticipants}
      />

      {/* Connection warning banner */}
      {rtcError && (
        <div
          className="px-4 py-2 text-center text-sm shrink-0"
          style={{ background: 'rgba(220,38,38,0.12)', color: '#fca5a5', borderBottom: '1px solid rgba(220,38,38,0.2)' }}
        >
          {rtcError}
        </div>
      )}

      {/* Video area — fills remaining space above toolbar */}
      <div className="flex-1 overflow-hidden" style={{ paddingBottom: '88px' }}>
        <VideoGrid peers={peers} />
      </div>

      {/* Local video PIP */}
      <LocalVideoPip
        stream={localStream}
        displayName={displayName}
        isCameraOff={isCameraOff}
      />

      {/* Toolbar */}
      <Toolbar
        isMuted={isMuted}
        isCameraOff={isCameraOff}
        onToggleMic={toggleMic}
        onToggleCamera={toggleCamera}
        onLeave={handleLeave}
      />

      {/* Watermark */}
      <div className="fixed bottom-4 left-4 z-30 select-none pointer-events-none">
        <span className="text-zinc-700 text-xs">Powered by RM Orbit</span>
      </div>
    </div>
  );
}
