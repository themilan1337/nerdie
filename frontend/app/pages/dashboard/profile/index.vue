<script setup lang="ts">
import { computed } from 'vue'
import { Icon } from '@iconify/vue'

definePageMeta({
  layout: 'dashboard'
})

const { userData, signOut } = useAuth()

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

const handleLogout = async () => {
  await signOut()
}
</script>

<template>
  <div class="max-w-4xl mx-auto space-y-8 py-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-4xl font-['Questrial'] font-light tracking-tight text-zinc-900 mb-2">Profile Settings.</h1>
        <p class="text-zinc-500 font-light">Manage your account and preferences.</p>
      </div>
    </div>

    <!-- Profile Card -->
    <div class="glass-panel p-8 rounded-[2rem] relative overflow-hidden group">
      <!-- Decorative background -->
      <div class="absolute top-0 right-0 w-64 h-64 bg-zinc-100/50 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 group-hover:bg-zinc-200/50 transition-colors duration-700"></div>
      
      <div class="relative flex flex-col md:flex-row items-center gap-8">
        <div class="relative group/avatar cursor-pointer">
          <div class="w-24 h-24 rounded-full bg-zinc-100 flex items-center justify-center overflow-hidden border-2 border-white shadow-lg group-hover/avatar:scale-105 transition-transform duration-300">
            <img
              v-if="userData?.photoUrl"
              :src="userData.photoUrl"
              :alt="displayName"
              class="w-full h-full object-cover"
            />
            <span v-else class="text-2xl font-light text-zinc-900">{{ userInitials }}</span>
          </div>
          <div class="absolute bottom-0 right-0 w-8 h-8 rounded-full bg-black text-white flex items-center justify-center border-2 border-white shadow-md group-hover/avatar:scale-110 transition-transform duration-300">
            <Icon icon="hugeicons:camera-01" class="w-4 h-4" />
          </div>
        </div>

        <div class="flex-1 text-center md:text-left space-y-1">
          <h2 class="text-2xl font-medium text-zinc-900">{{ displayName }}</h2>
          <p class="text-zinc-500 font-light">{{ userEmail }}</p>
          <div class="pt-2">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-zinc-100 text-xs font-medium text-zinc-600">
              <Icon icon="hugeicons:check-circle-01" class="w-3.5 h-3.5" />
              Pro Plan
            </span>
          </div>
        </div>

        <button class="px-6 py-2 rounded-full border border-zinc-200 hover:bg-zinc-50 hover:border-zinc-300 text-zinc-900 font-medium text-sm transition-all duration-300 bg-white shadow-sm">
          Edit Profile
        </button>
      </div>
    </div>

    <!-- Details Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- Personal Info -->
      <div class="glass-panel p-6 rounded-[2rem] space-y-6">
        <h3 class="text-lg font-medium text-zinc-900 flex items-center gap-2">
          <Icon icon="hugeicons:user" class="w-5 h-5 text-zinc-400" />
          Personal Information
        </h3>
        
        <div class="space-y-4">
          <div class="group">
            <label class="block text-xs font-medium text-zinc-400 mb-1.5 uppercase tracking-wider">Full Name</label>
            <div class="p-3 bg-zinc-50/50 rounded-xl border border-zinc-100 group-hover:border-zinc-200 transition-colors text-zinc-900 font-light">
              {{ displayName }}
            </div>
          </div>
          
          <div class="group">
            <label class="block text-xs font-medium text-zinc-400 mb-1.5 uppercase tracking-wider">Email Address</label>
            <div class="p-3 bg-zinc-50/50 rounded-xl border border-zinc-100 group-hover:border-zinc-200 transition-colors text-zinc-900 font-light">
              {{ userEmail }}
            </div>
          </div>
        </div>
      </div>

      <!-- Preferences -->
      <div class="glass-panel p-6 rounded-[2rem] space-y-6">
        <h3 class="text-lg font-medium text-zinc-900 flex items-center gap-2">
          <Icon icon="hugeicons:settings-01" class="w-5 h-5 text-zinc-400" />
          Preferences
        </h3>
        
        <div class="space-y-3">
          <button class="w-full flex items-center justify-between p-4 rounded-xl hover:bg-zinc-50 transition-colors group">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-lg bg-zinc-50 flex items-center justify-center group-hover:bg-white transition-colors">
                <Icon icon="hugeicons:moon-02" class="w-5 h-5 text-zinc-400 group-hover:text-zinc-900 transition-colors" />
              </div>
              <div class="text-left">
                <p class="font-medium text-zinc-900">Appearance</p>
                <p class="text-xs text-zinc-400">System Default</p>
              </div>
            </div>
            <Icon icon="hugeicons:arrow-right-01" class="w-4 h-4 text-zinc-300 group-hover:text-zinc-900 transition-colors" />
          </button>

          <button class="w-full flex items-center justify-between p-4 rounded-xl hover:bg-zinc-50 transition-colors group">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 rounded-lg bg-zinc-50 flex items-center justify-center group-hover:bg-white transition-colors">
                <Icon icon="hugeicons:notification-01" class="w-5 h-5 text-zinc-400 group-hover:text-zinc-900 transition-colors" />
              </div>
              <div class="text-left">
                <p class="font-medium text-zinc-900">Notifications</p>
                <p class="text-xs text-zinc-400">Enabled</p>
              </div>
            </div>
            <Icon icon="hugeicons:arrow-right-01" class="w-4 h-4 text-zinc-300 group-hover:text-zinc-900 transition-colors" />
          </button>
        </div>
      </div>
    </div>

    <!-- Danger Zone -->
    <div class="glass-panel p-6 rounded-[2rem]">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-medium text-red-500 mb-1">Sign Out</h3>
          <p class="text-sm text-zinc-400 font-light">Securely log out of your account on this device.</p>
        </div>
        <button
          @click="handleLogout"
          class="px-6 py-2.5 bg-red-50 hover:bg-red-100 text-red-600 rounded-full font-medium text-sm transition-colors flex items-center gap-2"
        >
          <Icon icon="hugeicons:logout-01" class="w-4 h-4" />
          Log Out
        </button>
      </div>
    </div>
  </div>
</template>
