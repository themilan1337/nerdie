<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Upload, FileText, Image as ImageIcon, File, Trash2, Download, Search, Filter, MoreVertical, Eye, CheckCircle, Clock, AlertCircle, X } from 'lucide-vue-next'
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

    const fileType = file.type.includes('pdf')
      ? 'PDF'
      : file.type.includes('image')
      ? 'Image'
      : 'Text'

    const tempDoc: Document = {
      id: `temp-${Date.now()}-${i}`,
      name: file.name,
      type: fileType,
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
      if (docIndex !== -1) {
        documents.value[docIndex] = {
          ...documents.value[docIndex],
          id: response.documentId || tempDoc.id,
          status: 'processed',
          chunks: response.chunks || 0,
          embeddings: response.embeddings || 0,
        }
      }

      showNotification(`Successfully processed ${file.name}`, 'success')
    } catch (err: any) {
      console.error('Upload error:', err)

      const docIndex = documents.value.findIndex(d => d.id === tempDoc.id)
      if (docIndex !== -1) {
        documents.value[docIndex].status = 'failed'
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
      return { color: 'bg-green-100 text-green-700', icon: CheckCircle, text: 'Processed' }
    case 'processing':
      return { color: 'bg-blue-100 text-blue-700', icon: Clock, text: 'Processing' }
    case 'failed':
      return { color: 'bg-red-100 text-red-700', icon: AlertCircle, text: 'Failed' }
    default:
      return { color: 'bg-gray-100 text-gray-700', icon: Clock, text: 'Unknown' }
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
  <div class="p-6 lg:p-8">
    <!-- Success Notification -->
    <Transition name="slide-down">
      <div
        v-if="showSuccessNotification"
        class="fixed top-4 right-4 z-50 bg-green-500 text-white px-6 py-4 rounded-2xl shadow-lg flex items-center gap-3 max-w-md"
      >
        <CheckCircle class="w-5 h-5 flex-shrink-0" />
        <p class="flex-1 text-sm font-medium">{{ successMessage }}</p>
        <button @click="showSuccessNotification = false" class="flex-shrink-0">
          <X class="w-5 h-5" />
        </button>
      </div>
    </Transition>

    <!-- Error Notification -->
    <Transition name="slide-down">
      <div
        v-if="showErrorNotification"
        class="fixed top-4 right-4 z-50 bg-red-500 text-white px-6 py-4 rounded-2xl shadow-lg flex items-center gap-3 max-w-md"
      >
        <AlertCircle class="w-5 h-5 flex-shrink-0" />
        <p class="flex-1 text-sm font-medium">{{ errorMessage }}</p>
        <button @click="showErrorNotification = false" class="flex-shrink-0">
          <X class="w-5 h-5" />
        </button>
      </div>
    </Transition>

    <!-- Page Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 ins">RAG Management</h1>
      <p class="text-gray-500 mt-1">Manage your knowledge base documents and embeddings</p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
      <div class="bg-white rounded-2xl border border-gray-200 p-5">
        <p class="text-sm text-gray-600 mb-1">Total Documents</p>
        <p class="text-2xl font-bold text-gray-900 ins">{{ stats.total }}</p>
      </div>
      <div class="bg-white rounded-2xl border border-gray-200 p-5">
        <p class="text-sm text-gray-600 mb-1">Processed</p>
        <p class="text-2xl font-bold text-green-600 ins">{{ stats.processed }}</p>
      </div>
      <div class="bg-white rounded-2xl border border-gray-200 p-5">
        <p class="text-sm text-gray-600 mb-1">Processing</p>
        <p class="text-2xl font-bold text-blue-600 ins">{{ stats.processing }}</p>
      </div>
      <div class="bg-white rounded-2xl border border-gray-200 p-5">
        <p class="text-sm text-gray-600 mb-1">Total Chunks</p>
        <p class="text-2xl font-bold text-purple-600 ins">{{ stats.totalChunks }}</p>
      </div>
      <div class="bg-white rounded-2xl border border-gray-200 p-5">
        <p class="text-sm text-gray-600 mb-1">Embeddings</p>
        <p class="text-2xl font-bold text-orange-600 ins">{{ stats.totalEmbeddings }}</p>
      </div>
    </div>

    <!-- Upload Area -->
    <div class="bg-white rounded-2xl border-2 border-dashed border-gray-300 p-12 mb-8 hover:border-gray-400 transition-colors">
      <div class="text-center">
        <div class="w-16 h-16 bg-gradient-to-br from-orange-400 to-pink-500 rounded-2xl mx-auto mb-4 flex items-center justify-center">
          <Upload class="w-8 h-8 text-white" />
        </div>
        <h3 class="text-xl font-bold text-gray-900 ins mb-2">Upload Documents</h3>
        <p class="text-gray-500 mb-6">Drag and drop files here, or click to browse</p>

        <label class="inline-block cursor-pointer">
          <input
            type="file"
            multiple
            accept=".pdf,.txt,.doc,.docx,.png,.jpg,.jpeg"
            @change="handleFileUpload"
            class="hidden"
            :disabled="isIngesting"
          />
          <span
            :class="[
              'px-6 py-3 rounded-full font-medium ins inline-flex items-center gap-2 transition-colors',
              isIngesting
                ? 'bg-gray-400 text-white cursor-not-allowed'
                : 'bg-black text-white hover:bg-gray-800 cursor-pointer'
            ]"
          >
            <Upload class="w-4 h-4" />
            {{ isIngesting ? 'Processing...' : 'Choose Files' }}
          </span>
        </label>

        <p class="text-sm text-gray-400 mt-4">Supported: PDF, TXT, DOC, DOCX, PNG, JPG (Max 10MB)</p>

        <!-- Upload Progress -->
        <div v-if="isIngesting && uploadProgress > 0" class="mt-6 max-w-md mx-auto">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-gray-700">Uploading...</span>
            <span class="text-sm font-medium text-gray-700">{{ uploadProgress }}%</span>
          </div>
          <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              class="h-full bg-gradient-to-r from-orange-400 to-pink-500 transition-all duration-300"
              :style="{ width: `${uploadProgress}%` }"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="bg-white rounded-2xl border border-gray-200 p-6 mb-6">
      <div class="flex flex-col md:flex-row gap-4">
        <!-- Search -->
        <div class="flex-1 relative">
          <Search class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search documents..."
            class="w-full pl-10 pr-4 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all"
          />
        </div>

        <!-- Filter Dropdown -->
        <div class="relative">
          <Filter class="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <select
            v-model="selectedFilter"
            class="pl-10 pr-8 py-2.5 bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent transition-all appearance-none cursor-pointer min-w-[200px]"
          >
            <option v-for="option in filterOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Documents List -->
    <div class="bg-white rounded-2xl border border-gray-200 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider ins">Document</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider ins">Type</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider ins">Size</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider ins">Status</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider ins">Chunks</th>
              <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider ins">Uploaded</th>
              <th class="px-6 py-4 text-right text-xs font-semibold text-gray-600 uppercase tracking-wider ins">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr
              v-for="doc in filteredDocuments"
              :key="doc.id"
              class="hover:bg-gray-50 transition-colors"
            >
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="p-2 bg-gray-100 rounded-lg">
                    <FileText v-if="doc.type === 'PDF'" class="w-5 h-5 text-red-500" />
                    <ImageIcon v-else-if="doc.type === 'Image'" class="w-5 h-5 text-blue-500" />
                    <File v-else class="w-5 h-5 text-gray-500" />
                  </div>
                  <div>
                    <p class="font-medium text-gray-900 text-sm">{{ doc.name }}</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="text-sm text-gray-600">{{ doc.type }}</span>
              </td>
              <td class="px-6 py-4">
                <span class="text-sm text-gray-600">{{ doc.size }}</span>
              </td>
              <td class="px-6 py-4">
                <span
                  :class="[
                    'inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-xs font-medium',
                    getStatusBadge(doc.status).color
                  ]"
                >
                  <component :is="getStatusBadge(doc.status).icon" class="w-3 h-3" />
                  {{ getStatusBadge(doc.status).text }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="text-sm">
                  <span class="text-gray-900 font-medium">{{ doc.chunks }}</span>
                  <span class="text-gray-400"> / </span>
                  <span class="text-gray-600">{{ doc.embeddings }}</span>
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="text-sm text-gray-600">{{ doc.uploadedAt }}</span>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center justify-end gap-2">
                  <button
                    @click="handleView(doc)"
                    class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    title="View"
                  >
                    <Eye class="w-4 h-4 text-gray-600" />
                  </button>
                  <button
                    @click="handleDownload(doc)"
                    class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    title="Download"
                  >
                    <Download class="w-4 h-4 text-gray-600" />
                  </button>
                  <button
                    v-if="doc.status === 'failed'"
                    @click="handleReprocess(doc)"
                    class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    title="Reprocess"
                  >
                    <CheckCircle class="w-4 h-4 text-blue-600" />
                  </button>
                  <button
                    @click="handleDelete(doc.id)"
                    class="p-2 rounded-lg hover:bg-red-50 transition-colors"
                    title="Delete"
                  >
                    <Trash2 class="w-4 h-4 text-red-600" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Empty State -->
        <div v-if="filteredDocuments.length === 0" class="text-center py-12">
          <div class="w-16 h-16 bg-gray-100 rounded-2xl mx-auto mb-4 flex items-center justify-center">
            <FileText class="w-8 h-8 text-gray-400" />
          </div>
          <h3 class="text-lg font-bold text-gray-900 ins mb-2">No documents found</h3>
          <p class="text-gray-500">{{ documents.length === 0 ? 'Upload your first document to get started' : 'Try adjusting your search or filters' }}</p>
        </div>
      </div>
    </div>

    <!-- Processing Info -->
    <div class="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white">
        <h3 class="text-lg font-bold ins mb-2">RAG Pipeline</h3>
        <p class="text-sm text-blue-100 mb-4">How your documents are processed</p>
        <div class="space-y-3">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center flex-shrink-0">
              <span class="text-sm font-bold">1</span>
            </div>
            <p class="text-sm">Upload & Extract Text</p>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center flex-shrink-0">
              <span class="text-sm font-bold">2</span>
            </div>
            <p class="text-sm">Chunk into Segments</p>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center flex-shrink-0">
              <span class="text-sm font-bold">3</span>
            </div>
            <p class="text-sm">Generate Embeddings</p>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center flex-shrink-0">
              <span class="text-sm font-bold">4</span>
            </div>
            <p class="text-sm">Store in Vector DB</p>
          </div>
        </div>
      </div>

      <div class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl p-6 text-white">
        <h3 class="text-lg font-bold ins mb-2">Vector Database</h3>
        <p class="text-sm text-purple-100 mb-4">Powered by pgvector + PostgreSQL</p>
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-sm">Embeddings Model</span>
            <span class="text-sm font-medium">Gemini Embeddings</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm">Vector Dimensions</span>
            <span class="text-sm font-medium">768</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm">Similarity Metric</span>
            <span class="text-sm font-medium">Cosine</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-sm">Active Documents</span>
            <span class="text-sm font-medium">{{ stats.total }}</span>
          </div>
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

.slide-down-enter-from {
  transform: translateY(-100%);
  opacity: 0;
}

.slide-down-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}
</style>
