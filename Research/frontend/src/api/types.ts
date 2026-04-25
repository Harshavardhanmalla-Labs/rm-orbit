/**
 * API Contract Types
 *
 * These TypeScript types MUST match the Pydantic models in the backend.
 * They are the source of truth for the API contract.
 *
 * Generated from: app/api/papers.py (Pydantic models)
 * Last updated: 2026-04-25
 */

/**
 * Base paper fields (matches PaperBase in backend)
 */
export interface Paper {
  /** Unique paper ID (UUID) */
  id: string
  /** Paper title */
  title: string | null
  /** Research topic */
  topic: string | null
  /** Academic niche */
  niche: string | null
  /** Target publication venue */
  target_venue: string | null
  /** Paper type (original_research, survey, etc.) */
  paper_type: string | null
  /** Current status (intake, processing, complete, failed, etc.) */
  status: 'intake' | 'processing' | 'complete' | 'failed' | 'cancelled' | string
  /** Current pipeline stage */
  current_stage: string | null
  /** Progress percentage (0-100) */
  stage_progress: number | null
  /** Creation timestamp (ISO format) */
  created_at: string
}

/**
 * Count breakdown by status (matches PapersListCounts in backend)
 */
export interface PapersListCounts {
  /** Total papers */
  total: number
  /** Completed papers */
  complete: number
  /** Failed papers */
  failed: number
  /** Draft papers (intake status) */
  draft: number
  /** Running papers (processing/running status) */
  running: number
  /** Cancelled papers */
  cancelled: number
}

/**
 * Response for GET /api/papers/ (matches PapersListResponse in backend)
 */
export interface PapersListResponse {
  /** List of papers */
  papers: Paper[]
  /** Total number of papers */
  total: number
  /** Count breakdown by status */
  counts: PapersListCounts
}

/**
 * Brain status response (matches brain_readiness in backend)
 */
export interface BrainComponent {
  name: string
  status: 'ready' | 'missing'
  required: boolean
  message: string
}

export interface BrainStatus {
  status: 'ready' | 'degraded' | 'not_ready'
  can_generate: boolean
  can_ingest_basic_files: boolean
  can_ingest_rich_pdfs: boolean
  can_parse_math_pdfs: boolean
  can_export_docx: boolean
  can_export_pdf: boolean
  optional_missing: string[]
  components: BrainComponent[]
}
