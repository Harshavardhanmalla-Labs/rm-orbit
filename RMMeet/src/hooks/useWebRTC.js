/**
 * useWebRTC.js
 *
 * Manages the full WebRTC + Socket.IO lifecycle for a guest participant.
 *
 * Signaling event contract (matches Meet backend signaling-runtime.js):
 *   Outbound: join-room, signal.offer, signal.answer, signal.ice-candidate, leave-room
 *   Inbound:  meeting.participant_joined, meeting.participant_left,
 *             signal.offer, signal.answer, signal.ice-candidate,
 *             chat.history (ignored here)
 *
 * Rooms are org-scoped on the server side ({orgId}:{roomId}). Guests use the
 * orgId embedded in their JWT, so the frontend just passes the bare roomId.
 *
 * Returns:
 *   localStream    – MediaStream | null
 *   peers          – Map<userId, { stream: MediaStream|null, displayName: string }>
 *   isMuted        – boolean
 *   isCameraOff    – boolean
 *   toggleMic()    – toggle local audio track
 *   toggleCamera() – toggle local video track
 *   leave()        – emit leave-room, close connections, stop tracks
 *   error          – string | null  (fatal errors surfaced to UI)
 *   status         – 'connecting' | 'connected' | 'disconnected'
 */

import { useEffect, useRef, useState, useCallback } from 'react';
import { io } from 'socket.io-client';

const STUN = {
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'stun:stun1.l.google.com:19302' },
  ],
};

const SOCKET_URL = '/'; // proxied by Vite → http://localhost:6001

