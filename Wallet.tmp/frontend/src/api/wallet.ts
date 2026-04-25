import api from './client'

export interface Secret {
  id: string
  name: string
  type: string
  project: string | null
  tags: string[]
  notes: string | null
  masked_value: string
  created_at: string
  updated_at: string
}

export interface SharedInfo {
  id: string
  category: string
  title: string
  value: string
  environment: string | null
  owner_team: string | null
  notes: string | null
  updated_at: string
}

export const secretsApi = {
  list: (p?: { search?: string; type?: string; project?: string }) =>
    api.get<Secret[]>('/wallet/secrets', { params: p }),
  create: (d: {
    name: string
    type: string
    value: string
    project?: string
    tags?: string[]
    notes?: string
  }) => api.post<Secret>('/wallet/secrets', d),
  reveal: (id: string) =>
    api.get<{ value: string }>(`/wallet/secrets/${id}/reveal`),
  delete: (id: string) => api.delete(`/wallet/secrets/${id}`),
}

export const sharedInfoApi = {
  list: (p?: { category?: string; search?: string }) =>
    api.get<SharedInfo[]>('/wallet/shared-info', { params: p }),
}
