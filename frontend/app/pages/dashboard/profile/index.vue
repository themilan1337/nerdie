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
  <div>
    <!-- Page Header -->
    <div class="mb-12">
      <h1 class="text-4xl font-['Questrial'] font-light tracking-tight text-zinc-900 mb-3">Profile</h1>
      <p class="text-zinc-500 font-light text-base">Manage your account and preferences</p>
    </div>

    <div class="space-y-8">

    <!-- Profile Card -->
    <div class="glass-panel p-8 rounded-[2rem] relative overflow-hidden group">
      <!-- Decorative background -->
      <div class="absolute top-0 right-0 w-64 h-64 bg-zinc-100/50 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 group-hover:bg-zinc-200/50 transition-colors duration-700"></div>
      
      <div class="relative flex flex-col md:flex-row items-center gap-8">
        <div class="relative group/avatar cursor-pointer">
          <div class="w-24 h-24 rounded-full bg-zinc-100 flex items-center justify-center overflow-hidden border-2 border-white shadow-lg transition-transform duration-300">
            <img
              v-if="userData?.photoUrl"
              :src="userData.photoUrl"
              :alt="displayName"
              class="w-full h-full object-cover"
            />
            <span v-else class="text-2xl font-light text-zinc-900">{{ userInitials }}</span>
          </div>
          <div class="absolute bottom-0 right-0 w-8 h-8 rounded-full bg-black text-white flex items-center justify-center border-2 border-white shadow-md transition-transform duration-300">
            <Icon icon="hugeicons:camera-01" class="w-4 h-4" />
          </div>
        </div>

        <div class="flex-1 text-center md:text-left space-y-1">
          <h2 class="text-2xl font-['Questrial'] text-zinc-900">{{ displayName }}</h2>
          <p class="text-zinc-500 font-light">{{ userEmail }}</p>
        </div>
      </div>
    </div>

    <!-- Details Grid -->
    <div class="grid grid-cols-1 gap-6">
      <!-- Personal Info -->
      <div class="glass-panel p-6 rounded-[2rem] space-y-6">
        <h3 class="text-lg font-['Questrial'] text-zinc-900 flex items-center gap-2">
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
    </div>

    <!-- Danger Zone -->
    <div class="glass-panel p-6 rounded-[2rem]">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-['Questrial'] text-red-500 mb-1">Sign Out</h3>
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
  </div>
</template>
