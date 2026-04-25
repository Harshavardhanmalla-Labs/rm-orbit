import axios from 'axios';

const api = axios.create({ baseURL: '/' });

export interface SearchResult {
  id: string;
  source: string;
  entity_type: string;
  title: string;
  snippet: string;
  url: string;
  score: number;
  updated_at: string | null;
  metadata: Record<string, unknown>;
}

export interface SearchResponse {
  query: string;
  org_id: string | null;
  total: number;
  took_ms: number;
  sources: string[];
  results: SearchResult[];
}

export const searchApi = {
  search: (query: string, sources?: string[], limit = 20) =>
    api.get<SearchResponse>('/api/search', {
      params: {
        q: query,
        limit,
        ...(sources?.length ? { sources: sources.join(',') } : {}),
      },
    }),
  getSources: () => api.get<{ sources: string[] }>('/api/search/sources'),
};