export function useWebRTC({ roomId, displayName, token, orgId }) {
  const [localStream, setLocalStream] = useState(null);
  // peers: Map<userId, { stream: MediaStream|null, displayName: string }>
  const [peers, setPeers] = useState(new Map());
  const [isMuted, setIsMuted] = useState(false);
  const [isCameraOff, setIsCameraOff] = useState(false);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState('connecting');

  // Refs — stable across re-renders, no stale-closure issues in socket callbacks
  const socketRef = useRef(null);
  const localStreamRef = useRef(null);
  const peerConnectionsRef = useRef(new Map()); // userId -> RTCPeerConnection
  const pendingIceCandidatesRef = useRef(new Map()); // userId -> ICECandidate[]
  const roomIdRef = useRef(roomId);
  const displayNameRef = useRef(displayName);

  // ─── helpers ────────────────────────────────────────────────────────────────

  function updatePeer(userId, patch) {
    setPeers((prev) => {
      const next = new Map(prev);
      const existing = next.get(userId) || { stream: null, displayName: userId };
      next.set(userId, { ...existing, ...patch });
      return next;
    });
  }

  function removePeer(userId) {
    setPeers((prev) => {
      const next = new Map(prev);
      next.delete(userId);
      return next;
    });

    const pc = peerConnectionsRef.current.get(userId);
    if (pc) {
      pc.close();
      peerConnectionsRef.current.delete(userId);
    }
    pendingIceCandidatesRef.current.delete(userId);
  }

  function createPeerConnection(userId, remoteDisplayName) {
    // Avoid duplicates
    const existing = peerConnectionsRef.current.get(userId);
    if (existing) return existing;

    const pc = new RTCPeerConnection(STUN);
    peerConnectionsRef.current.set(userId, pc);
    updatePeer(userId, { stream: null, displayName: remoteDisplayName || userId });

    // Add local tracks so the remote peer gets our media
    if (localStreamRef.current) {
      localStreamRef.current.getTracks().forEach((track) => {
        pc.addTrack(track, localStreamRef.current);
      });
    }

    // Remote track → update peer stream
    pc.ontrack = (event) => {
      const [remoteStream] = event.streams;
      if (remoteStream) {
        updatePeer(userId, { stream: remoteStream });
      }
    };

    // ICE candidates → relay via signaling
    pc.onicecandidate = (event) => {
      if (!event.candidate) return;
      socketRef.current?.emit('signal.ice-candidate', {
        targetUserId: userId,
        roomId: roomIdRef.current,
        candidate: event.candidate,
      });
    };

    pc.onconnectionstatechange = () => {
      if (pc.connectionState === 'failed' || pc.connectionState === 'closed') {
        // Peer disconnected at ICE level — clean up visually
        removePeer(userId);
      }
    };

    // Flush any buffered ICE candidates that arrived before the remote description
    pc.onsignalingstatechange = () => {
      if (pc.signalingState === 'stable') {
        const buffered = pendingIceCandidatesRef.current.get(userId) || [];
        buffered.forEach((c) => pc.addIceCandidate(c).catch(() => {}));
        pendingIceCandidatesRef.current.delete(userId);
      }
    };

    return pc;
  }

  // ─── main effect ────────────────────────────────────────────────────────────

  useEffect(() => {
    if (!token || !roomId || !displayName) return;

    roomIdRef.current = roomId;
    displayNameRef.current = displayName;

    let cancelled = false;

    async function init() {
      // 1. Acquire local media
      let stream;
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      } catch (mediaErr) {
        // Gracefully degrade — audio only, or no media
        try {
          stream = await navigator.mediaDevices.getUserMedia({ video: false, audio: true });
          setIsCameraOff(true);
        } catch {
          // Meetings can proceed watch-only
          stream = new MediaStream();
          setIsMuted(true);
          setIsCameraOff(true);
        }
      }

      if (cancelled) {
        stream.getTracks().forEach((t) => t.stop());
        return;
      }

      localStreamRef.current = stream;
      setLocalStream(stream);

      // 2. Connect socket with guest token
      const socket = io(SOCKET_URL, {
        auth: {
          token,
          orgId: orgId || '',
        },
        transports: ['websocket', 'polling'],
        reconnectionAttempts: 5,
        reconnectionDelay: 1000,
      });
      socketRef.current = socket;

      socket.on('connect', () => {
        if (cancelled) return;
        setStatus('connected');
        setError(null);

        // 3. Join room
        socket.emit('join-room', {
          roomId,
          displayName,
        });
      });

      socket.on('connect_error', (err) => {
        if (cancelled) return;
        console.error('[RMMeet] Socket connect error:', err.message);
        setStatus('disconnected');
        setError(`Connection failed: ${err.message}`);
      });

      socket.on('disconnect', (reason) => {
        if (cancelled) return;
        setStatus('disconnected');
        if (reason !== 'io client disconnect') {
          setError('Disconnected from server. Trying to reconnect…');
        }
      });

      socket.on('reconnect', () => {
        if (cancelled) return;
        setStatus('connected');
        setError(null);
        socket.emit('join-room', { roomId, displayName });
      });

      // ── Participant joined → we are the INITIATOR (create offer) ──────────
      socket.on('meeting.participant_joined', async ({ user_id, display_name }) => {
        if (cancelled) return;
        if (!user_id) return;

        const pc = createPeerConnection(user_id, display_name);
        updatePeer(user_id, { displayName: display_name || user_id });

        try {
          const offer = await pc.createOffer();
          await pc.setLocalDescription(offer);
          socket.emit('signal.offer', {
            targetUserId: user_id,
            roomId,
            sdp: pc.localDescription,
          });
        } catch (err) {
          console.error('[RMMeet] Failed to create offer for', user_id, err);
        }
      });

      // ── Received offer → we are the ANSWERER ──────────────────────────────
      socket.on('signal.offer', async ({ from_user_id, sdp }) => {
        if (cancelled) return;
        if (!from_user_id || !sdp) return;

        const pc = createPeerConnection(from_user_id, from_user_id);

        try {
          await pc.setRemoteDescription(new RTCSessionDescription(sdp));
          const answer = await pc.createAnswer();
          await pc.setLocalDescription(answer);
          socket.emit('signal.answer', {
            targetUserId: from_user_id,
            roomId,
            sdp: pc.localDescription,
          });
        } catch (err) {
          console.error('[RMMeet] Failed to answer offer from', from_user_id, err);
        }
      });

      // ── Received answer ────────────────────────────────────────────────────
      socket.on('signal.answer', async ({ from_user_id, sdp }) => {
        if (cancelled) return;
        if (!from_user_id || !sdp) return;

        const pc = peerConnectionsRef.current.get(from_user_id);
        if (!pc) return;

        try {
          if (pc.signalingState !== 'have-local-offer') return;
          await pc.setRemoteDescription(new RTCSessionDescription(sdp));
        } catch (err) {
          console.error('[RMMeet] Failed to set answer from', from_user_id, err);
        }
      });

      // ── ICE candidate ──────────────────────────────────────────────────────
      socket.on('signal.ice-candidate', async ({ from_user_id, candidate }) => {
        if (cancelled) return;
        if (!from_user_id || !candidate) return;

        const pc = peerConnectionsRef.current.get(from_user_id);
        if (!pc) return;

        const iceCandidate = new RTCIceCandidate(candidate);

        if (pc.remoteDescription && pc.remoteDescription.type) {
          try {
            await pc.addIceCandidate(iceCandidate);
          } catch (err) {
            console.warn('[RMMeet] ICE candidate error:', err.message);
          }
        } else {
          // Buffer until remote description is set
          if (!pendingIceCandidatesRef.current.has(from_user_id)) {
            pendingIceCandidatesRef.current.set(from_user_id, []);
          }
          pendingIceCandidatesRef.current.get(from_user_id).push(iceCandidate);
        }
      });

      // ── Participant left ───────────────────────────────────────────────────
      socket.on('meeting.participant_left', ({ user_id }) => {
        if (cancelled) return;
        if (!user_id) return;
        removePeer(user_id);
      });

      // ── Generic errors from signaling ──────────────────────────────────────
      socket.on('meeting.error', ({ reason }) => {
        if (cancelled) return;
        console.warn('[RMMeet] Meeting error:', reason);
        setError(reason || 'An error occurred in the meeting');
      });
    }

    init().catch((err) => {
      if (!cancelled) {
        console.error('[RMMeet] Init error:', err);
        setError(err.message || 'Failed to initialize meeting');
        setStatus('disconnected');
      }
    });

    return () => {
      cancelled = true;

      // Close all peer connections
      peerConnectionsRef.current.forEach((pc) => pc.close());
      peerConnectionsRef.current.clear();
      pendingIceCandidatesRef.current.clear();

      // Leave room gracefully
      if (socketRef.current) {
        socketRef.current.emit('leave-room', { roomId: roomIdRef.current });
        socketRef.current.disconnect();
        socketRef.current = null;
      }

      // Stop local media
      if (localStreamRef.current) {
        localStreamRef.current.getTracks().forEach((t) => t.stop());
        localStreamRef.current = null;
      }

      setLocalStream(null);
      setPeers(new Map());
      setStatus('disconnected');
    };
  }, [token, roomId, displayName, orgId]); // eslint-disable-line react-hooks/exhaustive-deps

  // ─── controls ───────────────────────────────────────────────────────────────

  const toggleMic = useCallback(() => {
    const stream = localStreamRef.current;
    if (!stream) return;
    stream.getAudioTracks().forEach((track) => {
      track.enabled = !track.enabled;
    });
    setIsMuted((prev) => !prev);
  }, []);

  const toggleCamera = useCallback(() => {
    const stream = localStreamRef.current;
    if (!stream) return;
    stream.getVideoTracks().forEach((track) => {
      track.enabled = !track.enabled;
    });
    setIsCameraOff((prev) => !prev);
  }, []);

  const leave = useCallback(() => {
    if (socketRef.current) {
      socketRef.current.emit('leave-room', { roomId: roomIdRef.current });
      socketRef.current.disconnect();
      socketRef.current = null;
    }
    peerConnectionsRef.current.forEach((pc) => pc.close());
    peerConnectionsRef.current.clear();
    if (localStreamRef.current) {
      localStreamRef.current.getTracks().forEach((t) => t.stop());
      localStreamRef.current = null;
    }
    setLocalStream(null);
    setPeers(new Map());
    setStatus('disconnected');
  }, []);

  return {
    localStream,
    peers,
    isMuted,
    isCameraOff,
    toggleMic,
    toggleCamera,
    leave,
    error,
    status,
  };
}
