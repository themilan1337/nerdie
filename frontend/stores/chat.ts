import { defineStore } from 'pinia'

export interface Message {
    id: string | number
    type: 'user' | 'assistant'
    content: string
    timestamp: string | Date
    sources?: { name: string; page?: number }[]
}

export interface ChatSession {
    id: string
    title: string
    messages: Message[]
    createdAt: string | Date
    updatedAt: string | Date
}

export const useChatStore = defineStore('chat', {
    state: () => ({
        sessions: [] as ChatSession[],
        currentSessionId: null as string | null,
    }),
    getters: {
        currentSession: (state) => state.sessions.find(s => s.id === state.currentSessionId),
        recentChats: (state): ChatSession[] => {
            return [...state.sessions]
                .sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
                .slice(0, 5) // Top 5 recent
        }
    },
    actions: {
        createSession(title?: string) {
            const id = crypto.randomUUID()
            const newSession: ChatSession = {
                id,
                title: title || 'New Chat',
                messages: [],
                createdAt: new Date(),
                updatedAt: new Date(),
            }
            this.sessions.push(newSession)
            this.currentSessionId = id
            return id
        },
        setCurrentSession(id: string) {
            if (!this.sessions.find(s => s.id === id)) {
                // If session doesn't exist (e.g. from URL), may want to redirect or create placeholder
                // For now, just create it on the fly if needed or handle error
                // console.warn('Session not found', id)
            }
            this.currentSessionId = id
        },
        addMessage(sessionId: string, message: Message) {
            const session = this.sessions.find(s => s.id === sessionId)
            if (session) {
                session.messages.push(message)
                session.updatedAt = new Date()

                // Auto-update title if it's the first user message and title is generic
                if (message.type === 'user' && session.messages.filter(m => m.type === 'user').length === 1 && session.title === 'New Chat') {
                    session.title = message.content.slice(0, 30) + (message.content.length > 30 ? '...' : '')
                }
            }
        },
        deleteSession(sessionId: string) {
            this.sessions = this.sessions.filter(s => s.id !== sessionId)
            if (this.currentSessionId === sessionId) {
                this.currentSessionId = null
            }
        },
        clearHistory() {
            this.sessions = []
            this.currentSessionId = null
        }
    },
    /* persist: true */
    // Persistence requires pinia-plugin-persistedstate. Commenting out to fix TS error for now.
})
