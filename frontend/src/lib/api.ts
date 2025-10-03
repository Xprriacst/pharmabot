import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}

export interface Source {
  title: string
  content: string
  url: string
  source_type: 'vidal' | 'meddispar'
  relevance_score: number
}

export interface ChatResponse {
  response: string
  sources: Source[]
  session_id: string
  timestamp: string
  tokens_used?: number
}

export interface SearchResult {
  title: string
  content: string
  url: string
  source_type: string
  relevance_score: number
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const chatApi = {
  sendMessage: async (
    message: string,
    conversationHistory: Message[] = [],
    sessionId?: string
  ): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/chat', {
      message,
      conversation_history: conversationHistory,
      session_id: sessionId,
    })
    return response.data
  },

  clearSession: async (sessionId: string): Promise<void> => {
    await api.post('/chat/clear', { session_id: sessionId })
  },
}

export const searchApi = {
  search: async (
    query: string,
    sourceType?: string,
    limit: number = 10
  ): Promise<{ query: string; results: SearchResult[]; total_results: number }> => {
    const params: any = { q: query, limit }
    if (sourceType) params.source_type = sourceType
    
    const response = await api.get('/search', { params })
    return response.data
  },

  getStats: async (): Promise<any> => {
    const response = await api.get('/search/stats')
    return response.data
  },
}

export const healthApi = {
  check: async (): Promise<any> => {
    const response = await api.get('/health')
    return response.data
  },

  status: async (): Promise<any> => {
    const response = await api.get('/status')
    return response.data
  },
}

export default api
