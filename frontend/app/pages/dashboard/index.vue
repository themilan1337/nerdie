<script setup lang="ts">
import { Icon } from '@iconify/vue'

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const stats = [
  { name: 'Total Chats', value: '24', icon: 'hugeicons:bubble-chat', change: '+12%', changeType: 'positive' },
  { name: 'Documents in RAG', value: '156', icon: 'hugeicons:database-01', change: '+8%', changeType: 'positive' },
  { name: 'Queries Today', value: '89', icon: 'hugeicons:analytics-up', change: '+23%', changeType: 'positive' },
  { name: 'Avg Response Time', value: '1.2s', icon: 'hugeicons:clock-01', change: '-5%', changeType: 'positive' },
]

const recentChats = [
  { id: 1, title: 'Machine Learning Basics', preview: 'What are the fundamental concepts...', time: '2 min ago', unread: true },
  { id: 2, title: 'Python Data Analysis', preview: 'How to use pandas for data...', time: '1 hour ago', unread: false },
  { id: 3, title: 'Web Development Tips', preview: 'Best practices for building...', time: '3 hours ago', unread: false },
  { id: 4, title: 'AI Ethics Discussion', preview: 'What are the ethical considerations...', time: '1 day ago', unread: false },
]

const recentDocuments = [
  { name: 'research_paper_2024.pdf', size: '2.4 MB', uploadedAt: '2 hours ago', type: 'PDF' },
  { name: 'company_handbook.docx', size: '1.8 MB', uploadedAt: '1 day ago', type: 'DOCX' },
  { name: 'meeting_notes.txt', size: '45 KB', uploadedAt: '2 days ago', type: 'TXT' },
  { name: 'project_overview.pdf', size: '3.2 MB', uploadedAt: '3 days ago', type: 'PDF' },
]

const quickActions = [
  { name: 'New Chat', description: 'Start a conversation', icon: 'hugeicons:bubble-chat', href: '/dashboard/chat/new', color: 'bg-blue-500' },
  { name: 'Upload Document', description: 'Add to knowledge base', icon: 'hugeicons:file-text', href: '/dashboard/rag', color: 'bg-green-500' },
  { name: 'View Analytics', description: 'Check performance', icon: 'hugeicons:analytics-up', href: '/dashboard/analytics', color: 'bg-purple-500' },
  { name: 'Quick Query', description: 'Fast AI response', icon: 'hugeicons:flash', href: '/dashboard/chat/new', color: 'bg-orange-500' },
]
</script>

<template>
  <div class="p-6 max-w-[1600px] mx-auto">
    <!-- Page Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 ins mb-1">Dashboard</h1>
      <p class="text-sm text-gray-500">Welcome back! Here's what's happening with your AI assistant.</p>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <div
        v-for="stat in stats"
        :key="stat.name"
        class="bg-white rounded-xl border border-gray-200 p-5 hover:shadow-sm transition-all"
      >
        <div class="flex items-start justify-between mb-3">
          <div class="p-2 bg-gray-50 rounded-lg">
            <Icon :icon="stat.icon" class="w-5 h-5 text-gray-700" />
          </div>
          <span
            :class="[
              'text-xs font-semibold px-2 py-1 rounded-md',
              stat.changeType === 'positive' ? 'text-green-600 bg-green-50' : 'text-red-600 bg-red-50'
            ]"
          >
            {{ stat.change }}
          </span>
        </div>
        <p class="text-xs text-gray-600 mb-1">{{ stat.name }}</p>
        <p class="text-2xl font-bold text-gray-900 ins">{{ stat.value }}</p>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="mb-6">
      <h2 class="text-lg font-bold text-gray-900 ins mb-4">Quick Actions</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <NuxtLink
          v-for="action in quickActions"
          :key="action.name"
          :to="action.href"
          class="bg-white rounded-xl border border-gray-200 p-4 hover:shadow-sm transition-all group"
        >
          <div :class="[action.color, 'w-10 h-10 rounded-lg flex items-center justify-center mb-3 group-hover:scale-105 transition-transform']">
            <Icon :icon="action.icon" class="w-5 h-5 text-white" />
          </div>
          <h3 class="font-semibold text-gray-900 mb-1 ins text-sm">{{ action.name }}</h3>
          <p class="text-xs text-gray-500">{{ action.description }}</p>
        </NuxtLink>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Recent Chats -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-xl border border-gray-200 p-5">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-bold text-gray-900 ins">Recent Chats</h2>
            <NuxtLink to="/dashboard/chat" class="text-xs text-gray-600 hover:text-black transition-colors ins">
              View all &rarr;
            </NuxtLink>
          </div>

          <div class="space-y-2">
            <NuxtLink
              v-for="chat in recentChats"
              :key="chat.id"
              :to="`/dashboard/chat/${chat.id}`"
              class="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 transition-all group"
            >
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-1">
                  <h3 class="font-medium text-gray-900 truncate text-sm ins">{{ chat.title }}</h3>
                  <span v-if="chat.unread" class="w-1.5 h-1.5 bg-blue-500 rounded-full flex-shrink-0"></span>
                </div>
                <p class="text-xs text-gray-500 truncate mb-1.5">{{ chat.preview }}</p>
                <div class="flex items-center gap-1.5">
                  <Icon icon="hugeicons:clock-01" class="w-3 h-3 text-gray-400" />
                  <span class="text-xs text-gray-400">{{ chat.time }}</span>
                </div>
              </div>
              <button class="p-1.5 rounded-lg opacity-0 group-hover:opacity-100 hover:bg-gray-100 transition-all">
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </NuxtLink>
          </div>
        </div>
      </div>

      <div>
        <div class="bg-white rounded-xl border border-gray-200 p-5 mb-4">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-bold text-gray-900 ins">Recent Documents</h2>
            <NuxtLink to="/dashboard/rag" class="text-xs text-gray-600 hover:text-black transition-colors ins">
              View all &rarr;
            </NuxtLink>
          </div>

          <div class="space-y-2">
            <div
              v-for="doc in recentDocuments"
              :key="doc.name"
              class="flex items-start gap-2.5 p-2.5 rounded-lg hover:bg-gray-50 transition-all group cursor-pointer"
            >
              <div class="p-1.5 bg-gray-100 rounded-md">
                <Icon icon="hugeicons:file-text" class="w-3.5 h-3.5 text-gray-600" />
              </div>
              <div class="flex-1 min-w-0">
                <h3 class="font-medium text-gray-900 truncate text-xs">{{ doc.name }}</h3>
                <div class="flex items-center gap-1.5 mt-0.5">
                  <span class="text-xs text-gray-400">{{ doc.size }}</span>
                  <span class="text-xs text-gray-300">•</span>
                  <span class="text-xs text-gray-400">{{ doc.uploadedAt }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-gradient-to-br from-black to-gray-800 rounded-xl p-5 text-white">
          <h3 class="text-base font-bold mb-1 ins">System Status</h3>
          <p class="text-xs text-gray-300 mb-4">All systems operational</p>
          <div class="space-y-2.5">
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-300">RAG System</span>
              <span class="text-xs bg-green-500 text-white px-2 py-0.5 rounded-full font-medium">Active</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-300">Embeddings</span>
              <span class="text-xs bg-green-500 text-white px-2 py-0.5 rounded-full font-medium">Ready</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-300">Gemini API</span>
              <span class="text-xs bg-green-500 text-white px-2 py-0.5 rounded-full font-medium">Connected</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
