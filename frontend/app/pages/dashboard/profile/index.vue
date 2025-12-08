<script setup lang="ts">
import { computed } from 'vue'
import { LogOut, Mail, Calendar } from 'lucide-vue-next'

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
  <div class="p-6 lg:p-8">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 ins">Profile</h1>
      <p class="text-gray-500 mt-1">View your account information</p>
    </div>

    <!-- Profile Content -->
    <div class="max-w-2xl">
      <div class="bg-white rounded-2xl border border-gray-200 p-8">
        <!-- User Avatar and Name -->
        <div class="flex flex-col items-center mb-8">
          <img
            v-if="userData?.photoUrl"
            :src="userData.photoUrl"
            :alt="displayName"
            class="w-24 h-24 rounded-full mb-4"
          />
          <div
            v-else
            class="w-24 h-24 rounded-full bg-gradient-to-br from-orange-400 to-pink-500 flex items-center justify-center mb-4"
          >
            <span class="text-white font-bold text-3xl ins">{{ userInitials }}</span>
          </div>
          <h2 class="text-2xl font-bold text-gray-900 ins">{{ displayName }}</h2>
          <p class="text-gray-500 mt-1">{{ userEmail }}</p>
        </div>

        <!-- User Information -->
        <div class="space-y-4 mb-8">
          <div class="p-4 bg-gray-50 rounded-xl">
            <div class="flex items-center gap-3">
              <Mail class="w-5 h-5 text-gray-400" />
              <div>
                <p class="text-xs text-gray-500">Email Address</p>
                <p class="text-sm font-medium text-gray-900">{{ userEmail }}</p>
              </div>
            </div>
          </div>

          <div class="p-4 bg-gray-50 rounded-xl">
            <div class="flex items-center gap-3">
              <Calendar class="w-5 h-5 text-gray-400" />
              <div>
                <p class="text-xs text-gray-500">Account Status</p>
                <p class="text-sm font-medium text-green-600">Active</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Logout Button -->
        <div class="pt-6 border-t border-gray-200">
          <button
            @click="handleLogout"
            class="w-full flex items-center justify-center gap-2 px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-xl font-medium ins transition-colors"
          >
            <LogOut class="w-5 h-5" />
            Logout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
