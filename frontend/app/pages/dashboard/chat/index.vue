<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { MessageSquare, Plus, Clock, Trash2, Search, Filter } from 'lucide-vue-next'

definePageMeta({
  layout: 'dashboard'
})

const router = useRouter()
const searchQuery = ref('')
const selectedFilter = ref('all')

const filterOptions = [
  { value: 'all', label: 'All Chats' },
  { value: 'today', label: 'Today' },
  { value: 'week', label: 'This Week' },
  { value: 'month', label: 'This Month' },
]

interface Chat {
  id: string
  title: string
  lastMessage: string
  timestamp: string
  messageCount: number
}

const chats = ref<Chat[]>([
  {
    id: '1',
    title: 'Machine Learning Discussion',
    lastMessage: 'Can you explain how neural networks work?',
    timestamp: '2 hours ago',
    messageCount: 15
  },
  {
    id: '2',
    title: 'Python Programming Help',
    lastMessage: 'How do I optimize this code?',
    timestamp: '5 hours ago',
    messageCount: 8
  },
  {
    id: '3',
    title: 'Database Design Questions',
    lastMessage: 'What is the best approach for indexing?',
    timestamp: 'Yesterday',
    messageCount: 23
  },
])

const filteredChats = computed(() => {
  let filtered = chats.value

  if (searchQuery.value) {
    filtered = filtered.filter(chat =>
      chat.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      chat.lastMessage.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  return filtered
})

const createNewChat = () => {
  router.push('/dashboard/chat/new')
}

const openChat = (chatId: string) => {
  router.push(`/dashboard/chat/${chatId}`)
}

const deleteChat = (chatId: string, event: Event) => {
  event.stopPropagation()
  if (confirm('Are you sure you want to delete this chat?')) {
    chats.value = chats.value.filter(chat => chat.id !== chatId)
  }
}
</script>

<template>
  <div class="p-6 lg:p-8">
    <!-- Page Header -->
    <div class="mb-8 flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 ins">Chat History</h1>
        <p class="text-gray-500 mt-1">View and manage your conversations</p>
      </div>
      <button
        @click="createNewChat"
        class="px-6 py-3 bg-black text-white rounded-full font-medium ins hover:bg-gray-800 transition-colors inline-flex items-center gap-2"
      >
        <Plus class="w-5 h-5" />
        New Chat
      </button>
    </div>

    <!-- Search and Filters -->
    <div class="bg-white rounded-2xl border border-gray-200 p-6 mb-6">
      <div class="flex flex-col md:flex-row gap-4">
        <!-- Search -->
        <div class="flex-1 relative">
          <Search class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search chats..."
            class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
          />
        </div>

        <!-- Filter Dropdown -->
        <div class="relative">
          <Filter class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <select
            v-model="selectedFilter"
            class="pl-10 pr-8 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all appearance-none cursor-pointer min-w-[200px]"
          >
            <option v-for="option in filterOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Chat List -->
    <div v-if="filteredChats.length > 0" class="space-y-4">
      <div
        v-for="chat in filteredChats"
        :key="chat.id"
        @click="openChat(chat.id)"
        class="bg-white rounded-2xl border border-gray-200 p-6 hover:border-gray-300 hover:shadow-md transition-all cursor-pointer group"
      >
        <div class="flex items-start justify-between">
          <div class="flex items-start gap-4 flex-1">
            <div class="w-12 h-12 bg-gradient-to-br from-blue-400 to-purple-500 rounded-xl flex items-center justify-center flex-shrink-0">
              <MessageSquare class="w-6 h-6 text-white" />
            </div>
            <div class="flex-1 min-w-0">
              <h3 class="text-lg font-bold text-gray-900 ins mb-1 group-hover:text-black">
                {{ chat.title }}
              </h3>
              <p class="text-gray-600 text-sm mb-2 truncate">
                {{ chat.lastMessage }}
              </p>
              <div class="flex items-center gap-4 text-xs text-gray-500">
                <span class="flex items-center gap-1">
                  <Clock class="w-3 h-3" />
                  {{ chat.timestamp }}
                </span>
                <span>{{ chat.messageCount }} messages</span>
              </div>
            </div>
          </div>
          <button
            @click="deleteChat(chat.id, $event)"
            class="p-2 rounded-lg hover:bg-red-50 transition-colors opacity-0 group-hover:opacity-100"
            title="Delete chat"
          >
            <Trash2 class="w-5 h-5 text-red-600" />
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="bg-white rounded-2xl border border-gray-200 p-12 text-center">
      <div class="w-20 h-20 bg-gray-100 rounded-2xl mx-auto mb-6 flex items-center justify-center">
        <MessageSquare class="w-10 h-10 text-gray-400" />
      </div>
      <h3 class="text-xl font-bold text-gray-900 ins mb-2">
        {{ chats.length === 0 ? 'No chats yet' : 'No chats found' }}
      </h3>
      <p class="text-gray-500 mb-6">
        {{ chats.length === 0
          ? 'Start a new conversation to get started'
          : 'Try adjusting your search or filters'
        }}
      </p>
      <button
        v-if="chats.length === 0"
        @click="createNewChat"
        class="px-6 py-3 bg-black text-white rounded-full font-medium ins hover:bg-gray-800 transition-colors inline-flex items-center gap-2"
      >
        <Plus class="w-5 h-5" />
        Start Your First Chat
      </button>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
      <div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white">
        <p class="text-sm text-blue-100 mb-1">Total Chats</p>
        <p class="text-3xl font-bold ins">{{ chats.length }}</p>
      </div>
      <div class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl p-6 text-white">
        <p class="text-sm text-purple-100 mb-1">Total Messages</p>
        <p class="text-3xl font-bold ins">{{ chats.reduce((sum, c) => sum + c.messageCount, 0) }}</p>
      </div>
      <div class="bg-gradient-to-br from-pink-500 to-pink-600 rounded-2xl p-6 text-white">
        <p class="text-sm text-pink-100 mb-1">Active Conversations</p>
        <p class="text-3xl font-bold ins">{{ chats.length }}</p>
      </div>
    </div>
  </div>
</template>
