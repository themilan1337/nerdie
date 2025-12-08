<script setup lang="ts">
import { ref } from 'vue'
import { Icon } from '@iconify/vue'

definePageMeta({
  layout: 'dashboard'
})

const router = useRouter()
const selectedPrompt = ref('')

const promptSuggestions = [
  {
    category: 'General',
    icon: 'hugeicons:bubble-chat',
    color: 'from-blue-400 to-blue-600',
    prompts: [
      'Explain a complex concept in simple terms',
      'Summarize the key points from a document',
      'Compare and contrast two ideas',
    ]
  },
  {
    category: 'Creative',
    icon: 'hugeicons:bulb',
    color: 'from-yellow-400 to-orange-500',
    prompts: [
      'Generate creative ideas for a project',
      'Write a compelling introduction',
      'Brainstorm innovative solutions',
    ]
  },
  {
    category: 'Technical',
    icon: 'hugeicons:code',
    color: 'from-purple-400 to-purple-600',
    prompts: [
      'Explain a programming concept',
      'Debug code and find issues',
      'Suggest best practices for development',
    ]
  },
  {
    category: 'Research',
    icon: 'hugeicons:book-open-01',
    color: 'from-green-400 to-green-600',
    prompts: [
      'Find information on a specific topic',
      'Analyze research findings',
      'Create a comprehensive overview',
    ]
  },
]

const recentTopics = [
  { title: 'Machine Learning Basics', time: '2 hours ago' },
  { title: 'Python Data Analysis', time: '1 day ago' },
  { title: 'Web Development Tips', time: '2 days ago' },
]

const handleStartChat = (prompt?: string) => {
  // In production, this would create a new chat and navigate to it
  const chatId = Math.floor(Math.random() * 10000)
  if (prompt) {
    // Store the initial prompt and navigate
    console.log('Starting chat with prompt:', prompt)
  }
  router.push(`/dashboard/chat/${chatId}`)
}

const handlePromptClick = (prompt: string) => {
  selectedPrompt.value = prompt
}
</script>

