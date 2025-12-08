<script setup lang="ts">
import { ref } from 'vue'
import { MessageSquare, Lightbulb, Code, BookOpen, Calculator, Globe, Sparkles } from 'lucide-vue-next'

definePageMeta({
  layout: 'dashboard'
})

const router = useRouter()
const selectedPrompt = ref('')

const promptSuggestions = [
  {
    category: 'General',
    icon: MessageSquare,
    color: 'from-blue-400 to-blue-600',
    prompts: [
      'Explain a complex concept in simple terms',
      'Summarize the key points from a document',
      'Compare and contrast two ideas',
    ]
  },
  {
    category: 'Creative',
    icon: Lightbulb,
    color: 'from-yellow-400 to-orange-500',
    prompts: [
      'Generate creative ideas for a project',
      'Write a compelling introduction',
      'Brainstorm innovative solutions',
    ]
  },
  {
    category: 'Technical',
    icon: Code,
    color: 'from-purple-400 to-purple-600',
    prompts: [
      'Explain a programming concept',
      'Debug code and find issues',
      'Suggest best practices for development',
    ]
  },
  {
    category: 'Research',
    icon: BookOpen,
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
  <div class="min-h-[calc(100vh-4rem)] bg-gradient-to-br from-gray-50 to-white">
    <div class="max-w-5xl mx-auto px-6 py-12">
      <!-- Header -->
      <div class="text-center mb-12">
        <div class="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-orange-400 to-pink-500 rounded-3xl mb-6 shadow-lg">
          <Sparkles class="w-10 h-10 text-white" />
        </div>
        <h1 class="text-4xl md:text-5xl font-bold text-gray-900 ins mb-4">
          Start a New Chat
        </h1>
        <p class="text-lg text-gray-500 max-w-2xl mx-auto">
          Ask anything and get answers powered by your knowledge base with RAG + Gemini AI
        </p>
      </div>

      <!-- Main Input -->
      <div class="mb-12">
        <div class="relative">
          <textarea
            v-model="selectedPrompt"
            @keydown.enter.ctrl="handleStartChat(selectedPrompt)"
            placeholder="What would you like to know?"
            rows="4"
            class="w-full px-6 py-4 bg-white border-2 border-gray-200 rounded-2xl text-lg resize-none focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all shadow-sm hover:shadow-md"
          />
          <button
            @click="handleStartChat(selectedPrompt)"
            :disabled="!selectedPrompt.trim()"
            :class="[
              'absolute bottom-4 right-4 px-6 py-2.5 rounded-xl font-medium ins transition-all flex items-center gap-2',
              selectedPrompt.trim()
                ? 'bg-black text-white hover:bg-gray-800 shadow-md hover:shadow-lg'
                : 'bg-gray-100 text-gray-400 cursor-not-allowed'
            ]"
          >
            <MessageSquare class="w-4 h-4" />
            Start Chat
          </button>
        </div>
        <p class="text-sm text-gray-400 mt-3 text-center">
          Press Ctrl + Enter to send, or click the button
        </p>
      </div>

      <!-- Prompt Suggestions -->
      <div class="mb-12">
        <h2 class="text-xl font-bold text-gray-900 ins mb-6">Suggested Prompts</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div
            v-for="category in promptSuggestions"
            :key="category.category"
            class="bg-white rounded-2xl border border-gray-200 p-6 hover:shadow-lg transition-all"
          >
            <div class="flex items-center gap-3 mb-4">
              <div :class="['w-10 h-10 rounded-xl flex items-center justify-center bg-gradient-to-br', category.color]">
                <component :is="category.icon" class="w-5 h-5 text-white" />
              </div>
              <h3 class="font-bold text-gray-900 ins text-lg">{{ category.category }}</h3>
            </div>
            <div class="space-y-2">
              <button
                v-for="(prompt, idx) in category.prompts"
                :key="idx"
                @click="handlePromptClick(prompt)"
                class="w-full text-left px-4 py-3 bg-gray-50 hover:bg-gray-100 rounded-xl text-sm text-gray-700 transition-all group"
              >
                <div class="flex items-center justify-between">
                  <span>{{ prompt }}</span>
                  <svg class="w-4 h-4 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Start Templates -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <button
          @click="handleStartChat('Summarize the main points from my documents')"
          class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white hover:shadow-xl transition-all group"
        >
          <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mb-4">
            <BookOpen class="w-6 h-6" />
          </div>
          <h3 class="font-bold ins text-lg mb-2">Quick Summary</h3>
          <p class="text-sm text-blue-100">Get key insights from your documents</p>
        </button>

        <button
          @click="handleStartChat('Help me understand complex topics')"
          class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl p-6 text-white hover:shadow-xl transition-all group"
        >
          <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mb-4">
            <Calculator class="w-6 h-6" />
          </div>
          <h3 class="font-bold ins text-lg mb-2">Deep Analysis</h3>
          <p class="text-sm text-purple-100">Explore topics in detail</p>
        </button>

        <button
          @click="handleStartChat('Search my knowledge base')"
          class="bg-gradient-to-br from-green-500 to-green-600 rounded-2xl p-6 text-white hover:shadow-xl transition-all group"
        >
          <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mb-4">
            <Globe class="w-6 h-6" />
          </div>
          <h3 class="font-bold ins text-lg mb-2">Knowledge Search</h3>
          <p class="text-sm text-green-100">Find specific information</p>
        </button>
      </div>

      <!-- Recent Topics -->
      <div v-if="recentTopics.length > 0" class="bg-white rounded-2xl border border-gray-200 p-6">
        <h2 class="text-xl font-bold text-gray-900 ins mb-4">Continue Recent Conversations</h2>
        <div class="space-y-3">
          <button
            v-for="(topic, idx) in recentTopics"
            :key="idx"
            @click="handleStartChat(topic.title)"
            class="w-full flex items-center justify-between p-4 bg-gray-50 hover:bg-gray-100 rounded-xl transition-all group"
          >
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 bg-gradient-to-br from-gray-200 to-gray-300 rounded-lg flex items-center justify-center">
                <MessageSquare class="w-5 h-5 text-gray-600" />
              </div>
              <div class="text-left">
                <h3 class="font-semibold text-gray-900 ins">{{ topic.title }}</h3>
                <p class="text-sm text-gray-500">{{ topic.time }}</p>
              </div>
            </div>
            <svg class="w-5 h-5 text-gray-400 group-hover:text-gray-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Features Info -->
      <div class="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="text-center p-6">
          <div class="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 class="font-bold text-gray-900 ins mb-1">Fast Responses</h3>
          <p class="text-sm text-gray-500">Powered by Gemini AI</p>
        </div>

        <div class="text-center p-6">
          <div class="w-12 h-12 bg-purple-50 rounded-xl flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
          <h3 class="font-bold text-gray-900 ins mb-1">Contextual</h3>
          <p class="text-sm text-gray-500">Based on your documents</p>
        </div>

        <div class="text-center p-6">
          <div class="w-12 h-12 bg-green-50 rounded-xl flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="font-bold text-gray-900 ins mb-1">Source Citations</h3>
          <p class="text-sm text-gray-500">Transparent & traceable</p>
        </div>
      </div>
    </div>
  </div>
</template>
