<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Icon } from '@iconify/vue'

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
        <Icon icon="hugeicons:plus-sign" class="w-5 h-5" />
        New Chat
      </button>
    </div>

    <!-- Search and Filters -->
    <div class="bg-white rounded-2xl border border-gray-200 p-6 mb-6">
      <div class="flex flex-col md:flex-row gap-4">
        <h1 class="text-4xl font-['Questrial'] font-light tracking-tight text-zinc-900 mb-2">Conversations.</h1>
        <p class="text-zinc-500 font-light">History of your dialogues with the AI.</p>
      </div>

      <div class="flex items-center gap-4 w-full md:w-auto">
        <div class="relative flex-1 md:w-80 group">
          <Icon icon="hugeicons:search-01" class="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-zinc-400 group-hover:text-zinc-600 transition-colors" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search conversations..."
            class="w-full pl-12 pr-4 py-3 bg-white border border-zinc-200 rounded-full text-zinc-900 placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-zinc-900/5 focus:border-zinc-900 transition-all shadow-sm group-hover:shadow-md"
          />
        </div>
        
        <NuxtLink
          to="/dashboard/chat/new"
          class="flex-shrink-0 w-12 h-12 bg-black text-white rounded-full flex items-center justify-center hover:scale-105 hover:shadow-lg transition-all duration-300"
        >
          <Icon icon="hugeicons:plus-sign" class="w-6 h-6" />
        </NuxtLink>
      </div>
    </div>

    <!-- Active/Recent Chats -->
    <div v-if="filteredChats.length > 0" class="grid grid-cols-1 gap-4">
      <TransitionGroup name="list" appear>
        <NuxtLink
          v-for="chat in filteredChats"
          :key="chat.id"
          :to="`/dashboard/chat/${chat.id}`"
          class="group glass-panel rounded-3xl p-6 hover:border-zinc-300 transition-all duration-300 flex items-start gap-6 relative overflow-hidden"
        >
          <!-- Hover effect background -->
          <div class="absolute inset-0 bg-zinc-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-10"></div>

          <div class="w-14 h-14 rounded-full bg-zinc-100 flex items-center justify-center flex-shrink-0 group-hover:bg-black transition-colors duration-500">
            <Icon icon="hugeicons:bubble-chat" class="w-6 h-6 text-zinc-500 group-hover:text-white transition-colors duration-500" />
          </div>
          
          <div class="flex-1 min-w-0 pt-1">
            <div class="flex items-center justify-between mb-2">
              <h3 class="text-lg font-medium text-zinc-900 truncate pr-4 group-hover:text-black transition-colors">{{ chat.title }}</h3>
              <span class="text-sm text-zinc-400 font-light">{{ formatDate(chat.updatedAt) }}</span>
            </div>
            
            <p class="text-zinc-500 line-clamp-2 font-light group-hover:text-zinc-600 transition-colors pr-12">{{ chat.preview }}</p>
            
            <div class="flex items-center gap-4 mt-4 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-y-2 group-hover:translate-y-0">
              <span class="text-xs font-medium px-2.5 py-1 rounded-full bg-zinc-200 text-zinc-600">
                {{ chat.messagesCount }} messages
              </span>
              <span class="text-xs font-medium px-2.5 py-1 rounded-full bg-zinc-200 text-zinc-600 capitalize">
                {{ chat.model }}
              </span>
            </div>
          </div>

          <div class="absolute right-6 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-all duration-500 transform translate-x-4 group-hover:translate-x-0">
            <Icon icon="hugeicons:arrow-right-01" class="w-6 h-6 text-zinc-400 group-hover:text-black" />
          </div>

          <button
            @click.prevent="deleteChat(chat.id)"
            class="absolute top-6 right-6 p-2 rounded-full hover:bg-zinc-200 text-zinc-300 hover:text-red-500 transition-colors opacity-0 group-hover:opacity-100 z-10"
            title="Delete conversation"
          >
            <Icon icon="hugeicons:delete-02" class="w-4 h-4" />
          </button>
        </NuxtLink>
      </TransitionGroup>
    </div>

    <div v-else class="text-center py-24">
      <div class="w-24 h-24 bg-zinc-50 rounded-full flex items-center justify-center mx-auto mb-6">
        <Icon icon="hugeicons:bubble-chat" class="w-10 h-10 text-zinc-300" />
      </div>
      <h3 class="text-xl font-medium text-zinc-900 mb-2">No conversations found</h3>
      <p class="text-zinc-500 font-light mb-8 max-w-sm mx-auto">Start a new chat to begin interacting with the AI assistant.</p>
      <NuxtLink
        to="/dashboard/chat/new"
        class="inline-flex items-center gap-2 px-8 py-3 bg-black text-white rounded-full hover:bg-zinc-800 transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5"
      >
        <Icon icon="hugeicons:plus-sign" class="w-5 h-5" />
        <span class="font-medium">Start New Chat</span>
      </NuxtLink>
    </div>
  </div>
</template>