<template>
  <div class="max-w-4xl mx-auto py-12 px-6">
    <!-- Header -->
    <div class="text-center mb-16 space-y-4">
      <div class="w-20 h-20 bg-black text-white rounded-[2rem] flex items-center justify-center mx-auto shadow-2xl shadow-zinc-200 mb-8 transform transition-transform hover:scale-105 duration-500">
        <Icon icon="hugeicons:ai-brain-01" class="w-10 h-10" />
      </div>
      <h1 class="text-5xl font-['Questrial'] font-light tracking-tight text-zinc-900">
        Good morning, Milan.
      </h1>
      <p class="text-xl text-zinc-400 font-light">
        What shall we explore today?
      </p>
    </div>

    <!-- Search/Input Area -->
    <div class="relative max-w-2xl mx-auto mb-20 group">
      <div class="absolute inset-0 bg-gradient-to-r from-zinc-200 via-zinc-100 to-zinc-200 rounded-full blur-xl opacity-20 group-hover:opacity-40 transition-opacity duration-700"></div>
      <div class="relative">
        <input
          v-model="selectedPrompt"
          type="text"
          placeholder="Ask anything..."
          class="w-full pl-8 pr-32 py-5 bg-white border border-zinc-200 rounded-full text-lg font-light text-zinc-900 placeholder-zinc-300 focus:outline-none focus:ring-2 focus:ring-black/5 focus:border-zinc-300 transition-all shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(0,0,0,0.08)]"
          @keydown.enter="handleStartChat(selectedPrompt)"
        />
        <button
          @click="handleStartChat(selectedPrompt)"
          :disabled="!selectedPrompt.trim()"
          class="absolute right-2 top-2 bottom-2 px-6 bg-black text-white rounded-full font-medium hover:bg-zinc-800 disabled:opacity-0 disabled:scale-90 transition-all duration-300 flex items-center gap-2"
        >
          <span>Start</span>
          <Icon icon="hugeicons:arrow-right-01" class="w-4 h-4" />
        </button>
      </div>
    </div>

    <!-- Categories Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-20">
      <div
        v-for="category in promptSuggestions"
        :key="category.category"
        class="group glass-panel rounded-[2rem] p-8 hover:border-zinc-300 transition-all duration-500 hover:-translate-y-1 relative overflow-hidden"
      >
        <div class="absolute top-0 right-0 p-8 opacity-0 group-hover:opacity-10 translate-x-4 group-hover:translate-x-0 transition-all duration-500">
          <Icon :icon="category.icon" class="w-32 h-32 text-black" />
        </div>

        <div class="relative z-10">
          <div class="flex items-center gap-4 mb-6">
            <div class="w-12 h-12 rounded-2xl bg-zinc-50 flex items-center justify-center group-hover:bg-black transition-colors duration-500">
              <Icon :icon="category.icon" class="w-6 h-6 text-zinc-900 group-hover:text-white transition-colors duration-500" />
            </div>
            <h3 class="text-lg font-medium text-zinc-900">{{ category.category }}</h3>
          </div>

          <div class="space-y-3">
            <button
              v-for="prompt in category.prompts"
              :key="prompt"
              @click="handleStartChat(prompt)"
              class="w-full text-left p-3 rounded-xl hover:bg-zinc-50 text-zinc-500 hover:text-zinc-900 transition-all text-sm font-light group/btn flex items-center justify-between"
            >
              <span>{{ prompt }}</span>
              <Icon icon="hugeicons:arrow-right-01" class="w-4 h-4 opacity-0 group-hover/btn:opacity-100 -translate-x-2 group-hover/btn:translate-x-0 transition-all" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Features -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <button
        @click="handleStartChat('Summarize the main points from my documents')"
        class="group p-6 rounded-3xl bg-zinc-50 hover:bg-zinc-900 transition-colors duration-500 text-left relative overflow-hidden"
      >
        <div class="absolute top-4 right-4 w-2 h-2 rounded-full bg-zinc-300 group-hover:bg-zinc-700 transition-colors"></div>
        <Icon icon="hugeicons:book-open-01" class="w-8 h-8 text-zinc-900 group-hover:text-white mb-4 transition-colors" />
        <h3 class="font-medium text-zinc-900 group-hover:text-white mb-1 transition-colors">Quick Summary</h3>
        <p class="text-sm text-zinc-500 group-hover:text-zinc-400 transition-colors">Get key insights from documents</p>
      </button>

      <button
        @click="handleStartChat('Help me understand complex topics')"
        class="group p-6 rounded-3xl bg-zinc-50 hover:bg-zinc-900 transition-colors duration-500 text-left relative overflow-hidden"
      >
        <div class="absolute top-4 right-4 w-2 h-2 rounded-full bg-zinc-300 group-hover:bg-zinc-700 transition-colors"></div>
        <Icon icon="hugeicons:calculator-01" class="w-8 h-8 text-zinc-900 group-hover:text-white mb-4 transition-colors" />
        <h3 class="font-medium text-zinc-900 group-hover:text-white mb-1 transition-colors">Deep Analysis</h3>
        <p class="text-sm text-zinc-500 group-hover:text-zinc-400 transition-colors">Explore topics in detail</p>
      </button>

      <button
        @click="handleStartChat('Search my knowledge base')"
        class="group p-6 rounded-3xl bg-zinc-50 hover:bg-zinc-900 transition-colors duration-500 text-left relative overflow-hidden"
      >
        <div class="absolute top-4 right-4 w-2 h-2 rounded-full bg-zinc-300 group-hover:bg-zinc-700 transition-colors"></div>
        <Icon icon="hugeicons:globe-01" class="w-8 h-8 text-zinc-900 group-hover:text-white mb-4 transition-colors" />
        <h3 class="font-medium text-zinc-900 group-hover:text-white mb-1 transition-colors">Knowledge Search</h3>
        <p class="text-sm text-zinc-500 group-hover:text-zinc-400 transition-colors">Find specific information</p>
      </button>
    </div>
  </div>
</template>
