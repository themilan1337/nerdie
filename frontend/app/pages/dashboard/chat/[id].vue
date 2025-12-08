<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { Icon } from '@iconify/vue'

definePageMeta({
  layout: 'dashboard'
})

const route = useRoute()
const chatId = route.params.id

const messageInput = ref('')
const messagesContainer = ref<HTMLElement | null>(null)
const isLoading = ref(false)
const isTyping = ref(false)
const textareaRef = ref<HTMLTextAreaElement | null>(null)
const user = ref(null) // Add user ref for avatar

// Format timestamp function
const formatTime = (timestamp: string | Date) => {
  if (typeof timestamp === 'string') {
    return timestamp
  }
  return new Date(timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}

const chatInfo = ref({
  title: 'Machine Learning Basics',
  createdAt: '2 hours ago',
  messageCount: 12
})

const messages = ref([
  {
    id: 1,
    type: 'user',
    content: 'What are the fundamental concepts of machine learning?',
    timestamp: '10:30 AM',
  },
  {
    id: 2,
    type: 'assistant',
    content: 'Machine learning is a subset of artificial intelligence that focuses on developing systems that can learn from and make decisions based on data. The fundamental concepts include:\n\n1. **Supervised Learning**: Training models on labeled data\n2. **Unsupervised Learning**: Finding patterns in unlabeled data\n3. **Features**: Input variables used for predictions\n4. **Training**: Process of teaching the model\n5. **Validation**: Testing model performance\n\nThese concepts form the foundation of most ML applications.',
    timestamp: '10:30 AM',
    sources: [
      { name: 'ML_Fundamentals.pdf', page: 12 },
      { name: 'AI_Introduction.docx', page: 5 }
    ]
  },
  {
    id: 3,
    type: 'user',
    content: 'Can you explain supervised learning in more detail?',
    timestamp: '10:32 AM',
  },
  {
    id: 4,
    type: 'assistant',
    content: 'Supervised learning is a type of machine learning where the model learns from labeled training data. Here\'s a detailed breakdown:\n\n**Key Components:**\n- Input data (features)\n- Output labels (targets)\n- Training algorithm\n- Model parameters\n\n**Common Algorithms:**\n- Linear Regression\n- Decision Trees\n- Neural Networks\n- Support Vector Machines\n\nThe model learns by finding patterns between inputs and outputs, then uses these patterns to make predictions on new, unseen data.',
    timestamp: '10:32 AM',
    sources: [
      { name: 'Supervised_Learning_Guide.pdf', page: 3 }
    ]
  },
])

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const handleSendMessage = async () => {
  if (!messageInput.value.trim() || isLoading.value) return

  const userMessage = {
    id: messages.value.length + 1,
    type: 'user',
    content: messageInput.value,
    timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
  }

  messages.value.push(userMessage)
  messageInput.value = ''
  isLoading.value = true
  scrollToBottom()

  // Simulate AI response
  setTimeout(() => {
    const aiMessage = {
      id: messages.value.length + 1,
      type: 'assistant',
      content: 'This is a simulated response. In production, this would connect to your RAG system with Gemini API to provide contextual answers based on your knowledge base.',
      timestamp: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
      sources: [
        { name: 'Example_Document.pdf', page: 1 }
      ]
    }
    messages.value.push(aiMessage)
    isLoading.value = false
    scrollToBottom()
  }, 1500)
}

const handleCopyMessage = (content: string) => {
  navigator.clipboard.writeText(content)
  console.log('Message copied to clipboard')
}

const handleRegenerateResponse = () => {
  console.log('Regenerating response...')
}

const handleFeedback = (messageId: number, type: 'positive' | 'negative') => {
  console.log(`Feedback for message ${messageId}: ${type}`)
}
</script>

<template>
  <div>
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-4xl font-['Questrial'] font-light tracking-tight text-zinc-900 mb-3">{{ chatInfo.title }}</h1>
      <p class="text-zinc-500 font-light text-base">{{ chatInfo.messageCount }} messages • {{ chatInfo.createdAt }}</p>
    </div>

    <!-- Messages Container -->
    <div class="max-w-3xl pb-32">
      <div class="space-y-6">

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
                v-if="user?.photoURL"
                :src="user.photoURL"
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

            <div class="text-zinc-600 leading-relaxed text-[15px] whitespace-pre-wrap">
             {{ message.content }}
            </div>

            <!-- Sources if available -->
            <div v-if="message.sources && message.sources.length" class="mt-3 flex flex-wrap gap-2">
              <div v-for="source in message.sources" :key="source.name" class="flex items-center gap-1.5 px-3 py-1.5 bg-zinc-50 border border-zinc-200 rounded-xl text-xs text-zinc-600 hover:border-zinc-300 transition-colors cursor-pointer">
                <Icon icon="hugeicons:file-02" class="w-3.5 h-3.5 text-zinc-400" />
                <span class="font-medium">{{ source.name }}</span>
                <span class="text-zinc-400">• p.{{ source.page }}</span>
              </div>
            </div>

            <!-- Actions -->
            <div v-if="message.type === 'assistant'" class="flex items-center gap-1 mt-3 opacity-0 group-hover:opacity-100 transition-opacity">
              <button class="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-900 hover:bg-zinc-100 transition-colors" title="Copy">
                <Icon icon="hugeicons:copy-01" class="w-4 h-4" />
              </button>
              <button class="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-900 hover:bg-zinc-100 transition-colors" title="Good">
                <Icon icon="hugeicons:thumbs-up" class="w-4 h-4" />
              </button>
              <button class="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-900 hover:bg-zinc-100 transition-colors" title="Bad">
                <Icon icon="hugeicons:thumbs-down" class="w-4 h-4" />
              </button>
              <button class="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-900 hover:bg-zinc-100 transition-colors" title="Regenerate">
                <Icon icon="hugeicons:refresh" class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <!-- Typing Indicator -->
        <div v-if="isTyping" class="flex gap-4">
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
    <div class="fixed bottom-0 left-0 right-0 bg-gradient-to-t from-zinc-50 via-zinc-50 to-transparent pt-8 pb-6 z-30 transition-all duration-300">
      <div class="max-w-3xl mx-auto" style="padding-left: calc(2rem + var(--removed-left-scroll-gutter, 0px)); padding-right: calc(2rem + var(--removed-right-scroll-gutter, 0px));">
        <div class="bg-white border border-zinc-200 rounded-2xl shadow-sm hover:shadow-md transition-shadow p-3 flex items-center gap-3">
          <button class="p-2 rounded-xl hover:bg-zinc-100 text-zinc-400 hover:text-zinc-900 transition-colors flex-shrink-0">
            <Icon icon="hugeicons:attachment-01" class="w-5 h-5" />
          </button>

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
