<script setup lang="ts">
import { ref } from 'vue'
import { User, Mail, Calendar, Key, Bell, Globe, Shield, Download } from 'lucide-vue-next'

definePageMeta({
  layout: 'dashboard'
})

const activeTab = ref('general')

const tabs = [
  { id: 'general', name: 'General', icon: User },
  { id: 'security', name: 'Security', icon: Shield },
  { id: 'notifications', name: 'Notifications', icon: Bell },
  { id: 'preferences', name: 'Preferences', icon: Globe },
]

const userProfile = ref({
  name: 'John Doe',
  email: 'john.doe@example.com',
  joinedDate: 'January 2024',
  avatar: '',
  bio: 'AI enthusiast and developer',
  location: 'San Francisco, CA',
  timezone: 'PST (UTC-8)',
})

const notificationSettings = ref({
  emailNotifications: true,
  chatUpdates: true,
  documentUploads: false,
  systemAlerts: true,
  weeklyReports: false,
})

const preferences = ref({
  language: 'English',
  theme: 'Light',
  defaultModel: 'Gemini Pro',
  responseLength: 'Medium',
})

const apiUsage = ref({
  current: 4523,
  limit: 10000,
  percentage: 45.23
})

const handleSaveProfile = () => {
  console.log('Saving profile...')
}

const handleChangePassword = () => {
  console.log('Changing password...')
}

const handleExportData = () => {
  console.log('Exporting data...')
}
</script>

