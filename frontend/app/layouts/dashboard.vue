<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { Icon } from '@iconify/vue'

const { isSidebarExpanded, toggleSidebar: toggleDesktopSidebar } = useSidebar()
const isSidebarOpen = ref(false)
const showLogoutDropdown = ref(false)
const showNotifications = ref(false)
const showSearch = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)
const notificationRef = ref<HTMLElement | null>(null)
const searchQuery = ref('')

const { userData, signOut, initAuthListener } = useAuth()

// Initialize auth listener
onMounted(() => {
  initAuthListener()
  document.addEventListener('click', handleClickOutside)

  // Keyboard shortcut for search (Cmd+K or Ctrl+K)
  document.addEventListener('keydown', handleKeyboardShortcut)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeyboardShortcut)
})

// Handle keyboard shortcuts
const handleKeyboardShortcut = (event: KeyboardEvent) => {
  if ((event.metaKey || event.ctrlKey) && event.key === 'k') {
    event.preventDefault()
    showSearch.value = !showSearch.value
  }
  if (event.key === 'Escape') {
    showSearch.value = false
    showNotifications.value = false
  }
}

// Handle click outside dropdown
const handleClickOutside = (event: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    showLogoutDropdown.value = false
  }
  if (notificationRef.value && !notificationRef.value.contains(event.target as Node)) {
    showNotifications.value = false
  }
}

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: 'hugeicons:home-01' },
  { name: 'New Chat', href: '/dashboard/chat/new', icon: 'hugeicons:plus-sign' },
  { name: 'Chats', href: '/dashboard/chat', icon: 'hugeicons:bubble-chat' },
  { name: 'RAG Management', href: '/dashboard/rag', icon: 'hugeicons:database-01' },
  { name: 'Profile', href: '/dashboard/profile', icon: 'hugeicons:user' },
]

