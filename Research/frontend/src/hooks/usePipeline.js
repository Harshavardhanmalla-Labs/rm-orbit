import { useState, useEffect, useRef } from 'react'
import { apiUrl, wsUrl } from '../api/client.js'

export function usePipeline(paperId) {
  const [status, setStatus] = useState(null)
  const [connected, setConnected] = useState(false)
  const [logs, setLogs] = useState([])
  const wsRef = useRef(null)
  const pollRef = useRef(null)

  useEffect(() => {
    if (!paperId) return

    let isMounted = true

    function startPolling() {
      if (pollRef.current) clearInterval(pollRef.current)
      pollRef.current = setInterval(async () => {
        try {
          const res = await fetch(apiUrl(`/api/pipeline/${paperId}/status`))
          if (!res.ok) return
          const data = await res.json()
          if (!isMounted) return
          setStatus(data)
          if (data.logs) setLogs(data.logs)
          if (data.status === 'complete' || data.status === 'failed') {
            clearInterval(pollRef.current)
          }
        } catch {
          // silently ignore polling errors
        }
      }, 3000)
    }

    function connect() {
      try {
        const ws = new WebSocket(wsUrl(`/api/pipeline/ws/${paperId}`))
        wsRef.current = ws

        ws.onopen = () => {
          if (isMounted) setConnected(true)
        }

        ws.onmessage = (e) => {
          if (!isMounted) return
          try {
            const data = JSON.parse(e.data)
            if (data.type === 'log') {
              setLogs((prev) => [...prev, data])
            } else {
              setStatus(data)
              if (data.logs) setLogs(data.logs)
            }
          } catch {
            // ignore malformed messages
          }
        }

        ws.onerror = () => {
          if (isMounted) {
            setConnected(false)
            startPolling()
          }
        }

        ws.onclose = () => {
          if (!isMounted) return
          setConnected(false)
          // Fall back to polling when WS closes so the UI stays live
          startPolling()
        }
      } catch {
        startPolling()
      }
    }

    connect()

    // Initial status fetch
    fetch(apiUrl(`/api/pipeline/${paperId}/status`))
      .then((r) => r.json())
      .then((data) => { if (isMounted) setStatus(data) })
      .catch(() => {})

    // Poll logs every 4 seconds while pipeline is running
    const logPollRef = setInterval(async () => {
      try {
        const r = await fetch(apiUrl(`/api/papers/${paperId}/logs`))
        if (!r.ok) return
        const entries = await r.json()
        if (!isMounted) return
        setLogs(entries.map((e) => ({
          message: `[${e.stage}] ${e.message}`,
          level: e.status === 'failed' ? 'error' : e.status === 'completed' ? 'success' : 'info',
          timestamp: e.created_at,
        })))
      } catch { /* ignore */ }
    }, 4000)

    return () => {
      isMounted = false
      if (wsRef.current) wsRef.current.close()
      if (pollRef.current) clearInterval(pollRef.current)
      clearInterval(logPollRef)
    }
  }, [paperId])

  return { status, connected, logs }
}