<template>
  <div class="p-6 lg:p-8">
    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 ins">Profile Settings</h1>
      <p class="text-gray-500 mt-1">Manage your account settings and preferences</p>
    </div>

    <!-- Tabs -->
    <div class="border-b border-gray-200 mb-8">
      <nav class="flex gap-8">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'flex items-center gap-2 px-1 py-4 border-b-2 font-medium transition-all ins',
            activeTab === tab.id
              ? 'border-black text-black'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
          ]"
        >
          <component :is="tab.icon" class="w-5 h-5" />
          {{ tab.name }}
        </button>
      </nav>
    </div>

    <!-- Tab Content -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- General Settings -->
      <div v-if="activeTab === 'general'" class="lg:col-span-2 space-y-6">
        <div class="bg-white rounded-2xl border border-gray-200 p-6">
          <h2 class="text-xl font-bold text-gray-900 ins mb-6">Profile Information</h2>

          <!-- Avatar Upload -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-3">Profile Picture</label>
            <div class="flex items-center gap-4">
              <div class="w-20 h-20 rounded-full bg-gradient-to-br from-orange-400 to-pink-500 flex items-center justify-center">
                <span class="text-white font-bold text-2xl ins">{{ userProfile.name.charAt(0) }}</span>
              </div>
              <div>
                <button class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm font-medium ins transition-colors">
                  Change Photo
                </button>
                <p class="text-xs text-gray-500 mt-1">JPG, PNG or GIF. Max 2MB</p>
              </div>
            </div>
          </div>

          <!-- Form Fields -->
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
              <input
                v-model="userProfile.name"
                type="text"
                class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
              <input
                v-model="userProfile.email"
                type="email"
                class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Bio</label>
              <textarea
                v-model="userProfile.bio"
                rows="3"
                class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all resize-none"
              />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Location</label>
                <input
                  v-model="userProfile.location"
                  type="text"
                  class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Timezone</label>
                <select
                  v-model="userProfile.timezone"
                  class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
                >
                  <option>PST (UTC-8)</option>
                  <option>EST (UTC-5)</option>
                  <option>GMT (UTC+0)</option>
                  <option>CET (UTC+1)</option>
                </select>
              </div>
            </div>
          </div>

          <div class="flex justify-end gap-3 mt-6 pt-6 border-t border-gray-200">
            <button class="px-6 py-2.5 bg-gray-100 hover:bg-gray-200 rounded-full font-medium ins transition-colors">
              Cancel
            </button>
            <button
              @click="handleSaveProfile"
              class="px-6 py-2.5 bg-black hover:bg-gray-800 text-white rounded-full font-medium ins transition-colors"
            >
              Save Changes
            </button>
          </div>
        </div>
      </div>

      <!-- Security Settings -->
      <div v-if="activeTab === 'security'" class="lg:col-span-2 space-y-6">
        <div class="bg-white rounded-2xl border border-gray-200 p-6">
          <h2 class="text-xl font-bold text-gray-900 ins mb-6">Security Settings</h2>

          <div class="space-y-6">
            <!-- Change Password -->
            <div class="p-4 bg-gray-50 rounded-xl">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-900 mb-1 ins">Password</h3>
                  <p class="text-sm text-gray-500">Last changed 3 months ago</p>
                </div>
                <button
                  @click="handleChangePassword"
                  class="px-4 py-2 bg-white hover:bg-gray-100 border border-gray-200 rounded-lg text-sm font-medium ins transition-colors"
                >
                  Change
                </button>
              </div>
            </div>

            <!-- Two-Factor Authentication -->
            <div class="p-4 bg-gray-50 rounded-xl">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-900 mb-1 ins">Two-Factor Authentication</h3>
                  <p class="text-sm text-gray-500">Add an extra layer of security</p>
                </div>
                <button class="px-4 py-2 bg-white hover:bg-gray-100 border border-gray-200 rounded-lg text-sm font-medium ins transition-colors">
                  Enable
                </button>
              </div>
            </div>

            <!-- API Keys -->
            <div class="p-4 bg-gray-50 rounded-xl">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <h3 class="font-semibold text-gray-900 mb-1 ins">API Keys</h3>
                  <p class="text-sm text-gray-500">Manage your API access keys</p>
                </div>
                <button class="px-4 py-2 bg-white hover:bg-gray-100 border border-gray-200 rounded-lg text-sm font-medium ins transition-colors">
                  Manage
                </button>
              </div>
            </div>

            <!-- Active Sessions -->
            <div class="p-4 bg-gray-50 rounded-xl">
              <h3 class="font-semibold text-gray-900 mb-3 ins">Active Sessions</h3>
              <div class="space-y-3">
                <div class="flex items-center justify-between p-3 bg-white rounded-lg">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                      <Globe class="w-5 h-5 text-gray-600" />
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-900">Chrome on MacOS</p>
                      <p class="text-xs text-gray-500">San Francisco, CA • Current session</p>
                    </div>
                  </div>
                  <span class="text-xs text-green-600 font-medium">Active</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Notifications Settings -->
      <div v-if="activeTab === 'notifications'" class="lg:col-span-2 space-y-6">
        <div class="bg-white rounded-2xl border border-gray-200 p-6">
          <h2 class="text-xl font-bold text-gray-900 ins mb-6">Notification Preferences</h2>

          <div class="space-y-4">
            <div
              v-for="(value, key) in notificationSettings"
              :key="key"
              class="flex items-center justify-between p-4 bg-gray-50 rounded-xl"
            >
              <div>
                <h3 class="font-medium text-gray-900 capitalize ins">{{ key.replace(/([A-Z])/g, ' $1').trim() }}</h3>
                <p class="text-sm text-gray-500 mt-1">Receive notifications about this activity</p>
              </div>
              <button
                @click="notificationSettings[key] = !notificationSettings[key]"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                  value ? 'bg-black' : 'bg-gray-300'
                ]"
              >
                <span
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                    value ? 'translate-x-6' : 'translate-x-1'
                  ]"
                />
              </button>
            </div>
          </div>

          <div class="flex justify-end gap-3 mt-6 pt-6 border-t border-gray-200">
            <button class="px-6 py-2.5 bg-black hover:bg-gray-800 text-white rounded-full font-medium ins transition-colors">
              Save Preferences
            </button>
          </div>
        </div>
      </div>

      <!-- Preferences Settings -->
      <div v-if="activeTab === 'preferences'" class="lg:col-span-2 space-y-6">
        <div class="bg-white rounded-2xl border border-gray-200 p-6">
          <h2 class="text-xl font-bold text-gray-900 ins mb-6">App Preferences</h2>

          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Language</label>
              <select
                v-model="preferences.language"
                class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
              >
                <option>English</option>
                <option>Spanish</option>
                <option>French</option>
                <option>German</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Theme</label>
              <select
                v-model="preferences.theme"
                class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
              >
                <option>Light</option>
                <option>Dark</option>
                <option>Auto</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Default AI Model</label>
              <select
                v-model="preferences.defaultModel"
                class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
              >
                <option>Gemini Pro</option>
                <option>Gemini Flash</option>
                <option>Gemini Ultra</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Response Length</label>
              <select
                v-model="preferences.responseLength"
                class="w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
              >
                <option>Short</option>
                <option>Medium</option>
                <option>Long</option>
                <option>Detailed</option>
              </select>
            </div>
          </div>

          <div class="flex justify-end gap-3 mt-6 pt-6 border-t border-gray-200">
            <button class="px-6 py-2.5 bg-black hover:bg-gray-800 text-white rounded-full font-medium ins transition-colors">
              Save Preferences
            </button>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <div class="space-y-6">
        <!-- Account Info Card -->
        <div class="bg-white rounded-2xl border border-gray-200 p-6">
          <h3 class="text-lg font-bold text-gray-900 ins mb-4">Account Info</h3>
          <div class="space-y-3">
            <div class="flex items-center gap-3">
              <Calendar class="w-4 h-4 text-gray-400" />
              <div>
                <p class="text-xs text-gray-500">Member since</p>
                <p class="text-sm font-medium text-gray-900">{{ userProfile.joinedDate }}</p>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <Mail class="w-4 h-4 text-gray-400" />
              <div>
                <p class="text-xs text-gray-500">Email status</p>
                <p class="text-sm font-medium text-green-600">Verified</p>
              </div>
            </div>
          </div>
        </div>

        <!-- API Usage Card -->
        <div class="bg-gradient-to-br from-black to-gray-800 rounded-2xl p-6 text-white">
          <h3 class="text-lg font-bold mb-4 ins">API Usage</h3>
          <div class="space-y-4">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm text-gray-300">This month</span>
                <span class="text-sm font-medium">{{ apiUsage.current }} / {{ apiUsage.limit }}</span>
              </div>
              <div class="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                <div
                  class="h-full bg-gradient-to-r from-green-400 to-blue-500 rounded-full transition-all"
                  :style="{ width: `${apiUsage.percentage}%` }"
                />
              </div>
            </div>
            <p class="text-xs text-gray-400">{{ (100 - apiUsage.percentage).toFixed(1) }}% remaining</p>
          </div>
        </div>

        <!-- Export Data Card -->
        <div class="bg-white rounded-2xl border border-gray-200 p-6">
          <h3 class="text-lg font-bold text-gray-900 ins mb-2">Export Data</h3>
          <p class="text-sm text-gray-500 mb-4">Download all your data in JSON format</p>
          <button
            @click="handleExportData"
            class="w-full px-4 py-2.5 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium ins transition-colors flex items-center justify-center gap-2"
          >
            <Download class="w-4 h-4" />
            Export Data
          </button>
        </div>

        <!-- Danger Zone -->
        <div class="bg-red-50 rounded-2xl border border-red-200 p-6">
          <h3 class="text-lg font-bold text-red-900 ins mb-2">Danger Zone</h3>
          <p class="text-sm text-red-600 mb-4">Irreversible actions</p>
          <button class="w-full px-4 py-2.5 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium ins transition-colors">
            Delete Account
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
