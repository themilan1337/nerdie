<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Icon } from '@iconify/vue'
import type { Document } from '~/types/ingestion'

definePageMeta({
  layout: 'dashboard'
})

const searchQuery = ref('')
const selectedFilter = ref('all')
const showSuccessNotification = ref(false)
const successMessage = ref('')
const showErrorNotification = ref(false)
const errorMessage = ref('')

const {
  isLoading: isIngesting,
  error: ingestionError,
  uploadProgress,
  processFile,
  ingestText,
  healthCheck
} = useIngestion()

const filterOptions = [
  { value: 'all', label: 'All Documents' },
  { value: 'pdf', label: 'PDFs' },
  { value: 'image', label: 'Images' },
  { value: 'text', label: 'Text Files' },
  { value: 'processing', label: 'Processing' },
]

const documents = ref<Document[]>([])

const stats = computed(() => ({
  total: documents.value.length,
  processed: documents.value.filter(d => d.status === 'processed').length,
  processing: documents.value.filter(d => d.status === 'processing').length,
  totalChunks: documents.value.reduce((sum, d) => sum + d.chunks, 0),
  totalEmbeddings: documents.value.reduce((sum, d) => sum + d.embeddings, 0),
}))

const filteredDocuments = computed(() => {
  let filtered = documents.value

  if (searchQuery.value) {
    filtered = filtered.filter(doc =>
      doc.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  if (selectedFilter.value !== 'all') {
    if (selectedFilter.value === 'processing') {
      filtered = filtered.filter(doc => doc.status === 'processing')
    } else {
      filtered = filtered.filter(doc =>
        doc.type.toLowerCase() === selectedFilter.value
      )
    }
  }

  return filtered
})

const showNotification = (message: string, type: 'success' | 'error') => {
  if (type === 'success') {
    successMessage.value = message
    showSuccessNotification.value = true
    setTimeout(() => {
      showSuccessNotification.value = false
    }, 5000)
  } else {
    errorMessage.value = message
    showErrorNotification.value = true
    setTimeout(() => {
      showErrorNotification.value = false
    }, 5000)
  }
}

const handleFileUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  const files = input.files

  if (!files || files.length === 0) return

  for (let i = 0; i < files.length; i++) {
    const file = files[i]
    if (!file) continue

    const fileType = file.type.includes('pdf')
      ? 'PDF'
      : file.type.includes('image')
      ? 'Image'
      : 'Text'

    const tempDoc: Document = {
      id: `temp-${Date.now()}-${i}`,
      name: file.name || 'Untitled',
      type: fileType as 'PDF' | 'Image' | 'Text',
      size: `${(file.size / 1024 / 1024).toFixed(2)} MB`,
      uploadedAt: new Date().toISOString().split('T')[0],
      status: 'processing',
      chunks: 0,
      embeddings: 0,
      metadata: {
        filename: file.name,
        fileType: file.type,
        fileSize: file.size,
      }
    }

    documents.value.unshift(tempDoc)

    try {
      const response = await processFile(file)

      const docIndex = documents.value.findIndex(d => d.id === tempDoc.id)
      if (docIndex !== -1 && documents.value[docIndex]) {
        // Create a new object with safely spread properties to avoid type errors
        const updatedDoc = {
          ...documents.value[docIndex]!,
          id: response.documentId || tempDoc.id,
          status: 'processed' as const,
          chunks: response.chunks || 0,
          embeddings: response.embeddings || 0,
        }
        documents.value[docIndex] = updatedDoc as Document
      }

      showNotification(`Successfully processed ${file.name}`, 'success')
    } catch (err: any) {
      console.error('Upload error:', err)

      const docIndex = documents.value.findIndex(d => d.id === tempDoc.id)
      if (docIndex !== -1 && documents.value[docIndex]) {
        documents.value[docIndex]!.status = 'failed'
      }

      showNotification(`Failed to process ${file.name}: ${err.message}`, 'error')
    }
  }

  input.value = ''
}

const handleDelete = (id: string) => {
  if (confirm('Are you sure you want to delete this document?')) {
    documents.value = documents.value.filter(doc => doc.id !== id)
    showNotification('Document deleted successfully', 'success')
  }
}

const handleDownload = (doc: Document) => {
  console.log('Downloading:', doc.name)
  showNotification('Download feature coming soon', 'error')
}

const handleView = (doc: Document) => {
  console.log('Viewing:', doc.name)
  showNotification('View feature coming soon', 'error')
}

const handleReprocess = async (doc: Document) => {
  console.log('Reprocessing:', doc.name)
  showNotification('Reprocess feature coming soon', 'error')
}

const getStatusBadge = (status: string) => {
  switch (status) {
    case 'processed':
      return { color: 'bg-green-100 text-green-700', icon: 'hugeicons:check-circle-01', text: 'Processed' }
    case 'processing':
      return { color: 'bg-blue-100 text-blue-700', icon: 'hugeicons:clock-01', text: 'Processing' }
    case 'failed':
      return { color: 'bg-red-100 text-red-700', icon: 'hugeicons:alert-circle', text: 'Failed' }
    default:
      return { color: 'bg-gray-100 text-gray-700', icon: 'hugeicons:clock-01', text: 'Unknown' }
  }
}

const checkServiceHealth = async () => {
  try {
    await healthCheck()
    console.log('Ingestion service is healthy')
  } catch (err) {
    console.error('Ingestion service health check failed:', err)
  }
}

onMounted(() => {
  checkServiceHealth()
})
</script>

<template>
  <div>
    <!-- Success Notification -->
    <Transition name="slide-down">
      <div v-if="showSuccessNotification" class="fixed top-6 right-6 z-50 pointer-events-none">
        <div class="glass-panel bg-white/90 backdrop-blur-xl border border-green-200 px-6 py-4 rounded-2xl flex items-center gap-3 shadow-lg max-w-md pointer-events-auto">
          <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0">
            <Icon icon="hugeicons:check-circle-01" class="w-5 h-5 text-green-600" />
          </div>
          <p class="text-sm font-medium text-green-900">{{ successMessage }}</p>
        </div>
      </div>
    </Transition>

    <!-- Error Notification -->
    <Transition name="slide-down">
      <div v-if="showErrorNotification" class="fixed top-6 right-6 z-50 pointer-events-none">
        <div class="glass-panel bg-white/90 backdrop-blur-xl border border-red-200 px-6 py-4 rounded-2xl flex items-center gap-3 shadow-lg max-w-md pointer-events-auto">
          <div class="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
            <Icon icon="hugeicons:alert-circle" class="w-5 h-5 text-red-600" />
          </div>
          <p class="text-sm font-medium text-red-900">{{ errorMessage }}</p>
        </div>
      </div>
    </Transition>

    <!-- Page Header -->
    <div class="mb-12">
      <h1 class="text-4xl font-['Questrial'] font-light tracking-tight text-zinc-900 mb-3">RAG Management</h1>
      <p class="text-zinc-500 font-light text-base">Manage documents for RAG processing to enhance AI responses with your data</p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
      <div class="glass-panel p-6 rounded-3xl">
        <p class="text-sm text-zinc-400 mb-2 font-medium">Total Docs</p>
        <p class="text-3xl font-light text-zinc-900">{{ stats.total }}</p>
      </div>
      <div class="glass-panel p-6 rounded-3xl">
        <p class="text-sm text-zinc-400 mb-2 font-medium">Text Chunks</p>
        <p class="text-3xl font-light text-zinc-900">{{ stats.totalChunks }}</p>
      </div>
      <div class="glass-panel p-6 rounded-3xl">
        <p class="text-sm text-zinc-400 mb-2 font-medium">Embeddings</p>
        <p class="text-3xl font-light text-zinc-900">{{ stats.totalEmbeddings }}</p>
      </div>
    </div>

    <!-- Upload Area -->
    <div class="group relative mb-4">
      <div class="absolute inset-0 bg-gradient-to-r from-zinc-100 to-zinc-50 rounded-[2rem] opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
      <label class="relative block w-full h-48 rounded-[2rem] border-2 border-dashed border-zinc-200 bg-white/50 hover:bg-white hover:border-zinc-300 transition-all cursor-pointer overflow-hidden group-hover:shadow-lg">
        <input
          type="file"
          multiple
          class="hidden"
          accept=".pdf,.txt,.md,.json,.csv"
          @change="handleFileUpload"
          :disabled="isIngesting"
        />
        
        <div class="absolute inset-0 flex flex-col items-center justify-center">
          <div class="w-16 h-16 rounded-full bg-zinc-50 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
            <Icon
              :icon="isIngesting ? 'hugeicons:loading-03' : 'hugeicons:cloud-upload'"
              class="w-8 h-8 text-zinc-400 group-hover:text-zinc-900 transition-colors"
              :class="{'animate-spin': isIngesting}"
            />
          </div>
          <p class="text-lg font-light text-zinc-900 mb-1">
            {{ isIngesting ? 'Processing files...' : 'Drop files here to upload' }}
          </p>
          <p class="text-sm text-zinc-400 font-light">
            Support for PDF, TXT, MD, JSON
          </p>
        </div>
      </label>
    </div>

    <!-- Documents List -->
    <div class="space-y-6">
      <!-- Controls -->
      <div class="flex flex-col md:flex-row gap-4 justify-between items-center">
        <h2 class="text-xl font-light text-zinc-900">Stored Documents</h2>
        
        <div class="flex items-center gap-3 w-full md:w-auto">
          <div class="relative flex-1 md:w-64 group">
            <Icon icon="hugeicons:search-01" class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400 group-hover:text-zinc-600 transition-colors" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search documents..."
              class="w-full pl-10 pr-4 py-2 bg-white border border-zinc-200 rounded-full text-zinc-900 placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-black/5 focus:border-zinc-300 transition-all shadow-sm"
            />
          </div>
          
          <div class="relative">
            <select
              v-model="selectedFilter"
              class="appearance-none pl-4 pr-10 py-2 bg-white border border-zinc-200 rounded-full text-zinc-900 focus:outline-none focus:ring-2 focus:ring-black/5 focus:border-zinc-300 transition-all shadow-sm cursor-pointer min-w-[140px]"
            >
              <option v-for="option in filterOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
            <Icon icon="hugeicons:arrow-down-01" class="w-4 h-4 absolute right-3 top-1/2 -translate-y-1/2 text-zinc-400 pointer-events-none" />
          </div>
        </div>
      </div>

      <!-- Table -->
      <div class="glass-panel rounded-3xl overflow-hidden bg-white/50">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-zinc-100 bg-white/50">
                <th class="px-6 py-4 text-left text-xs font-medium text-zinc-500 uppercase tracking-wider">Name</th>
                <th class="px-6 py-4 text-left text-xs font-medium text-zinc-500 uppercase tracking-wider">Status</th>
                <th class="px-6 py-4 text-left text-xs font-medium text-zinc-500 uppercase tracking-wider">Size</th>
                <th class="px-6 py-4 text-left text-xs font-medium text-zinc-500 uppercase tracking-wider">Chunks</th>
                <th class="px-6 py-4 text-right text-xs font-medium text-zinc-500 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-zinc-100">
              <tr v-if="filteredDocuments.length === 0">
                <td colspan="5" class="px-6 py-12 text-center text-zinc-500 font-light">
                  No documents found
                </td>
              </tr>
              <tr
                v-for="doc in filteredDocuments"
                :key="doc.id"
                class="group hover:bg-white/80 transition-colors"
                :class="{'bg-zinc-50/50': doc.status === 'processing'}"
              >
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-zinc-100 flex items-center justify-center text-zinc-400 group-hover:text-zinc-900 group-hover:bg-white border border-transparent group-hover:border-zinc-200 transition-all">
                      <Icon icon="hugeicons:file-02" class="w-5 h-5" />
                    </div>
                    <div>
                      <p class="text-sm font-medium text-zinc-900 group-hover:text-black transition-colors">{{ doc.name }}</p>
                      <p class="text-xs text-zinc-400">{{ doc.type }} • {{ doc.uploadedAt }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <div class="flex items-center gap-2">
                    <div
                      class="px-2.5 py-1 rounded-full text-xs font-medium flex items-center gap-1.5"
                      :class="getStatusBadge(doc.status).color"
                    >
                      <Icon :icon="getStatusBadge(doc.status).icon" class="w-3.5 h-3.5" :class="{'animate-spin': doc.status === 'processing'}" />
                      {{ getStatusBadge(doc.status).text }}
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 text-sm text-zinc-500 font-light">{{ doc.size }}</td>
                <td class="px-6 py-4 text-sm text-zinc-500 font-light">
                  {{ doc.status === 'processed' ? doc.chunks : '-' }}
                </td>
                <td class="px-6 py-4 text-right">
                  <div class="flex items-center justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      @click="handleView(doc)"
                      class="p-2 rounded-lg hover:bg-zinc-100 text-zinc-400 hover:text-zinc-900 transition-colors"
                      title="View content"
                    >
                      <Icon icon="hugeicons:view" class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleReprocess(doc)"
                      class="p-2 rounded-lg hover:bg-zinc-100 text-zinc-400 hover:text-zinc-900 transition-colors"
                      title="Reprocess"
                    >
                      <Icon icon="hugeicons:refresh" class="w-4 h-4" />
                    </button>
                    <button
                      @click="handleDelete(doc.id)"
                      class="p-2 rounded-lg hover:bg-red-50 text-zinc-400 hover:text-red-500 transition-colors"
                      title="Delete"
                    >
                      <Icon icon="hugeicons:delete-02" class="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}
</style>