const toggleMobileSidebar = () => {
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
        'fixed inset-y-0 left-0 z-40 bg-zinc-50 border-r border-zinc-200/50 transition-all duration-300 ease-in-out lg:translate-x-0',
        isSidebarExpanded ? 'lg:w-72' : 'lg:w-20',
        'w-72',
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
    >
      <div class="h-full flex flex-col transition-all duration-300" :class="isSidebarExpanded ? 'p-6' : 'py-6 px-3'">
        <!-- Logo -->
        <div class="h-12 flex items-center mb-8 transition-all duration-300" :class="isSidebarExpanded ? 'px-2' : 'justify-center'">
          <h1 v-if="isSidebarExpanded" class="font-['Questrial'] text-4xl font-bold tracking-tight text-zinc-900 whitespace-nowrap">nerdie.</h1>
          <h1 v-else class="font-['Questrial'] text-2xl font-bold tracking-tight text-zinc-900">n.</h1>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 space-y-2 flex flex-col" :class="{ 'items-center': !isSidebarExpanded }">
          <NuxtLink
            v-for="item in navigation"
            :key="item.name"
            :to="item.href"
            class="flex items-center text-zinc-500 hover:text-zinc-900 hover:bg-zinc-100 transition-all duration-300 group relative overflow-hidden"
            :class="[
              isSidebarExpanded ? 'gap-3 px-4 py-3 rounded-2xl w-full' : 'rounded-full w-12 h-12 justify-center',
            ]"
            active-class="!bg-black !text-white shadow-lg shadow-black/5"
          >
            <Icon :icon="item.icon" class="w-5 h-5 flex-shrink-0" />
            <span
              v-if="isSidebarExpanded"
              class="font-medium text-sm tracking-wide whitespace-nowrap"
            >
              {{ item.name }}
            </span>
          </NuxtLink>
        </nav>

        <!-- User section -->
        <div class="mt-auto pt-6 border-t border-zinc-200/50" :class="{ 'flex justify-center': !isSidebarExpanded }">
          <div class="relative" ref="dropdownRef">
            <button
              @click="showLogoutDropdown = !showLogoutDropdown"
              class="flex items-center p-2 rounded-2xl hover:bg-zinc-100 transition-all duration-300 group"
              :class="[
                isSidebarExpanded ? 'gap-3 w-full' : 'justify-center w-12 h-12 rounded-full'
              ]"
            >
              <div class="relative flex-shrink-0">
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
              </div>

              <div
                v-if="isSidebarExpanded"
                class="flex-1 min-w-0 text-left"
              >
                <p class="text-sm font-semibold text-zinc-900 truncate group-hover:text-black transition-colors">{{ displayName }}</p>
              </div>

              <Icon
                v-if="isSidebarExpanded"
                icon="hugeicons:more-horizontal"
                class="w-5 h-5 text-zinc-400 group-hover:text-zinc-600 flex-shrink-0"
              />
            </button>

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
      @click="toggleMobileSidebar"
    />

    <!-- Main content -->
    <div 
      class="flex-1 flex flex-col overflow-hidden transition-all duration-300 ease-in-out"
      :class="isSidebarExpanded ? 'lg:ml-72' : 'lg:ml-20'"
    >
      <!-- Header -->
      <header class="h-16 flex items-center border-b border-zinc-200/50 justify-between px-8 flex-shrink-0">
        <div class="flex items-center gap-4">
          <button
            @click="toggleMobileSidebar"
            class="lg:hidden p-2 rounded-xl hover:bg-zinc-100 transition-colors -ml-2"
          >
            <Icon icon="hugeicons:menu-01" class="w-6 h-6 text-zinc-900" />
          </button>

          <button
            @click="toggleDesktopSidebar"
            class="hidden lg:flex p-2 rounded-xl hover:bg-zinc-100 transition-colors text-zinc-500 hover:text-zinc-900"
            :title="isSidebarExpanded ? 'Collapse Sidebar' : 'Expand Sidebar'"
          >
            <Icon :icon="isSidebarExpanded ? 'hugeicons:sidebar-left' : 'hugeicons:sidebar-right'" class="w-6 h-6" />
          </button>
        </div>

        <div class="flex items-center gap-6">
          <!-- Search Trigger -->
          <button
            @click="showSearch = true"
            class="hidden md:flex items-center gap-3 px-4 py-2.5 bg-white border border-zinc-200/50 rounded-full shadow-sm hover:shadow-md hover:border-zinc-300 transition-all duration-300 w-64 group"
          >
            <Icon icon="hugeicons:search-01" class="w-4 h-4 text-zinc-400 group-hover:text-zinc-600" />
            <span class="text-sm text-zinc-400 group-hover:text-zinc-600">Search anything...</span>
            <span class="ml-auto text-xs text-zinc-300 border border-zinc-200 px-1.5 py-0.5 rounded">⌘K</span>
          </button>

          <!-- Notifications -->
          <div class="relative z-[99999]" ref="notificationRef">
            <button
              @click="showNotifications = !showNotifications"
              class="p-2.5 rounded-full hover:bg-zinc-100 transition-colors relative group"
              :class="{ 'bg-zinc-100': showNotifications }"
            >
              <Icon icon="hugeicons:notification-03" class="w-5 h-5 text-zinc-500 group-hover:text-zinc-900" />
            </button>

            <!-- Notifications Dropdown -->
            <Transition
              enter-active-class="transition ease-out duration-200"
              enter-from-class="opacity-0 translate-y-2 scale-95"
              enter-to-class="opacity-100 translate-y-0 scale-100"
              leave-active-class="transition ease-in duration-150"
              leave-from-class="opacity-100 translate-y-0 scale-100"
              leave-to-class="opacity-0 translate-y-2 scale-95"
            >
              <div
                v-if="showNotifications"
                class="absolute right-0 top-full mt-3 w-80 bg-white/95 backdrop-blur-xl border border-zinc-200/50 shadow-[0_8px_30px_rgb(0,0,0,0.12)] rounded-2xl overflow-hidden"
              >
                <div class="p-4 border-b border-zinc-200/50">
                  <h3 class="font-medium text-zinc-900">Notifications</h3>
                </div>
                <div class="p-8 text-center">
                  <div class="w-12 h-12 bg-zinc-50 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Icon icon="hugeicons:notification-03" class="w-6 h-6 text-zinc-300" />
                  </div>
                  <p class="text-sm text-zinc-500">No notifications</p>
                </div>
              </div>
            </Transition>
          </div>
        </div>
      </header>

      <!-- Page content -->
      <main class="flex-1 overflow-y-auto px-8 py-8">
        <div class="max-w-[1600px] mx-auto page-wrapper">
          <slot />
        </div>
      </main>
    </div>

    <!-- Search Modal -->
    <Teleport to="body">
      <Transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="showSearch"
          class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-start justify-center pt-[10vh] px-4"
          @click="showSearch = false"
        >
          <div
            @click.stop
            class="w-full max-w-2xl bg-white rounded-2xl shadow-2xl overflow-hidden animate-[slideUp_0.3s_ease-out]"
          >
            <!-- Search Input -->
            <div class="flex items-center gap-3 px-6 py-4 border-b border-zinc-200">
              <Icon icon="hugeicons:search-01" class="w-5 h-5 text-zinc-400 flex-shrink-0" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search chats, documents, and more..."
                class="flex-1 text-base text-zinc-900 placeholder-zinc-400 focus:outline-none bg-transparent"
                autofocus
              />
              <button
                @click="showSearch = false"
                class="text-xs text-zinc-400 hover:text-zinc-600 px-2 py-1 border border-zinc-200 rounded"
              >
                ESC
              </button>
            </div>

            <!-- Search Results -->
            <div class="max-h-[60vh] overflow-y-auto">
              <div v-if="!searchQuery.trim()" class="p-8 text-center">
                <div class="w-16 h-16 bg-zinc-50 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Icon icon="hugeicons:search-01" class="w-8 h-8 text-zinc-300" />
                </div>
                <p class="text-sm text-zinc-500 mb-2">Start typing to search</p>
                <p class="text-xs text-zinc-400">Search across chats, documents, and pages</p>
              </div>

              <div v-else class="p-4">
                <div class="text-center py-12">
                  <div class="w-16 h-16 bg-zinc-50 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Icon icon="hugeicons:search-01" class="w-8 h-8 text-zinc-300" />
                  </div>
                  <p class="text-sm text-zinc-500 mb-1">No results found for "{{ searchQuery }}"</p>
                  <p class="text-xs text-zinc-400">Try searching for something else</p>
                </div>
              </div>
            </div>

            <!-- Quick Actions -->
            <div v-if="!searchQuery.trim()" class="border-t border-zinc-200 p-4">
              <p class="text-xs font-medium text-zinc-400 uppercase tracking-wide mb-3 px-2">Quick Actions</p>
              <div class="space-y-1">
                <NuxtLink
                  to="/dashboard/chat/new"
                  @click="showSearch = false"
                  class="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-zinc-50 transition-colors text-sm text-zinc-700 group"
                >
                  <Icon icon="hugeicons:plus-sign" class="w-4 h-4 text-zinc-400 group-hover:text-zinc-900" />
                  <span>New Chat</span>
                </NuxtLink>
                <NuxtLink
                  to="/dashboard/rag"
                  @click="showSearch = false"
                  class="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-zinc-50 transition-colors text-sm text-zinc-700 group"
                >
                  <Icon icon="hugeicons:file-upload" class="w-4 h-4 text-zinc-400 group-hover:text-zinc-900" />
                  <span>Upload Document</span>
                </NuxtLink>
                <NuxtLink
                  to="/dashboard/chat"
                  @click="showSearch = false"
                  class="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-zinc-50 transition-colors text-sm text-zinc-700 group"
                >
                  <Icon icon="hugeicons:bubble-chat" class="w-4 h-4 text-zinc-400 group-hover:text-zinc-900" />
                  <span>View Chats</span>
                </NuxtLink>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
