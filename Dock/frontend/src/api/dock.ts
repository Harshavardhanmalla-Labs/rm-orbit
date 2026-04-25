import api from './client'

export interface App {
  id: string
  name: string
  vendor: string | null
  category: string | null
  status: string
  version: string | null
  description: string | null
  license_type: string | null
  cost_per_seat: number | null
  created_at: string
}

export interface License {
  id: string
  app_id: string
  app_name?: string
  license_key: string | null
  seats_total: number
  seats_used: number
  expiry_date: string | null
  status: string
  created_at: string
}

export interface Assignment {
  id: string
  app_id: string
  app_name?: string
  user_id: string
  user_email?: string
  status: string
  assigned_at: string
  expires_at: string | null
}

export interface AccessRequest {
  id: string
  app_id: string
  app_name?: string
  requester_id: string
  requester_email?: string
  status: string
  justification: string | null
  requested_at: string
  reviewed_at: string | null
}

export interface AuditEvent {
  id: string
  action: string
  actor_id: string
  resource_type: string
  resource_id: string
  created_at: string
}

export const appsApi = {
  list: (p?: { search?: string; status?: string; category?: string }) =>
    api.get<App[]>('/dock/apps', { params: p }),
  assigned: () => api.get<App[]>('/dock/apps/assigned'),
  create: (d: Partial<App> & { name: string }) => api.post<App>('/dock/apps', d),
  update: (id: string, d: Partial<App>) => api.patch<App>(`/dock/apps/${id}`, d),
}

export const licensesApi = {
  list: () => api.get<License[]>('/dock/licenses'),
  create: (d: {
    app_id: string
    seats_total: number
    license_key?: string
    expiry_date?: string
  }) => api.post<License>('/dock/licenses', d),
}

export const assignmentsApi = {
  list: () => api.get<Assignment[]>('/dock/assignments'),
  create: (d: { app_id: string; user_id: string; expires_at?: string }) =>
    api.post<Assignment>('/dock/assignments', d),
  update: (id: string, d: Partial<Assignment>) =>
    api.patch<Assignment>(`/dock/assignments/${id}`, d),
}

export const requestsApi = {
  list: (p?: { status?: string }) =>
    api.get<AccessRequest[]>('/dock/requests', { params: p }),
  create: (d: { app_id: string; justification?: string }) =>
    api.post<AccessRequest>('/dock/requests', d),
  update: (id: string, d: { status: string }) =>
    api.patch<AccessRequest>(`/dock/requests/${id}`, d),
}

export const auditApi = {
  list: () => api.get<AuditEvent[]>('/dock/audit/events'),
}
