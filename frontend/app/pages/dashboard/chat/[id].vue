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
  <div class="h-[calc(100vh-4rem)] flex flex-col">
    <!-- Chat Header -->
    <div class="border-b border-gray-200 px-6 py-4 bg-white">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-gray-900 ins">{{ chatInfo.title }}</h1>
          <p class="text-sm text-gray-500 mt-1">{{ chatInfo.messageCount }} messages • {{ chatInfo.createdAt }}</p>
        </div>
        <div class="flex items-center gap-2">
          <button class="p-2 rounded-lg hover:bg-gray-100 transition-colors">
            <Icon icon="hugeicons:download-01" class="w-5 h-5 text-gray-600" />
          </button>
          <button class="p-2 rounded-lg hover:bg-gray-100 transition-colors">
            <Icon icon="hugeicons:more-vertical" class="w-5 h-5 text-gray-600" />
          </button>
        </div>
      </div>
    </div>

    <!-- Messages Container -->
    <div
      ref="messagesContainer"
      class="flex-1 overflow-y-auto px-6 py-6 bg-gray-50"
    >
      <div class="max-w-4xl mx-auto space-y-6">
        <!-- Welcome Message -->
        <div class="text-center py-8">
          <div class="w-16 h-16 bg-gradient-to-br from-orange-400 to-pink-500 rounded-2xl mx-auto mb-4 flex items-center justify-center">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-900 ins mb-2">{{ chatInfo.title }}</h2>
          <p class="text-gray-500">Ask anything based on your knowledge base</p>
        </div>

        <!-- Messages -->
        <div
          v-for="(message, index) in messages"
          :key="message.id"
          class="group flex gap-6 max-w-4xl mx-auto opacity-0 animate-[slideUp_0.4s_ease-out_forwards]"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <!-- Avatar -->
          <div class="flex-shrink-0 mt-1">
            <div
              v-if="message.type === 'assistant'"
              class="w-8 h-8 rounded-full bg-black text-white flex items-center justify-center shadow-md"
            >
              <Icon icon="hugeicons:ai-brain-01" class="w-4 h-4" />
            </div>
            <div
              v-else
              class="w-8 h-8 rounded-full bg-zinc-100 border border-zinc-200 flex items-center justify-center"
            >
              <img
                v-if="user?.photoURL"
                :src="user.photoURL"
                alt="User"
                class="w-full h-full rounded-full object-cover"
              />
              <span v-else class="text-xs font-medium text-zinc-600">ME</span>
            </div>
          </div>

          <!-- Content -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <span class="text-sm font-medium text-zinc-900">
                {{ message.type === 'assistant' ? 'Nerdie AI' : 'You' }}
              </span>
              <span class="text-xs text-zinc-300">{{ formatTime(message.timestamp) }}</span>
            </div>

            <div
              class="text-zinc-600 leading-relaxed font-light prose prose-zinc max-w-none"
              :class="{'bg-zinc-50 p-4 rounded-2xl rounded-tl-sm': message.type === 'user'}"
            >
             {{ message.content }}
            </div>

            <!-- Actions -->
            <div v-if="message.type === 'assistant'" class="flex items-center gap-2 mt-3 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
              <button class="action-btn" title="Copy">
                <Icon icon="hugeicons:copy-01" class="w-3.5 h-3.5" />
              </button>
              <button class="action-btn" title="Good response">
                <Icon icon="hugeicons:thumbs-up" class="w-3.5 h-3.5" />
              </button>
              <button class="action-btn" title="Bad response">
                <Icon icon="hugeicons:thumbs-down" class="w-3.5 h-3.5" />
              </button>
              <button class="action-btn" title="Regenerate">
                <Icon icon="hugeicons:refresh" class="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Typinng Indicator -->
      <div v-if="isTyping" class="flex gap-6 max-w-4xl mx-auto">
        <div class="w-8 h-8 rounded-full bg-black text-white flex items-center justify-center shadow-lg">
          <Icon icon="hugeicons:ai-brain-01" class="w-4 h-4 animate-pulse" />
        </div>
        <div class="flex items-center gap-1.5 h-8">
          <div class="w-1.5 h-1.5 bg-zinc-300 rounded-full animate-bounce" style="animation-delay: 0s"></div>
          <div class="w-1.5 h-1.5 bg-zinc-300 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
          <div class="w-1.5 h-1.5 bg-zinc-300 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="flex-shrink-0 pt-6 pb-2 max-w-4xl mx-auto w-full z-10 bg-zinc-50">
      <div class="relative group">
        <div class="absolute inset-0 bg-gradient-to-r from-zinc-200 to-zinc-100 rounded-[2rem] blur opacity-20 group-hover:opacity-40 transition-opacity"></div>
        <div class="relative bg-white border border-zinc-200 shadow-[0_8px_40px_-10px_rgba(0,0,0,0.05)] rounded-[2rem] p-2 flex items-end gap-2 transition-all duration-300 hover:shadow-[0_12px_50px_-10px_rgba(0,0,0,0.08)] hover:border-zinc-300">
          
          <button class="p-3 rounded-full hover:bg-zinc-50 text-zinc-400 hover:text-zinc-900 transition-colors">
            <Icon icon="hugeicons:attachment-01" class="w-5 h-5" />
          </button>

          <textarea
            v-model="messageInput"
            rows="1"
            placeholder="Ask anything..."
            class="flex-1 py-3 px-2 bg-transparent border-none focus:ring-0 text-zinc-900 placeholder-zinc-400 resize-none max-h-32 font-light"
            @keydown.enter.prevent="handleSendMessage"
            ref="textareaRef"
          ></textarea>

          <button
            @click="handleSendMessage"
            :disabled="!messageInput.trim() || isLoading"
            class="p-3 rounded-full bg-black text-white hover:bg-zinc-800 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-md hover:shadow-lg hover:scale-105"
          >
            <Icon icon="hugeicons:sent" class="w-5 h-5" />
          </button>
        </div>
        <div class="text-center mt-3">
          <p class="text-[10px] text-zinc-400 font-medium tracking-wide uppercase opacity-70">
            Nerdie AI can make mistakes. Check important info.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>


@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
