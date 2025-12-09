<script setup lang="ts">
import { ref, nextTick, onMounted, watch, computed } from 'vue'
import { Icon } from '@iconify/vue'
import { marked } from 'marked'
import { useChatStore } from '../../../../stores/chat'
import { useRagApi } from '../../../../composables/useRagApi'

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

// Configure marked for better rendering
marked.setOptions({
  breaks: true,
  gfm: true
})

const route = useRoute()
const router = useRouter()
const chatStore = useChatStore()
const { fetchRagQuery } = useRagApi()
const { userData } = useAuth()

const chatId = route.params.id as string
const messageInput = ref('')
const messagesContainer = ref<HTMLElement | null>(null)
const isLoading = ref(false)
const textareaRef = ref<HTMLTextAreaElement | null>(null)

// Initialize session
onMounted(async () => {
    if (chatId === 'new') {
        const newId = chatStore.createSession()
        router.replace(`/dashboard/chat/${newId}`)
    } else {
        chatStore.setCurrentSession(chatId)
        
        // Check for auto-prompt from new chat page
        const prompt = route.query.prompt as string
        if (prompt) {
            messageInput.value = prompt
            // Remove query param to clean URL
            router.replace({ query: undefined })
            // Wait for session init then send
            await nextTick()
            handleSendMessage()
        }
    }
    scrollToBottom()
})

const currentSession = computed(() => chatStore.currentSession)
const messages = computed(() => currentSession.value?.messages || [])
const chatTitle = computed(() => currentSession.value?.title || 'New Chat')

