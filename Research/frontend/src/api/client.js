import axios from 'axios'

const configuredApiBaseUrl = import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, '')

export const API_BASE_URL = configuredApiBaseUrl || ''

export function apiUrl(path) {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  return `${API_BASE_URL}${normalizedPath}`
}

export function wsUrl(path) {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  const baseUrl = configuredApiBaseUrl || window.location.origin
  const url = new URL(normalizedPath, baseUrl)
  url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:'
  return url.toString()
}

export const api = axios.create({ baseURL: API_BASE_URL })

// ============================================================================
// API Contract Validation
// ============================================================================
/**
 * Validate that a papers list response matches the expected contract.
 *
 * Contract: {
 *   papers: Array,
 *   total: number,
 *   counts: { total, complete, failed, draft, running, cancelled }
 * }
 */
function validatePapersListResponse(data) {
  if (!data) {
    throw new Error('API contract violation: Response is empty or null')
  }

  // Check for OLD bug: raw array response (before the fix)
  if (Array.isArray(data)) {
    throw new Error(
      'API contract violation: Expected {papers: Array, total: number, counts: {...}}, ' +
      'but got raw array. Backend needs to return {papers: [...]}. ' +
      'See app/api/papers.py list_papers() endpoint.'
    )
  }

  // Check for expected structure
  if (typeof data !== 'object') {
    throw new Error(
      `API contract violation: Expected object, got ${typeof data}. ` +
      'Response must match PapersListResponse schema.'
    )
  }

  // Validate papers array
  if (!Array.isArray(data.papers)) {
    throw new Error(
      `API contract violation: 'papers' must be array, got ${typeof data.papers}. ` +
      'Ensure backend returns PapersListResponse with papers field.'
    )
  }

  // Validate total count
  if (typeof data.total !== 'number') {
    throw new Error(
      `API contract violation: 'total' must be number, got ${typeof data.total}. ` +
      'Ensure backend returns PapersListResponse.total field.'
    )
  }

  // Validate counts object
  if (!data.counts || typeof data.counts !== 'object') {
    throw new Error(
      `API contract violation: 'counts' must be object, got ${typeof data.counts}. ` +
      'Ensure backend returns PapersListCounts with total, complete, failed, draft, running, cancelled.'
    )
  }

  const requiredCountFields = ['total', 'complete', 'failed', 'draft', 'running', 'cancelled']
  for (const field of requiredCountFields) {
    if (typeof data.counts[field] !== 'number') {
      throw new Error(
        `API contract violation: 'counts.${field}' must be number, got ${typeof data.counts[field]}. ` +
        'Ensure backend returns all count fields in PapersListCounts.'
      )
    }
  }

  return true
}

// Request interceptor for logging
api.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error)
)

// Response interceptor for unified error handling + contract validation
api.interceptors.response.use(
  (response) => {
    // Special handling for /api/papers/ endpoint
    if (response.config.url?.includes('/api/papers/') && response.config.method === 'get') {
      try {
        validatePapersListResponse(response.data)
      } catch (e) {
        console.error('API Contract Violation:', e.message)
        throw e
      }
    }

    return response
  },
  (error) => {
    const message = error.response?.data?.detail || error.response?.data?.message || error.message || 'An unknown error occurred'
    return Promise.reject(new Error(message))
  }
)
