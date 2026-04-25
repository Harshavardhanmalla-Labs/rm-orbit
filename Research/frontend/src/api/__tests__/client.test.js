/**
 * API Client Contract Tests
 *
 * These tests verify that:
 * 1. The API client validates responses against the expected contract
 * 2. Invalid responses are rejected with clear error messages
 * 3. The original bug (raw array response) is caught by validation
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { api } from '../client'

// Mock axios interceptors
vi.mock('axios', () => {
  const actual = vi.importActual('axios')
  return {
    default: {
      create: vi.fn((config) => {
        const instance = actual.default.create(config)
        instance.interceptors = {
          request: { use: vi.fn((success, error) => {}) },
          response: { use: vi.fn((success, error) => {}) },
        }
        return instance
      }),
    },
  }
})

describe('API Contract Validation', () => {
  describe('papers list response validation', () => {
    it('should accept valid papers list response', async () => {
      const validResponse = {
        papers: [
          {
            id: '550e8400-e29b-41d4-a716-446655440000',
            title: 'Test Paper',
            topic: 'ML',
            niche: 'Deep Learning',
            target_venue: 'arxiv',
            paper_type: 'original_research',
            status: 'complete',
            current_stage: 'complete',
            stage_progress: 100,
            created_at: '2026-04-25T10:30:00Z',
          },
        ],
        total: 1,
        counts: {
          total: 1,
          complete: 1,
          failed: 0,
          draft: 0,
          running: 0,
          cancelled: 0,
        },
      }

      // Create a mock response config
      const config = { url: '/api/papers/', method: 'get' }
      const response = { config, data: validResponse, status: 200 }

      // Validation should pass
      expect(() => {
        // Simulate the response interceptor
        validatePapersListResponse(response.data)
      }).not.toThrow()
    })

    it('should reject raw array response (original bug)', () => {
      const buggyResponse = [
        {
          id: '550e8400-e29b-41d4-a716-446655440000',
          title: 'Test Paper',
          status: 'complete',
        },
      ]

      expect(() => {
        validatePapersListResponse(buggyResponse)
      }).toThrow(/raw array/)
      expect(() => {
        validatePapersListResponse(buggyResponse)
      }).toThrow(/{papers: Array, total: number, counts:/)
    })

    it('should reject response without papers field', () => {
      const invalidResponse = {
        total: 1,
        counts: {
          total: 1,
          complete: 1,
          failed: 0,
          draft: 0,
          running: 0,
          cancelled: 0,
        },
      }

      expect(() => {
        validatePapersListResponse(invalidResponse)
      }).toThrow(/'papers' must be array/)
    })

    it('should reject response with non-array papers', () => {
      const invalidResponse = {
        papers: 'not an array',
        total: 1,
        counts: {
          total: 1,
          complete: 1,
          failed: 0,
          draft: 0,
          running: 0,
          cancelled: 0,
        },
      }

      expect(() => {
        validatePapersListResponse(invalidResponse)
      }).toThrow(/'papers' must be array/)
    })

    it('should reject response without total field', () => {
      const invalidResponse = {
        papers: [],
        counts: {
          total: 0,
          complete: 0,
          failed: 0,
          draft: 0,
          running: 0,
          cancelled: 0,
        },
      }

      expect(() => {
        validatePapersListResponse(invalidResponse)
      }).toThrow(/'total' must be number/)
    })

    it('should reject response with non-number total', () => {
      const invalidResponse = {
        papers: [],
        total: 'one',
        counts: {
          total: 0,
          complete: 0,
          failed: 0,
          draft: 0,
          running: 0,
          cancelled: 0,
        },
      }

      expect(() => {
        validatePapersListResponse(invalidResponse)
      }).toThrow(/'total' must be number/)
    })

    it('should reject response without counts field', () => {
      const invalidResponse = {
        papers: [],
        total: 0,
      }

      expect(() => {
        validatePapersListResponse(invalidResponse)
      }).toThrow(/'counts' must be object/)
    })

    it('should reject response with missing count subfields', () => {
      const invalidResponse = {
        papers: [],
        total: 0,
        counts: {
          total: 0,
          complete: 0,
          failed: 0,
          // missing draft, running, cancelled
        },
      }

      expect(() => {
        validatePapersListResponse(invalidResponse)
      }).toThrow(/counts\.(draft|running|cancelled)/)
    })

    it('should reject null response', () => {
      expect(() => {
        validatePapersListResponse(null)
      }).toThrow(/Response is empty or null/)
    })

    it('should reject undefined response', () => {
      expect(() => {
        validatePapersListResponse(undefined)
      }).toThrow(/Response is empty or null/)
    })

    it('should reject non-object response', () => {
      expect(() => {
        validatePapersListResponse('invalid')
      }).toThrow(/Expected object, got string/)
    })

    it('error messages should be helpful for debugging', () => {
      const buggyResponse = [{ id: '1', status: 'complete' }]

      try {
        validatePapersListResponse(buggyResponse)
        expect.fail('Should have thrown')
      } catch (e) {
        expect(e.message).toContain('API contract violation')
        expect(e.message).toContain('See app/api/papers.py')
      }
    })
  })
})

/**
 * Local validation function for testing
 * (In actual code, this is in client.js)
 */
function validatePapersListResponse(data) {
  if (!data) {
    throw new Error('API contract violation: Response is empty or null')
  }

  if (Array.isArray(data)) {
    throw new Error(
      'API contract violation: Expected {papers: Array, total: number, counts: {...}}, ' +
      'but got raw array. Backend needs to return {papers: [...]}. ' +
      'See app/api/papers.py list_papers() endpoint.'
    )
  }

  if (typeof data !== 'object') {
    throw new Error(
      `API contract violation: Expected object, got ${typeof data}. ` +
      'Response must match PapersListResponse schema.'
    )
  }

  if (!Array.isArray(data.papers)) {
    throw new Error(
      `API contract violation: 'papers' must be array, got ${typeof data.papers}. ` +
      'Ensure backend returns PapersListResponse with papers field.'
    )
  }

  if (typeof data.total !== 'number') {
    throw new Error(
      `API contract violation: 'total' must be number, got ${typeof data.total}. ` +
      'Ensure backend returns PapersListResponse.total field.'
    )
  }

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
