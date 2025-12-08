<script setup lang="ts">
import { ref, computed } from 'vue'
import { Icon } from '@iconify/vue'
import { useChatStore } from '../../../../stores/chat'

definePageMeta({
  layout: 'dashboard',
  middleware: 'auth'
})

const chatStore = useChatStore()
const searchQuery = ref('')

const conversations = computed(() => {
    // Access detailed sessions from store
    let chats = [...chatStore.sessions].sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime())
    
    if (searchQuery.value) {
        const q = searchQuery.value.toLowerCase()
        chats = chats.filter(c => c.title.toLowerCase().includes(q))
    }
    
    return chats.map(c => ({
        id: c.id,
        title: c.title,
        message: c.messages[c.messages.length - 1]?.content || 'New conversation',
        time: new Date(c.updatedAt).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}),
    }))
})
</script>

<template>
  <div class="h-full flex flex-col">
    <!-- Header -->
    <div class="mb-8 flex-shrink-0">
      <h1 class="text-4xl font-['Questrial'] font-light tracking-tight text-zinc-900 mb-3">Messages</h1>
      <p class="text-zinc-500 font-light text-base">Your conversation history with Nerdie AI</p>
    </div>

    <!-- Controls -->
    <div class="mb-6 flex gap-4 flex-shrink-0">
      <div class="relative flex-1 group">
        <Icon icon="hugeicons:search-01" class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400 group-hover:text-zinc-600 transition-colors" />
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search conversations..."
          class="w-full pl-10 pr-4 py-3 bg-white border border-zinc-200 rounded-2xl text-zinc-900 placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-black/5 focus:border-zinc-300 transition-all shadow-sm"
        />
      </div>
      <NuxtLink
        to="/dashboard/chat/new"
        class="flex items-center gap-2 px-6 py-3 bg-zinc-900 text-white rounded-2xl font-medium hover:bg-black transition-all shadow-sm hover:shadow-lg hover:-translate-y-0.5"
      >
        <Icon icon="hugeicons:plus-sign" class="w-5 h-5" />
        <span>New Chat</span>
      </NuxtLink>
    </div>

    <div class="flex-1 min-h-0 bg-white border border-zinc-100 rounded-3xl overflow-hidden flex flex-col">
      <div v-if="conversations.length === 0" class="flex-1 flex my-16 flex-col items-center justify-center text-zinc-400">
          <Icon icon="hugeicons:bubble-chat" class="w-12 h-12 mb-3 opacity-50" />
          <p class="font-['Questrial']">No conversations found</p>
      </div>
      <div v-else class="overflow-y-auto flex-1 p-2 space-y-2">
        <NuxtLink
          v-for="chat in conversations"
          :key="chat.id"
          :to="`/dashboard/chat/${chat.id}`"
          class="flex items-center gap-4 p-4 rounded-2xl hover:bg-zinc-50 transition-all group border border-transparent hover:border-zinc-100"
        >
          <div class="w-12 h-12 rounded-full bg-zinc-100 flex items-center justify-center flex-shrink-0 group-hover:bg-zinc-900 transition-colors duration-300">
            <Icon icon="hugeicons:bubble-chat" class="w-6 h-6 text-zinc-500 group-hover:text-white" />
          </div>
          
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between mb-1">
              <h3 class="font-medium text-zinc-900 truncate pr-4">{{ chat.title }}</h3>
              <span class="text-xs text-zinc-400 whitespace-nowrap">{{ chat.time }}</span>
            </div>
            <p class="text-sm text-zinc-500 truncate group-hover:text-zinc-700 pr-8">
              {{ chat.message }}
            </p>
          </div>
          
          <div class="opacity-0 group-hover:opacity-100 transition-opacity">
            <Icon icon="hugeicons:arrow-right-01" class="w-5 h-5 text-zinc-400" />
          </div>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
