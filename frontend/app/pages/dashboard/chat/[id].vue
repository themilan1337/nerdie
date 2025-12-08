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
  <div class="h-[calc(100vh-4rem)] flex flex-col relative">
    <!-- Chat Header -->
    <div class="absolute top-0 left-0 right-0 z-10 px-6 py-4 flex items-center justify-between bg-zinc-50/80 backdrop-blur-xl border-b border-zinc-200/50">
      <div>
        <h1 class="text-lg font-['Questrial'] text-zinc-900 tracking-tight">{{ chatInfo.title }}</h1>
        <div class="flex items-center gap-2 text-xs text-zinc-500">
          <span>{{ chatInfo.messageCount }} messages</span>
          <span class="w-1 h-1 rounded-full bg-zinc-300"></span>
          <span>{{ chatInfo.createdAt }}</span>
        </div>
      </div>
      <div class="flex items-center gap-1">
        <button class="p-2 rounded-xl hover:bg-zinc-100 transition-colors text-zinc-500 hover:text-zinc-900">
          <Icon icon="hugeicons:download-01" class="w-5 h-5" />
        </button>
        <button class="p-2 rounded-xl hover:bg-zinc-100 transition-colors text-zinc-500 hover:text-zinc-900">
          <Icon icon="hugeicons:more-vertical" class="w-5 h-5" />
        </button>
      </div>
    </div>

    <!-- Messages Container -->
    <div
      ref="messagesContainer"
      class="flex-1 overflow-y-auto pt-24 pb-32 px-4 scroll-smooth"
    >
      <div class="max-w-3xl mx-auto space-y-8">
        <!-- Welcome Message -->
        <div class="text-center py-12">
          <div class="w-16 h-16 bg-white border border-zinc-200 shadow-sm rounded-3xl mx-auto mb-6 flex items-center justify-center">
            <Icon icon="hugeicons:bubble-chat-spark-01" class="w-8 h-8 text-zinc-900" />
          </div>
          <h2 class="text-2xl font-['Questrial'] text-zinc-900 mb-2 tracking-tight">{{ chatInfo.title }}</h2>
          <p class="text-zinc-500 text-sm">Reviewing conversation history and details</p>
        </div>

        <!-- Messages -->
        <div
          v-for="(message, index) in messages"
          :key="message.id"
          class="group flex gap-5 max-w-3xl mx-auto opacity-0 animate-[slideUp_0.4s_ease-out_forwards]"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <!-- Avatar -->
          <div class="flex-shrink-0 mt-1">
            <div
              v-if="message.type === 'assistant'"
              class="w-8 h-8 rounded-xl bg-zinc-900 text-white flex items-center justify-center shadow-sm"
            >
              <Icon icon="hugeicons:ai-brain-01" class="w-4 h-4" />
            </div>
            <div
              v-else
              class="w-8 h-8 rounded-xl bg-white border border-zinc-200 flex items-center justify-center overflow-hidden"
            >
              <img
                v-if="user?.photoURL"
                :src="user.photoURL"
                alt="User"
                class="w-full h-full object-cover"
              />
              <span v-else class="text-xs font-bold text-zinc-700">ME</span>
            </div>
          </div>

          <!-- Content -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1.5">
              <span class="text-sm font-semibold text-zinc-900">
                {{ message.type === 'assistant' ? 'Nerdie AI' : 'You' }}
              </span>
              <span class="text-xs text-zinc-400 font-medium">{{ formatTime(message.timestamp) }}</span>
            </div>

            <div
              class="text-zinc-600 leading-7 font-normal prose prose-zinc prose-p:my-1 prose-headings:text-zinc-900 prose-strong:text-zinc-900 max-w-none text-[15px]"
            >
             {{ message.content }}
            </div>

            <!-- Sources if available -->
            <div v-if="message.sources && message.sources.length" class="mt-4 flex flex-wrap gap-2">
              <div v-for="source in message.sources" :key="source.name" class="flex items-center gap-1.5 px-3 py-1.5 bg-white border border-zinc-200 rounded-lg text-xs text-zinc-600 hover:border-zinc-300 transition-colors cursor-pointer">
                <Icon icon="hugeicons:document-attachment" class="w-3.5 h-3.5 text-zinc-400" />
                <span>{{ source.name }}</span>
                <span class="text-zinc-400 ml-0.5">p. {{ source.page }}</span>
              </div>
            </div>

            <!-- Actions -->
            <div v-if="message.type === 'assistant'" class="flex items-center gap-1 mt-3 opacity-0 group-hover:opacity-100 transition-all duration-200 translate-y-1 group-hover:translate-y-0">
              <button class="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-900 hover:bg-zinc-100 transition-colors" title="Copy">
                <Icon icon="hugeicons:copy-01" class="w-4 h-4" />
              </button>
              <button class="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-900 hover:bg-zinc-100 transition-colors" title="Good response">
                <Icon icon="hugeicons:thumbs-up" class="w-4 h-4" />
              </button>
              <button class="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-900 hover:bg-zinc-100 transition-colors" title="Bad response">
                <Icon icon="hugeicons:thumbs-down" class="w-4 h-4" />
              </button>
              <button class="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-900 hover:bg-zinc-100 transition-colors" title="Regenerate">
                <Icon icon="hugeicons:refresh" class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <!-- Typing Indicator -->
        <div v-if="isTyping" class="flex gap-5 max-w-3xl mx-auto pl-1">
          <div class="w-8 h-8 rounded-xl bg-zinc-900 text-white flex items-center justify-center shadow-sm">
            <Icon icon="hugeicons:ai-brain-01" class="w-4 h-4 animate-pulse" />
          </div>
          <div class="flex items-center gap-1.5 h-8">
            <div class="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce" style="animation-delay: 0s"></div>
            <div class="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
            <div class="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="absolute bottom-6 left-0 right-0 z-20 px-4">
      <div class="max-w-2xl mx-auto w-full">
        <div class="relative group">
          <!-- Subtle Glow -->
          <div class="absolute -inset-1 bg-gradient-to-r from-zinc-200 via-zinc-100 to-zinc-200 rounded-[24px] blur opacity-40 group-hover:opacity-70 transition-opacity duration-500"></div>
          
          <div class="relative bg-white/80 backdrop-blur-xl border border-white/50 shadow-[0_8px_30px_rgb(0,0,0,0.04)] ring-1 ring-zinc-200/50 rounded-[20px] p-2 flex items-end gap-2 transition-all duration-300 hover:shadow-[0_12px_40px_rgb(0,0,0,0.08)]">
            
            <button class="p-3 rounded-xl hover:bg-zinc-100 text-zinc-400 hover:text-zinc-900 transition-colors">
              <Icon icon="hugeicons:attachment-01" class="w-5 h-5" />
            </button>

            <textarea
              v-model="messageInput"
              rows="1"
              placeholder="Ask anything..."
              class="flex-1 py-3 px-1 bg-transparent border-none focus:ring-0 text-zinc-900 placeholder-zinc-400 resize-none max-h-32 text-base"
              @keydown.enter.prevent="handleSendMessage"
              ref="textareaRef"
            ></textarea>

            <button
              @click="handleSendMessage"
              :disabled="!messageInput.trim() || isLoading"
              class="p-2.5 rounded-xl bg-zinc-900 text-white hover:bg-black disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-sm"
            >
              <Icon icon="hugeicons:sent" class="w-5 h-5" />
            </button>
          </div>
        </div>
        
        <div class="text-center mt-3">
          <p class="text-[10px] text-zinc-400 font-medium tracking-wide opacity-60">
            AI can make mistakes. Please verify important information.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom scrollbar for this page */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: transparent;
  border-radius: 4px;
}

.overflow-y-auto:hover::-webkit-scrollbar-thumb {
  background: #e4e4e7;
}

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
