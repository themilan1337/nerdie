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
  { name: 'Upload Document', description: 'Add to knowledge base', icon: 'hugeicons:plus-sign-circle', href: '/dashboard/rag', color: 'bg-green-500' },
  { name: 'View Analytics', description: 'Check performance', icon: 'hugeicons:analytics-up', href: '/dashboard/analytics', color: 'bg-purple-500' },
  { name: 'Quick Query', description: 'Fast AI response', icon: 'hugeicons:flash', href: '/dashboard/chat/new', color: 'bg-orange-500' },
]
</script>

<template>
  <div>
    <!-- Page Header -->
    <div class="mb-12">
      <h1 class="text-4xl font-['Questrial'] font-light tracking-tight text-zinc-900 mb-3">Overview</h1>
      <p class="text-zinc-500 font-light text-base">Here's your daily intelligence briefing.</p>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
      <div
        v-for="stat in stats"
        :key="stat.name"
        class="group glass-panel rounded-3xl p-6 transition-all duration-500 hover:shadow-[0_20px_40px_-15px_rgba(0,0,0,0.1)] hover:-translate-y-1"
      >
        <div class="flex items-start justify-between mb-8">
          <div class="p-3 bg-zinc-50 rounded-2xl group-hover:bg-zinc-900 transition-colors duration-500">
            <Icon :icon="stat.icon" class="w-5 h-5 text-zinc-900 group-hover:text-white transition-colors duration-500" />
          </div>
          <span
            class="text-xs font-medium px-2.5 py-1 rounded-full bg-zinc-100 text-zinc-600 group-hover:bg-zinc-900 group-hover:text-white transition-colors duration-500"
          >
            {{ stat.change }}
          </span>
        </div>
        <div>
          <p class="text-3xl font-light text-zinc-900 tracking-tight mb-1">{{ stat.value }}</p>
          <p class="text-sm text-zinc-500 font-medium tracking-wide">{{ stat.name }}</p>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="mb-12">
      <h2 class="text-lg font-medium text-zinc-900 mb-6 flex items-center gap-2">
        <span class="w-1.5 h-1.5 bg-zinc-900 rounded-full"></span>
        Quick Actions
      </h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <NuxtLink
          v-for="action in quickActions"
          :key="action.name"
          :to="action.href"
          class="group bg-white border border-zinc-100 p-6 rounded-3xl hover:border-zinc-300 transition-all duration-300 flex flex-col items-center text-center justify-center gap-4 aspect-[4/3]"
        >
          <div class="w-14 h-14 rounded-full bg-zinc-50 flex items-center justify-center group-hover:bg-zinc-900 transition">
            <Icon :icon="action.icon" class="w-6 h-6 text-zinc-900 group-hover:text-white transition-colors duration-300" />
          </div>
          <div>
            <h3 class="font-medium text-zinc-900 mb-1 group-hover:text-black">{{ action.name }}</h3>
            <p class="text-xs text-zinc-500 group-hover:text-zinc-600">{{ action.description }}</p>
          </div>
        </NuxtLink>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Recent Chats -->
      <div class="lg:col-span-2">
        <div class="glass-panel rounded-3xl p-8 h-full">
          <div class="flex items-center justify-between mb-8">
            <h2 class="text-lg font-medium text-zinc-900">Recent Conversations</h2>
            <NuxtLink to="/dashboard/chat" class="text-sm font-medium text-zinc-500 hover:text-zinc-900 transition-colors">
              View all
            </NuxtLink>
          </div>

          <div class="space-y-4">
            <NuxtLink
              v-for="chat in recentChats"
              :key="chat.id"
              :to="`/dashboard/chat/${chat.id}`"
              class="flex items-start gap-4 p-4 rounded-2xl hover:bg-zinc-50 transition-all group border border-transparent hover:border-zinc-100"
            >
              <div class="w-10 h-10 rounded-full bg-zinc-100 flex items-center justify-center flex-shrink-0 group-hover:bg-zinc-900 transition-colors duration-300">
                <Icon icon="hugeicons:bubble-chat" class="w-5 h-5 text-zinc-500 group-hover:text-white" />
              </div>
              <div class="flex-1 min-w-0 pt-0.5">
                <div class="flex items-center justify-between mb-1">
                  <h3 class="font-medium text-zinc-900 truncate pr-4">{{ chat.title }}</h3>
                  <span class="text-xs text-zinc-400 whitespace-nowrap">{{ chat.time }}</span>
                </div>
                <p class="text-sm text-zinc-500 truncate group-hover:text-zinc-700">{{ chat.preview }}</p>
              </div>
              <div class="pt-2 opacity-0 group-hover:opacity-100 transition-opacity transform translate-x-2 group-hover:translate-x-0">
                <Icon icon="hugeicons:arrow-right-01" class="w-4 h-4 text-zinc-400" />
              </div>
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- System Status & Recent Docs -->
      <div class="space-y-8">
        <!-- Recent Docs -->
        <div class="glass-panel rounded-3xl p-8">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-medium text-zinc-900">Knowledge Base</h2>
            <NuxtLink to="/dashboard/rag" class="p-2 rounded-full hover:bg-zinc-100 transition-colors">
              <Icon icon="hugeicons:plus-sign" class="w-4 h-4 text-zinc-900" />
            </NuxtLink>
          </div>

          <div class="space-y-3">
            <div
              v-for="doc in recentDocuments"
              :key="doc.name"
              class="flex items-center gap-3 p-3 rounded-xl hover:bg-zinc-50 transition-colors cursor-pointer group"
            >
              <div class="p-2 bg-zinc-50 rounded-lg group-hover:bg-white group-hover:shadow-sm transition-all">
                <Icon icon="hugeicons:file-text" class="w-4 h-4 text-zinc-500 group-hover:text-zinc-900" />
              </div>
              <div class="flex-1 min-w-0">
                <h3 class="text-sm font-medium text-zinc-700 truncate group-hover:text-zinc-900">{{ doc.name }}</h3>
                <p class="text-xs text-zinc-400">{{ doc.size }} • {{ doc.uploadedAt }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Minimal System Status -->
        <div class="bg-zinc-900 rounded-3xl p-8 text-white relative overflow-hidden group">
          <div class="absolute top-0 right-0 w-32 h-32 bg-zinc-800 rounded-full blur-3xl -mr-16 -mt-16 opacity-50 group-hover:opacity-100 transition-opacity duration-700"></div>
          
          <div class="relative z-10">
            <div class="flex items-start justify-between mb-8">
              <div>
                <h3 class="text-lg font-medium mb-1">System Status</h3>
                <p class="text-zinc-400 text-sm">All systems operational</p>
              </div>
              <div class="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)] animate-pulse"></div>
            </div>

            <div class="space-y-4">
              <div class="flex items-center justify-between text-sm">
                <span class="text-zinc-400">RAG Engine</span>
                <span class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span>
                  Active
                </span>
              </div>
              <div class="flex items-center justify-between text-sm">
                <span class="text-zinc-400">Gemini Pro</span>
                <span class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span>
                  Connected
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
