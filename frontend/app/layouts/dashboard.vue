<script setup lang="ts">
import { ref } from 'vue'
import { Home, MessageSquare, Database, User, Plus, Menu, X } from 'lucide-vue-next'

const isSidebarOpen = ref(true)

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: Home },
  { name: 'New Chat', href: '/dashboard/chat/new', icon: Plus },
  { name: 'Chats', href: '/dashboard/chat', icon: MessageSquare },
  { name: 'RAG Management', href: '/dashboard/rag', icon: Database },
  { name: 'Profile', href: '/dashboard/profile', icon: User },
]

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}
</script>

<template>
  <div class="flex h-screen overflow-hidden bg-gray-50">
    <!-- Sidebar -->
    <aside
      :class="[
        'fixed inset-y-0 left-0 z-40 w-64 bg-white border-r border-gray-200 transition-transform duration-300 ease-in-out lg:translate-x-0',
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
    >
      <div class="h-full flex flex-col">
        <!-- Logo -->
        <div class="h-16 flex items-center px-6 border-b border-gray-200 flex-shrink-0">
          <h1 class="font-['Questrial'] text-xl font-bold tracking-wider text-gray-900">Nerdie</h1>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          <NuxtLink
            v-for="item in navigation"
            :key="item.name"
            :to="item.href"
            class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-gray-700 hover:bg-gray-100 transition-all group text-sm"
            active-class="bg-black text-white hover:bg-black/90"
          >
            <component :is="item.icon" class="w-5 h-5" />
            <span class="ins font-medium">{{ item.name }}</span>
          </NuxtLink>
        </nav>

        <!-- User section -->
        <div class="p-3 border-t border-gray-200 flex-shrink-0">
          <NuxtLink
            to="/dashboard/profile"
            class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-gray-100 transition-all"
          >
            <div class="w-8 h-8 rounded-full bg-gradient-to-br from-orange-400 to-pink-500 flex items-center justify-center flex-shrink-0">
              <span class="text-white font-bold text-xs ins">U</span>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate ins">User</p>
              <p class="text-xs text-gray-500 truncate">user@email.com</p>
            </div>
          </NuxtLink>
        </div>
      </div>
    </aside>

    <!-- Overlay for mobile -->
    <div
      v-if="isSidebarOpen"
      class="fixed inset-0 bg-black/50 z-30 lg:hidden"
      @click="toggleSidebar"
    />

    <!-- Main content -->
    <div class="flex-1 flex flex-col overflow-hidden lg:ml-64">
      <!-- Header -->
      <header class="h-16 bg-white border-b border-gray-200 flex items-center px-4 lg:px-6 flex-shrink-0">
        <button
          @click="toggleSidebar"
          class="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors mr-3"
        >
          <Menu class="w-5 h-5 text-gray-700" />
        </button>

        <div class="flex-1 flex items-center justify-between gap-4">
          <div class="flex-1 max-w-xl">
            <div class="relative">
              <svg class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                placeholder="Search..."
                class="w-full pl-10 pr-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
              />
            </div>
          </div>

          <button class="p-2 rounded-lg hover:bg-gray-100 transition-colors relative flex-shrink-0">
            <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            <span class="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 overflow-y-auto bg-gray-50">
        <slot />
      </main>
    </div>
  </div>
</template>
