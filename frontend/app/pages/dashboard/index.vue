<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { Icon } from '@iconify/vue'
import { useChatStore } from '../../../stores/chat'
import { useIngestionApi } from '../../../composables/useIngestionApi'

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const { userData } = useAuth()
const chatStore = useChatStore()
const { fetchDocuments } = useIngestionApi()

// Local state for documents
const recentDocuments = ref<any[]>([])
const isLoadingDocs = ref(true)

// Fetch data on mount
onMounted(async () => {
    isLoadingDocs.value = true
    try {
        const docs = await fetchDocuments()
        // Assuming docs is an array, we might need to map it if structure differs
        // The ingestion list doc endpoint returns list of objects.
        // We'll map them to match UI needs or use as is.
        recentDocuments.value = docs || []
    } catch (e) {
        console.error("Failed to fetch docs", e)
    } finally {
        isLoadingDocs.value = false
    }
})

// Get time-based greeting
const greeting = computed(() => {
  const hour = new Date().getHours()

  if (hour >= 5 && hour < 12) {
    return 'Good morning'
  } else if (hour >= 12 && hour < 17) {
    return 'Good afternoon'
  } else if (hour >= 17 && hour < 22) {
    return 'Good evening'
  } else {
    return 'Good night'
  }
})

// Get user's first name
const firstName = computed(() => {
  if (userData.value?.displayName) {
    return userData.value.displayName.split(' ')[0]
  }
  return 'User'
})

// Computed Stats
const stats = computed(() => [
  { name: 'Total Chats', value: chatStore.sessions.length.toString(), icon: 'hugeicons:bubble-chat', change: '+0%', changeType: 'neutral' }, // Change % would need real historical data
  { name: 'Documents in RAG', value: recentDocuments.value.length.toString(), icon: 'hugeicons:database-01', change: '+0%', changeType: 'neutral' },
  { name: 'Queries Today', value: '0', icon: 'hugeicons:analytics-up', change: '0%', changeType: 'neutral' }, // Need query tracking in store to show real data
  { name: 'Avg Response Time', value: '1.2s', icon: 'hugeicons:clock-01', change: '-5%', changeType: 'positive' }, // Mock for now
])

const recentChats = computed(() => chatStore.recentChats.map((c: any) => ({
    id: c.id,
    title: c.title,
    preview: c.messages[c.messages.length - 1]?.content.slice(0, 50) + '...' || 'No messages',
    time: new Date(c.updatedAt).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}),
    unread: false
})))


const quickActions = [
  { name: 'New Chat', description: 'Start a conversation', icon: 'hugeicons:bubble-chat', href: '/dashboard/chat/new', color: 'bg-blue-500' },
  { name: 'Upload Document', description: 'Add to knowledge base', icon: 'hugeicons:plus-sign-circle', href: '/dashboard/rag', color: 'bg-green-500' },
  { name: 'View Analytics', description: 'Check performance', icon: 'hugeicons:analytics-up', href: '/dashboard/analytics', color: 'bg-purple-500' },
  { name: 'Quick Query', description: 'Fast AI response', icon: 'hugeicons:flash', href: '/dashboard/chat/new', color: 'bg-orange-500' },
]

// Helper to format file size if needed
const formatSize = (size: number) => {
    if (!size) return 'Unknown'
    const i = Math.floor(Math.log(size) / Math.log(1024));
    return (size / Math.pow(1024, i)).toFixed(1) + ' ' + ['B', 'KB', 'MB', 'GB', 'TB'][i];
};
</script>

<template>
  <div>
    <!-- Page Header -->
    <div class="mb-12">
      <h1 class="text-4xl font-['Questrial'] font-light tracking-tight text-zinc-900 mb-3">{{ greeting }}, {{ firstName }}.</h1>
      <p class="text-zinc-500 font-light text-base">Here's your daily intelligence briefing</p>
    </div>

    <!-- Stats Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
      <div
        v-for="stat in stats"
        :key="stat.name"
        class="group glass-panel rounded-3xl p-6 transition-all duration-500 hover:shadow-[0_20px_40px_-15px_rgba(0,0,0,0.1)]"
      >
        <div class="flex items-start justify-between mb-8">
          <div class="p-3 bg-zinc-50 rounded-2xl transition-colors duration-500">
            <Icon :icon="stat.icon" class="w-5 h-5 text-zinc-900 transition-colors duration-500" />
          </div>
          <span
            class="text-xs font-medium px-2.5 py-1 rounded-full bg-zinc-100 text-zinc-600 transition-colors duration-500"
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
      <h2 class="text-lg font-['Questrial'] text-zinc-900 mb-6 flex items-center gap-2">
        Quick Actions
      </h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <NuxtLink
          v-for="action in quickActions"
          :key="action.name"
          :to="action.href"
          class="group bg-white border border-zinc-100 p-6 rounded-3xl hover:border-zinc-300 transition-all duration-300 flex flex-col items-center text-center justify-center gap-4 aspect-[4/3]"
        >
          <div class="w-14 h-14 rounded-full bg-zinc-50 flex items-center justify-center transition">
            <Icon :icon="action.icon" class="w-6 h-6 text-zinc-900 transition-colors duration-300" />
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
            <h2 class="text-lg font-['Questrial'] text-zinc-900">Recent Conversations</h2>
            <NuxtLink to="/dashboard/chat" class="text-sm font-medium text-zinc-500 hover:text-zinc-900 transition-colors">
              View all
            </NuxtLink>
          </div>

          <div v-if="recentChats.length === 0" class="text-center py-12 text-zinc-400">
             <Icon icon="hugeicons:bubble-chat" class="w-10 h-10 mx-auto mb-3 opacity-50" />
             <p>No recent conversations</p>
          </div>

          <div class="space-y-4" v-else>
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
            <h2 class="text-lg font-['Questrial'] text-zinc-900">Knowledge Base</h2>
            <NuxtLink to="/dashboard/rag" class="p-2 rounded-full hover:bg-zinc-100 transition-colors">
              <Icon icon="hugeicons:plus-sign" class="w-4 h-4 text-zinc-900" />
            </NuxtLink>
          </div>

           <div v-if="isLoadingDocs" class="flex justify-center py-8">
              <Icon icon="svg-spinners:ring-resize" class="w-6 h-6 text-zinc-400" />
           </div>
           
           <div v-else-if="recentDocuments.length === 0" class="text-center py-8 text-zinc-400 text-sm">
                No documents uploaded yet
           </div>

          <div class="space-y-3" v-else>
            <div
              v-for="doc in recentDocuments.slice(0, 5)"
              :key="doc.name || doc.id"
              class="flex items-center gap-3 p-3 rounded-xl hover:bg-zinc-50 transition-colors cursor-pointer group"
            >
              <div class="p-2 bg-zinc-50 rounded-lg group-hover:bg-white group-hover:shadow-sm transition-all">
                <Icon icon="hugeicons:file-text" class="w-4 h-4 text-zinc-500 group-hover:text-zinc-900" />
              </div>
              <div class="flex-1 min-w-0">
                <h3 class="text-sm font-medium text-zinc-700 truncate group-hover:text-zinc-900">{{ doc.metadata?.source || doc.filename || doc.id }}</h3>
                <!-- Assuming doc might have metadata with source, or fallback to id -->
                <!-- API response structure isn't 100% clear on 'name', assuming metadata.source or filename -->
                <p class="text-xs text-zinc-400">{{ formatSize(doc.metadata?.size || 0) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
