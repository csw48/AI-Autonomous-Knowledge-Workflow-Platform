const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Request failed");
  }
  return response.json() as Promise<T>;
}

export type HealthResponse = {
  status: string;
  detail: string;
};

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE}/api/v1/health`, { cache: "no-store" });
  return handleResponse<HealthResponse>(response);
}

export type ChatResponse = {
  provider: string;
  answer: string;
};

export async function sendChat(prompt: string): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE}/api/v1/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }),
  });

  return handleResponse<ChatResponse>(response);
}

export type RagContext = {
  document_id: string;
  chunk_index: number;
  content: string;
};

export interface RagChatResponse extends ChatResponse {
  contexts: RagContext[];
}

export async function sendRagChat(query: string, top_k = 5): Promise<RagChatResponse> {
  const response = await fetch(`${API_BASE}/api/v1/chat/rag`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query, top_k }),
  });

  return handleResponse<RagChatResponse>(response);
}

export type DocumentUploadResponse = {
  id: string;
  title: string;
  chunk_count: number;
  source?: string | null;
};

export async function uploadDocument(file: File, title?: string): Promise<DocumentUploadResponse> {
  const form = new FormData();
  form.append("file", file);
  if (title) {
    form.append("title", title);
  }

  const response = await fetch(`${API_BASE}/api/v1/documents`, {
    method: "POST",
    body: form,
  });

  return handleResponse<DocumentUploadResponse>(response);
}

export type SearchMatch = {
  document_id: string;
  chunk_index: number;
  content: string;
};

export async function searchDocuments({
  query,
  limit = 5,
}: {
  query: string;
  limit?: number;
}): Promise<SearchMatch[]> {
  const response = await fetch(`${API_BASE}/api/v1/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, limit }),
  });
  return handleResponse<SearchMatch[]>(response);
}
