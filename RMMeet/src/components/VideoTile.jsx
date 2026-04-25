/**
 * VideoTile.jsx — Single participant video tile.
 *
 * Renders a video element attached to the given MediaStream, with the
 * participant's display name overlaid at the bottom-left.
 *
 * When there is no stream (peer joined but WebRTC hasn't exchanged tracks yet)
 * it shows an avatar placeholder with initials.
 */

import { useEffect, useRef } from 'react';

function getInitials(name = '') {
  return name
    .split(' ')
    .slice(0, 2)
    .map((w) => w[0]?.toUpperCase() || '')
    .join('');
}

export default function VideoTile({ stream, displayName, isLocal = false }) {
  const videoRef = useRef(null);

  useEffect(() => {
    const el = videoRef.current;
    if (!el) return;
    if (stream) {
      el.srcObject = stream;
    } else {
      el.srcObject = null;
    }
  }, [stream]);

  const hasVideo = stream && stream.getVideoTracks().some((t) => t.enabled && t.readyState === 'live');

  return (
    <div className="relative rounded-xl overflow-hidden bg-tile flex items-center justify-center w-full h-full min-h-[120px]">
      {/* Video element — always rendered so srcObject assignment works */}
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted={isLocal}
        className={`w-full h-full object-cover ${hasVideo ? 'opacity-100' : 'opacity-0 absolute inset-0'}`}
      />

      {/* Avatar placeholder when no video */}
      {!hasVideo && (
        <div className="flex flex-col items-center justify-center gap-3 z-10">
          <div
            className="w-16 h-16 rounded-full flex items-center justify-center text-xl font-semibold text-white select-none"
            style={{ background: 'linear-gradient(135deg, #6366f1 0%, #4f46e5 100%)' }}
          >
            {getInitials(displayName) || '?'}
          </div>
          <span className="text-zinc-400 text-sm">{displayName || 'Participant'}</span>
        </div>
      )}

      {/* Name overlay */}
      <div className="absolute bottom-0 left-0 right-0 px-3 py-2 bg-gradient-to-t from-black/70 to-transparent">
        <span className="text-white text-sm font-medium drop-shadow truncate block">
          {displayName || 'Participant'}
          {isLocal && (
            <span className="ml-1.5 text-xs text-indigo-300 font-normal">(you)</span>
          )}
        </span>
      </div>
    </div>
  );
}