// Auto-scroll
watch(() => messages.value.length, () => {
    scrollToBottom()
})

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// Format timestamp function
const formatTime = (timestamp: string | Date | undefined) => {
  if (!timestamp) return ''
  if (typeof timestamp === 'string') {
     // If it's a simple time string like "10:30 AM", return it.
     // But real data will likely be ISO string.
     if(timestamp.includes('M') && timestamp.length < 10) return timestamp 
     return new Date(timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
  }
  return new Date(timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}


const handleSendMessage = async () => {
  if (!messageInput.value.trim() || isLoading.value) return

  const content = messageInput.value
  messageInput.value = ''
  
  // Add user message
  chatStore.addMessage(chatId, {
      id: Date.now(),
      type: 'user',
      content: content,
      timestamp: new Date()
  })

  isLoading.value = true
  scrollToBottom()

  try {
      const response: any = await fetchRagQuery(content, userData.value?.uid || 'anon')
      
      // Add assistant message
      chatStore.addMessage(chatId, {
          id: Date.now() + 1,
          type: 'assistant',
          content: response.answer,
          timestamp: new Date(),
          sources: response.chunks
            .map((c: any) => ({
                name: c.metadata?.source || 'Unknown',
                page: c.metadata?.page
            }))
            .filter((s: any) => s.name !== 'Unknown')
      })

  } catch (error) {
      console.error('Failed to get answer:', error)
      chatStore.addMessage(chatId, {
          id: Date.now() + 1,
          type: 'assistant',
          content: 'Sorry, I encountered an error retrieving the information.',
          timestamp: new Date()
      })
  } finally {
      isLoading.value = false
      scrollToBottom()
  }
}

const handleCopyMessage = (content: string) => {
  navigator.clipboard.writeText(content)
}

const handleRegenerateResponse = () => {
  // Logic to regenerate could be implemented here
  // For now, just a placeholder or could re-send last user message
  const lastUserMsg = messages.value.filter((m: any) => m.type === 'user').pop()
  if (lastUserMsg) {
      messageInput.value = lastUserMsg.content
      handleSendMessage()
  }
}

// Render markdown content
const renderMarkdown = (content: string) => {
  return marked.parse(content)
}

</script>

<template>
  <div class="flex flex-col h-[calc(100vh-6rem)]">
    <!-- Page Header -->
    <div class="mb-4 flex-shrink-0">
      <h1 class="text-4xl font-['Questrial'] font-light tracking-tight text-zinc-900 mb-3">{{ chatTitle }}</h1>
      <p class="text-zinc-500 font-light text-base">{{ messages.length }} messages</p>
    </div>

    <!-- Messages Container -->
    <div 
        ref="messagesContainer"
        class="flex-1 overflow-y-auto pb-32 scroll-smooth"
    >
      <div class="space-y-6 max-w-3xl">

        <!-- Messages -->
        <div
          v-for="(message, index) in messages"
          :key="message.id"
          class="group flex gap-4"
        >
          <!-- Avatar -->
          <div class="flex-shrink-0">
            <div
              v-if="message.type === 'assistant'"
              class="w-10 h-10 rounded-full bg-zinc-900 text-white flex items-center justify-center"
            >
              <Icon icon="hugeicons:ai-brain-01" class="w-5 h-5" />
            </div>
            <div
              v-else
              class="w-10 h-10 rounded-full bg-zinc-100 border border-zinc-200 flex items-center justify-center overflow-hidden"
            >
              <img
                v-if="userData?.photoUrl"
                :src="userData.photoUrl"
                alt="User"
                class="w-full h-full object-cover"
              />
              <span v-else class="text-xs font-medium text-zinc-600">U</span>
            </div>
          </div>

          <!-- Content -->
          <div class="flex-1 min-w-0 pt-1">
            <div class="flex items-center gap-2 mb-2">
              <span class="text-sm font-medium text-zinc-900">
                {{ message.type === 'assistant' ? 'Nerdie AI' : 'You' }}
              </span>
              <span class="text-xs text-zinc-400">{{ formatTime(message.timestamp) }}</span>
            </div>

            <!-- Message content with markdown support -->
            <div
              v-if="message.type === 'assistant'"
              class="prose prose-sm prose-zinc max-w-none text-zinc-600 leading-relaxed"
              v-html="renderMarkdown(message.content)"
            ></div>
            <div
              v-else
              class="text-zinc-600 leading-relaxed text-[15px] whitespace-pre-wrap"
            >
              {{ message.content }}
            </div>

            <!-- Sources if available -->
            <div v-if="message.sources && message.sources.length" class="mt-3 flex flex-wrap gap-2">
              <div v-for="(source, idx) in message.sources" :key="idx" class="flex items-center gap-1.5 px-3 py-1.5 bg-zinc-50 border border-zinc-200 rounded-xl text-xs text-zinc-600 hover:border-zinc-300 transition-colors cursor-pointer">
                <Icon icon="hugeicons:file-02" class="w-3.5 h-3.5 text-zinc-400" />
                <span class="font-medium max-w-[150px] truncate">{{ source.name }}</span>
                <span v-if="source.page" class="text-zinc-400">• p.{{ source.page }}</span>
              </div>
            </div>

            <!-- Actions -->
            <div v-if="message.type === 'assistant'" class="flex items-center gap-1 mt-3 opacity-0 group-hover:opacity-100 transition-opacity">
              <button @click="handleCopyMessage(message.content)" class="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-900 hover:bg-zinc-100 transition-colors" title="Copy">
                <Icon icon="hugeicons:copy-01" class="w-4 h-4" />
              </button>
              <button @click="handleRegenerateResponse" class="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-900 hover:bg-zinc-100 transition-colors" title="Regenerate">
                <Icon icon="hugeicons:refresh" class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <!-- Loading Indicator -->
        <div v-if="isLoading" class="flex gap-4">
          <div class="w-10 h-10 rounded-full bg-zinc-900 text-white flex items-center justify-center">
            <Icon icon="hugeicons:ai-brain-01" class="w-5 h-5 animate-pulse" />
          </div>
          <div class="flex items-center gap-1.5 pt-2">
            <div class="w-2 h-2 bg-zinc-400 rounded-full animate-bounce" style="animation-delay: 0s"></div>
            <div class="w-2 h-2 bg-zinc-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
            <div class="w-2 h-2 bg-zinc-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="fixed bottom-0 left-0 right-0 bg-gradient-to-t from-zinc-50 via-zinc-50 to-transparent pt-8 pb-6 z-30 pointer-events-none">
      <div class="max-w-3xl mx-auto pointer-events-auto">
        <div class="bg-white border border-zinc-200 rounded-2xl shadow-sm hover:shadow-md transition-shadow p-3 flex items-center gap-3">
          <textarea
            v-model="messageInput"
            rows="1"
            placeholder="Ask anything..."
            class="flex-1 py-2 px-2 bg-transparent border-none focus:ring-0 text-zinc-900 placeholder-zinc-400 resize-none max-h-32 text-[15px] focus:outline-none"
            @keydown.enter.prevent="handleSendMessage"
            ref="textareaRef"
          ></textarea>

          <button
            @click="handleSendMessage"
            :disabled="!messageInput.trim() || isLoading"
            class="p-2.5 rounded-xl bg-zinc-900 text-white hover:bg-black disabled:opacity-50 disabled:cursor-not-allowed transition-all flex-shrink-0"
          >
            <Icon icon="hugeicons:sent" class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
