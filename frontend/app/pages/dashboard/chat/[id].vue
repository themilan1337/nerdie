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
          v-for="message in messages"
          :key="message.id"
          :class="[
            'flex gap-4',
            message.type === 'user' ? 'justify-end' : 'justify-start'
          ]"
        >
          <!-- Assistant Avatar -->
          <div
            v-if="message.type === 'assistant'"
            class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center flex-shrink-0"
          >
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>

          <!-- Message Content -->
          <div :class="['max-w-2xl', message.type === 'user' ? 'order-first' : '']">
            <div
              :class="[
                'rounded-2xl px-5 py-3',
                message.type === 'user'
                  ? 'bg-black text-white'
                  : 'bg-white border border-gray-200'
              ]"
            >
              <p class="text-sm leading-relaxed whitespace-pre-wrap" v-html="message.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>')"></p>

              <!-- Sources -->
              <div v-if="message.type === 'assistant' && message.sources" class="mt-4 pt-4 border-t border-gray-200">
                <p class="text-xs font-medium text-gray-500 mb-2">Sources:</p>
                <div class="flex flex-wrap gap-2">
                  <div
                    v-for="(source, idx) in message.sources"
                    :key="idx"
                    class="inline-flex items-center gap-1 px-2 py-1 bg-gray-50 rounded-lg text-xs text-gray-600"
                  >
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    {{ source.name }} (p.{{ source.page }})
                  </div>
                </div>
              </div>
            </div>

            <!-- Message Actions -->
            <div class="flex items-center gap-2 mt-2 px-2">
              <span class="text-xs text-gray-400">{{ message.timestamp }}</span>

              <div v-if="message.type === 'assistant'" class="flex items-center gap-1 ml-auto">
                <button
                  @click="handleCopyMessage(message.content)"
                  class="p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                  title="Copy"
                >
                  <Icon icon="hugeicons:copy-01" class="w-3.5 h-3.5 text-gray-400" />
                </button>
                <button
                  @click="handleFeedback(message.id, 'positive')"
                  class="p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                  title="Good response"
                >
                  <Icon icon="hugeicons:thumbs-up" class="w-3.5 h-3.5 text-gray-400" />
                </button>
                <button
                  @click="handleFeedback(message.id, 'negative')"
                  class="p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                  title="Bad response"
                >
                  <Icon icon="hugeicons:thumbs-down" class="w-3.5 h-3.5 text-gray-400" />
                </button>
                <button
                  @click="handleRegenerateResponse"
                  class="p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                  title="Regenerate"
                >
                  <Icon icon="hugeicons:refresh" class="w-3.5 h-3.5 text-gray-400" />
                </button>
              </div>
            </div>
          </div>

          <!-- User Avatar -->
          <div
            v-if="message.type === 'user'"
            class="w-8 h-8 rounded-full bg-gradient-to-br from-orange-400 to-pink-500 flex items-center justify-center flex-shrink-0"
          >
            <span class="text-white font-bold text-sm ins">U</span>
          </div>
        </div>

        <!-- Loading Indicator -->
        <div v-if="isLoading" class="flex gap-4">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center flex-shrink-0">
            <svg class="w-5 h-5 text-white animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <div class="bg-white border border-gray-200 rounded-2xl px-5 py-3">
            <div class="flex gap-1">
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="border-t border-gray-200 bg-white px-6 py-4">
      <div class="max-w-4xl mx-auto">
        <div class="flex items-end gap-3">
          <button class="p-3 rounded-xl hover:bg-gray-100 transition-colors">
            <Icon icon="hugeicons:attachment" class="w-5 h-5 text-gray-600" />
          </button>

          <div class="flex-1">
            <textarea
              v-model="messageInput"
              @keydown.enter.prevent="handleSendMessage"
              placeholder="Ask a question..."
              rows="1"
              class="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
              style="max-height: 200px;"
            />
          </div>

          <button
            @click="handleSendMessage"
            :disabled="!messageInput.trim() || isLoading"
            :class="[
              'p-3 rounded-xl transition-all',
              messageInput.trim() && !isLoading
                ? 'bg-black text-white hover:bg-gray-800'
                : 'bg-gray-100 text-gray-400 cursor-not-allowed'
            ]"
          >
            <Icon icon="hugeicons:sent" class="w-5 h-5" />
          </button>
        </div>

        <p class="text-xs text-gray-400 mt-2 text-center">
          Press Enter to send • Responses are generated using RAG + Gemini
        </p>
      </div>
    </div>
  </div>
</template>
