export const WRITER_WORKSPACE_KEY = "writer_workspace_id";
export const WRITER_DEFAULT_WORKSPACE = "ws-default";

export function getWorkspaceId(): string {
  return window.localStorage.getItem(WRITER_WORKSPACE_KEY) || WRITER_DEFAULT_WORKSPACE;
}

export function getAuthToken(): string {
  return (
    window.localStorage.getItem("auth_token") ||
    window.localStorage.getItem("gate_access_token") ||
    ""
  );
}

export function getCachedOrgId(): string {
  const raw = window.localStorage.getItem("auth_user");
  if (!raw) return "";
  try {
    const parsed = JSON.parse(raw);
    return parsed?.org_id || parsed?.orgId || "";
  } catch {
    return "";
  }
}

interface RequestOptions {
  method?: string;
  workspaceId?: string;
  body?: unknown;
}

export async function writerApi<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = "GET", workspaceId = getWorkspaceId(), body = null } = options;
  const authToken = getAuthToken();
  const orgId = getCachedOrgId();
  
  const response = await fetch(`/api${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      "X-Workspace-Id": workspaceId,
      ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
      ...(orgId ? { "X-Org-Id": orgId } : {}),
    },
    body: body ? JSON.stringify(body) : null,
  });

  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    try {
      const payload = await response.json();
      detail = payload.detail || payload.error || detail;
    } catch {
      // no-op fallback
    }
    throw new Error(detail);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  const text = await response.text();
  if (!text) {
    return undefined as T;
  }
  return JSON.parse(text) as T;
}
