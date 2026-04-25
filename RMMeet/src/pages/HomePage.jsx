/**
 * HomePage.jsx — Landing page.
 *
 * Two actions:
 *   1. Enter a meeting link or code → navigates to /join/:roomId
 *   2. Start instant meeting → generates a random roomId → navigates to /join/:roomId
 */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function generateRoomId() {
  // xxx-yyyy-zzz format (Google Meet–style)
  const seg = () => Math.random().toString(36).slice(2, 5).toLowerCase();
  return `${seg()}-${seg()}${seg()}-${seg()}`;
}

function extractRoomId(input) {
  // Accept: full URL (.../room/abc  or  .../join/abc), bare code, or "abc-defg-hij" style
  try {
    const url = new URL(input.includes('://') ? input : `https://x.com${input.startsWith('/') ? '' : '/'}${input}`);
    const parts = url.pathname.split('/').filter(Boolean);
    const roomIdx = parts.findIndex((p) => p === 'room' || p === 'join');
    if (roomIdx !== -1 && parts[roomIdx + 1]) {
      return parts[roomIdx + 1];
    }
  } catch {
    // not a URL — treat input as raw room code
  }
  return input.trim().replace(/\s+/g, '-');
}

// ── Inline SVG icons ──────────────────────────────────────────────────────────

function IconVideo() {
  return (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#6366f1" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" />
      <circle cx="12" cy="13" r="3" />
    </svg>
  );
}

function IconPlus() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
      <line x1="12" y1="5" x2="12" y2="19" />
      <line x1="5" y1="12" x2="19" y2="12" />
    </svg>
  );
}

function IconArrow() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>
  );
}

// ─────────────────────────────────────────────────────────────────────────────

export default function HomePage() {
  const navigate = useNavigate();
  const [input, setInput] = useState('');
  const [inputError, setInputError] = useState('');

  function handleJoin(e) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) {
      setInputError('Please enter a meeting link or code.');
      return;
    }
    const roomId = extractRoomId(trimmed);
    if (!roomId) {
      setInputError('Could not parse a room ID from that link.');
      return;
    }
    navigate(`/join/${encodeURIComponent(roomId)}`);
  }

  function handleInstant() {
    navigate(`/join/${generateRoomId()}`);
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4" style={{ background: '#0a0a0a' }}>
      {/* Card */}
      <div
        className="w-full max-w-md rounded-2xl p-8 shadow-2xl"
        style={{ background: '#161616', border: '1px solid rgba(255,255,255,0.07)' }}
      >
        {/* Logo + wordmark */}
        <div className="flex items-center gap-3 mb-8">
          <div
            className="w-10 h-10 rounded-xl flex items-center justify-center"
            style={{ background: 'linear-gradient(135deg, #6366f1, #4f46e5)' }}
          >
            <IconVideo />
          </div>
          <div>
            <div className="text-white font-semibold text-lg leading-tight">RM Meet</div>
            <div className="text-zinc-500 text-xs">Guest access — no account required</div>
          </div>
        </div>

        {/* Join form */}
        <form onSubmit={handleJoin} noValidate>
          <label htmlFor="meeting-input" className="block text-zinc-300 text-sm font-medium mb-2">
            Meeting link or code
          </label>
          <input
            id="meeting-input"
            type="text"
            value={input}
            onChange={(e) => {
              setInput(e.target.value);
              setInputError('');
            }}
            placeholder="e.g. abc-defg-hij or paste a link"
            autoFocus
            autoComplete="off"
            spellCheck={false}
            className="w-full rounded-lg px-4 py-3 text-white text-sm placeholder-zinc-600 outline-none focus:ring-2 focus:ring-indigo-500"
            style={{ background: '#0a0a0a', border: `1px solid ${inputError ? '#ef4444' : 'rgba(255,255,255,0.1)'}` }}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleJoin(e);
            }}
          />
          {inputError && (
            <p className="mt-1.5 text-red-400 text-xs">{inputError}</p>
          )}

          <button
            type="submit"
            className="mt-4 w-full flex items-center justify-center gap-2 rounded-lg py-3 font-semibold text-white text-sm cursor-pointer"
            style={{ background: '#6366f1' }}
            onMouseEnter={(e) => (e.currentTarget.style.background = '#4f46e5')}
            onMouseLeave={(e) => (e.currentTarget.style.background = '#6366f1')}
          >
            <IconArrow />
            Join Meeting
          </button>
        </form>

        {/* Divider */}
        <div className="flex items-center gap-3 my-6">
          <div className="flex-1 h-px bg-white/8" />
          <span className="text-zinc-600 text-xs">or</span>
          <div className="flex-1 h-px bg-white/8" />
        </div>

        {/* Instant meeting */}
        <button
          onClick={handleInstant}
          className="w-full flex items-center justify-center gap-2 rounded-lg py-3 font-medium text-zinc-300 text-sm cursor-pointer"
          style={{ background: 'rgba(99,102,241,0.1)', border: '1px solid rgba(99,102,241,0.25)' }}
          onMouseEnter={(e) => (e.currentTarget.style.background = 'rgba(99,102,241,0.18)')}
          onMouseLeave={(e) => (e.currentTarget.style.background = 'rgba(99,102,241,0.1)')}
        >
          <IconPlus />
          Start instant meeting
        </button>
      </div>

      {/* Footer */}
      <p className="mt-8 text-zinc-700 text-xs text-center">
        Powered by{' '}
        <span className="text-zinc-500">RM Orbit</span>
        {' '}·{' '}
        <span className="text-zinc-600">Enterprise suite for founders</span>
      </p>
    </div>
  );
}
