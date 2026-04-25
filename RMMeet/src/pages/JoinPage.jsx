/**
 * JoinPage.jsx — Pre-join lobby.
 *
 * Shows the room ID, asks for display name, then navigates to /room/:roomId
 * with the name passed via location state so RoomPage can start immediately.
 */

import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';

function IconVideo() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" />
      <circle cx="12" cy="13" r="3" />
    </svg>
  );
}

function IconArrowLeft() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <line x1="19" y1="12" x2="5" y2="12" />
      <polyline points="12 19 5 12 12 5" />
    </svg>
  );
}

export default function JoinPage() {
  const { roomId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const nameRef = useRef(null);

  // Restore name from session storage so returning users don't re-type
  const savedName = sessionStorage.getItem('rm-meet-display-name') || '';
  const [name, setName] = useState(savedName);
  const [nameError, setNameError] = useState('');

  useEffect(() => {
    nameRef.current?.focus();
  }, []);

  function handleJoin(e) {
    e.preventDefault();
    const trimmed = name.trim();
    if (!trimmed) {
      setNameError('Please enter your name to continue.');
      nameRef.current?.focus();
      return;
    }
    if (trimmed.length < 2) {
      setNameError('Name must be at least 2 characters.');
      return;
    }
    sessionStorage.setItem('rm-meet-display-name', trimmed);
    navigate(`/room/${roomId}`, { state: { displayName: trimmed }, replace: false });
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4" style={{ background: '#0a0a0a' }}>
      {/* Back button */}
      <div className="w-full max-w-md mb-4">
        <button
          onClick={() => navigate('/')}
          className="flex items-center gap-1.5 text-zinc-500 hover:text-zinc-300 text-sm cursor-pointer transition-colors"
        >
          <IconArrowLeft />
          Back
        </button>
      </div>

      {/* Card */}
      <div
        className="w-full max-w-md rounded-2xl p-8 shadow-2xl"
        style={{ background: '#161616', border: '1px solid rgba(255,255,255,0.07)' }}
      >
        {/* Header */}
        <div className="mb-6">
          <div className="flex items-center gap-2 text-indigo-400 text-xs font-medium mb-3 uppercase tracking-wider">
            <IconVideo />
            Meeting
          </div>
          <h1 className="text-white text-2xl font-bold mb-1">Ready to join?</h1>
          <p className="text-zinc-500 text-sm">
            Room:{' '}
            <span
              className="font-mono text-zinc-300 bg-zinc-800 px-2 py-0.5 rounded text-xs select-all"
            >
              {roomId}
            </span>
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleJoin} noValidate>
          <label htmlFor="display-name" className="block text-zinc-300 text-sm font-medium mb-2">
            Your name
          </label>
          <input
            id="display-name"
            ref={nameRef}
            type="text"
            value={name}
            onChange={(e) => {
              setName(e.target.value);
              setNameError('');
            }}
            placeholder="e.g. Alex Johnson"
            autoComplete="name"
            maxLength={60}
            className="w-full rounded-lg px-4 py-3 text-white text-sm placeholder-zinc-600 outline-none focus:ring-2 focus:ring-indigo-500"
            style={{
              background: '#0a0a0a',
              border: `1px solid ${nameError ? '#ef4444' : 'rgba(255,255,255,0.1)'}`,
            }}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleJoin(e);
            }}
          />
          {nameError && (
            <p className="mt-1.5 text-red-400 text-xs">{nameError}</p>
          )}

          <button
            type="submit"
            className="mt-5 w-full flex items-center justify-center gap-2 rounded-lg py-3.5 font-semibold text-white text-sm cursor-pointer"
            style={{ background: '#6366f1' }}
            onMouseEnter={(e) => (e.currentTarget.style.background = '#4f46e5')}
            onMouseLeave={(e) => (e.currentTarget.style.background = '#6366f1')}
          >
            Join Meeting
          </button>
        </form>

        {/* Notice */}
        <p className="mt-5 text-zinc-600 text-xs text-center leading-relaxed">
          By joining you consent to your audio and video being shared with other participants.
          No account or sign-up required.
        </p>
      </div>

      <p className="mt-8 text-zinc-700 text-xs">Powered by RM Orbit</p>
    </div>
  );
}
