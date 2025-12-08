<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { Icon } from '@iconify/vue'

const isSidebarOpen = ref(true)
const showLogoutDropdown = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)

const { userData, signOut, initAuthListener } = useAuth()

// Initialize auth listener
onMounted(() => {
  initAuthListener()
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Handle click outside dropdown
const handleClickOutside = (event: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    showLogoutDropdown.value = false
  }
}

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: 'hugeicons:home-01' },
  { name: 'New Chat', href: '/dashboard/chat/new', icon: 'hugeicons:plus-sign' },
  { name: 'Chats', href: '/dashboard/chat', icon: 'hugeicons:bubble-chat' },
  { name: 'RAG Management', href: '/dashboard/rag', icon: 'hugeicons:database-01' },
  { name: 'Profile', href: '/dashboard/profile', icon: 'hugeicons:user' },
]

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

const handleLogout = async () => {
  await signOut()
}

// Get user initials
const userInitials = computed(() => {
  if (userData.value?.displayName) {
    return userData.value.displayName
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .substring(0, 2)
  }
  return 'U'
})

// Get display name or email
const displayName = computed(() => {
  return userData.value?.displayName || 'User'
})

const userEmail = computed(() => {
  return userData.value?.email || 'user@email.com'
})
</script>

<template>
  <div class="flex h-screen overflow-hidden bg-zinc-50 selection:bg-black selection:text-white">
    <!-- Sidebar -->
    <aside
      :class="[
        'fixed inset-y-0 left-0 z-40 w-72 bg-zinc-50 border-r border-zinc-200/50 transition-transform duration-500 cubic-bezier(0.32, 0.72, 0, 1) lg:translate-x-0',
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
    >
      <div class="h-full flex flex-col p-6">
        <!-- Logo -->
        <div class="h-12 flex items-center px-2 mb-8">
          <h1 class="font-['Questrial'] text-2xl font-bold tracking-tight text-zinc-900">nerdie.</h1>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 space-y-1">
          <NuxtLink
            v-for="item in navigation"
            :key="item.name"
            :to="item.href"
            class="flex items-center gap-3 px-4 py-3 rounded-2xl text-zinc-500 hover:text-zinc-900 hover:bg-zinc-100 transition-all duration-300 group relative overflow-hidden"
            active-class="!bg-black !text-white shadow-lg shadow-black/5"
          >
            <Icon :icon="item.icon" class="w-5 h-5 transition-transform duration-300 group-hover:scale-110" />
            <span class="font-medium text-sm tracking-wide">{{ item.name }}</span>
          </NuxtLink>
        </nav>

        <!-- User section -->
        <div class="mt-auto pt-6 border-t border-zinc-200/50">
          <div class="relative" ref="dropdownRef">
            <button
              @click="showLogoutDropdown = !showLogoutDropdown"
              class="flex items-center gap-3 p-2 rounded-2xl hover:bg-zinc-100 transition-all duration-300 w-full group"
            >
              <div class="relative">
                <img
                  v-if="userData?.photoUrl"
                  :src="userData.photoUrl"
                  :alt="displayName"
                  class="w-10 h-10 rounded-full object-cover ring-2 ring-white shadow-sm"
                />
                <div
                  v-else
                  class="w-10 h-10 rounded-full bg-zinc-900 text-white flex items-center justify-center ring-2 ring-white shadow-sm"
                >
                  <span class="font-medium text-xs">{{ userInitials }}</span>
                </div>
                <div class="absolute bottom-0 right-0 w-2.5 h-2.5 bg-green-500 border-2 border-white rounded-full"></div>
              </div>
              
              <div class="flex-1 min-w-0 text-left">
                <p class="text-sm font-semibold text-zinc-900 truncate group-hover:text-black transition-colors">{{ displayName }}</p>
                <p class="text-xs text-zinc-500 truncate">Free Plan</p>
              </div>
              
              <Icon icon="hugeicons:more-horizontal" class="w-5 h-5 text-zinc-400 group-hover:text-zinc-600" />
            </button>

            <!-- Logout dropdown -->
            <Transition
              enter-active-class="transition ease-out duration-200"
              enter-from-class="opacity-0 translate-y-2 scale-95"
              enter-to-class="opacity-100 translate-y-0 scale-100"
              leave-active-class="transition ease-in duration-150"
              leave-from-class="opacity-100 translate-y-0 scale-100"
              leave-to-class="opacity-0 translate-y-2 scale-95"
            >
              <div
                v-if="showLogoutDropdown"
                class="absolute bottom-full left-0 right-0 mb-3 bg-white/80 backdrop-blur-xl border border-white/20 shadow-[0_8px_30px_rgb(0,0,0,0.12)] rounded-2xl overflow-hidden p-1.5"
              >
                <NuxtLink
                  to="/dashboard/profile"
                  class="flex items-center gap-2 px-3 py-2.5 rounded-xl hover:bg-zinc-50 transition-colors text-sm text-zinc-700"
                  @click="showLogoutDropdown = false"
                >
                  <Icon icon="hugeicons:user" class="w-4 h-4" />
                  <span>Profile</span>
                </NuxtLink>
                <button
                  @click="handleLogout"
                  class="w-full flex items-center gap-2 px-3 py-2.5 rounded-xl hover:bg-red-50 hover:text-red-600 transition-colors text-sm text-zinc-700"
                >
                  <Icon icon="hugeicons:logout-01" class="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </div>
            </Transition>
          </div>
        </div>
      </div>
    </aside>

    <!-- Overlay for mobile -->
    <div
      v-if="isSidebarOpen"
      class="fixed inset-0 bg-black/20 backdrop-blur-sm z-30 lg:hidden transition-opacity duration-300"
      @click="toggleSidebar"
    />

    <!-- Main content -->
    <div class="flex-1 flex flex-col overflow-hidden lg:ml-72 transition-all duration-500">
      <!-- Header -->
      <header class="h-20 flex items-center justify-between px-8 flex-shrink-0">
        <div class="flex items-center gap-4">
          <button
            @click="toggleSidebar"
            class="lg:hidden p-2 rounded-xl hover:bg-zinc-100 transition-colors -ml-2"
          >
            <Icon icon="hugeicons:menu-01" class="w-6 h-6 text-zinc-900" />
          </button>
          
          <h2 class="text-xl font-medium text-zinc-900 tracking-tight hidden md:block">
            {{ $route.name === 'dashboard' ? 'Overview' : '' }}
          </h2>
        </div>

        <div class="flex items-center gap-6">
          <!-- Command Bar Trigger -->
          <button class="hidden md:flex items-center gap-3 px-4 py-2.5 bg-white border border-zinc-200/50 rounded-full shadow-sm hover:shadow-md hover:border-zinc-300 transition-all duration-300 w-64 group">
            <Icon icon="hugeicons:search-01" class="w-4 h-4 text-zinc-400 group-hover:text-zinc-600" />
            <span class="text-sm text-zinc-400 group-hover:text-zinc-600">Search anything...</span>
            <span class="ml-auto text-xs text-zinc-300 border border-zinc-200 px-1.5 py-0.5 rounded">⌘K</span>
          </button>

          <button class="p-2.5 rounded-full hover:bg-zinc-100 transition-colors relative group">
            <Icon icon="hugeicons:notification-03" class="w-5 h-5 text-zinc-500 group-hover:text-zinc-900" />
            <span class="absolute top-2.5 right-2.5 w-1.5 h-1.5 bg-red-500 rounded-full ring-2 ring-white"></span>
          </button>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 overflow-y-auto px-8 pb-8">
        <div class="max-w-[1600px] mx-auto">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>
