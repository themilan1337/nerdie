<script setup lang="ts">
import { ref, computed } from 'vue'
import { Upload, FileText, Image as ImageIcon, File, Trash2, Download, Search, Filter, MoreVertical, Eye, CheckCircle, Clock, AlertCircle } from 'lucide-vue-next'

definePageMeta({
  layout: 'dashboard'
})

const searchQuery = ref('')
const selectedFilter = ref('all')
const isUploading = ref(false)
const uploadProgress = ref(0)

const filterOptions = [
  { value: 'all', label: 'All Documents' },
  { value: 'pdf', label: 'PDFs' },
  { value: 'image', label: 'Images' },
  { value: 'text', label: 'Text Files' },
  { value: 'processing', label: 'Processing' },
]

const documents = ref([
  {
    id: 1,
    name: 'Machine_Learning_Guide.pdf',
    type: 'PDF',
    size: '2.4 MB',
    uploadedAt: '2024-01-15',
    status: 'processed',
    chunks: 45,
    embeddings: 45,
    icon: FileText,
    color: 'text-red-500'
  },
  {
    id: 2,
    name: 'Neural_Networks_Diagram.png',
    type: 'Image',
    size: '1.8 MB',
    uploadedAt: '2024-01-14',
    status: 'processed',
    chunks: 1,
    embeddings: 1,
    icon: ImageIcon,
    color: 'text-blue-500'
  },
  {
    id: 3,
    name: 'Research_Paper_2024.pdf',
    type: 'PDF',
    size: '3.2 MB',
    uploadedAt: '2024-01-13',
    status: 'processing',
    chunks: 67,
    embeddings: 42,
    icon: FileText,
    color: 'text-red-500'
  },
  {
    id: 4,
    name: 'Project_Notes.txt',
    type: 'Text',
    size: '45 KB',
    uploadedAt: '2024-01-12',
    status: 'processed',
    chunks: 12,
    embeddings: 12,
    icon: File,
    color: 'text-gray-500'
  },
  {
    id: 5,
    name: 'AI_Ethics_Guidelines.pdf',
    type: 'PDF',
    size: '1.2 MB',
    uploadedAt: '2024-01-11',
    status: 'failed',
    chunks: 0,
    embeddings: 0,
    icon: FileText,
    color: 'text-red-500'
  },
  {
    id: 6,
    name: 'Data_Visualization.png',
    type: 'Image',
    size: '890 KB',
    uploadedAt: '2024-01-10',
    status: 'processed',
    chunks: 1,
    embeddings: 1,
    icon: ImageIcon,
    color: 'text-blue-500'
  },
])

const stats = computed(() => ({
  total: documents.value.length,
  processed: documents.value.filter(d => d.status === 'processed').length,
  processing: documents.value.filter(d => d.status === 'processing').length,
  totalChunks: documents.value.reduce((sum, d) => sum + d.chunks, 0),
  totalEmbeddings: documents.value.reduce((sum, d) => sum + d.embeddings, 0),
}))

const filteredDocuments = computed(() => {
  let filtered = documents.value

  // Apply search filter
  if (searchQuery.value) {
    filtered = filtered.filter(doc =>
      doc.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  // Apply type filter
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

const handleFileUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement
  const files = input.files

  if (!files || files.length === 0) return

  isUploading.value = true
  uploadProgress.value = 0

  // Simulate upload progress
  const interval = setInterval(() => {
    uploadProgress.value += 10
    if (uploadProgress.value >= 100) {
      clearInterval(interval)
      setTimeout(() => {
        isUploading.value = false
        uploadProgress.value = 0

        // Add new document to the list
        for (let i = 0; i < files.length; i++) {
          const file = files[i]
          const fileType = file.type.includes('pdf') ? 'PDF' : file.type.includes('image') ? 'Image' : 'Text'
          documents.value.unshift({
            id: documents.value.length + 1,
            name: file.name,
            type: fileType,
            size: `${(file.size / 1024 / 1024).toFixed(2)} MB`,
            uploadedAt: new Date().toISOString().split('T')[0],
            status: 'processing',
            chunks: 0,
            embeddings: 0,
            icon: fileType === 'PDF' ? FileText : fileType === 'Image' ? ImageIcon : File,
            color: fileType === 'PDF' ? 'text-red-500' : fileType === 'Image' ? 'text-blue-500' : 'text-gray-500'
          })
        }
      }, 500)
    }
  }, 200)
}

const handleDelete = (id: number) => {
  if (confirm('Are you sure you want to delete this document?')) {
    documents.value = documents.value.filter(doc => doc.id !== id)
  }
}

const handleDownload = (doc: any) => {
  console.log('Downloading:', doc.name)
}

const handleView = (doc: any) => {
  console.log('Viewing:', doc.name)
}

const handleReprocess = (doc: any) => {
  console.log('Reprocessing:', doc.name)
  const document = documents.value.find(d => d.id === doc.id)
  if (document) {
    document.status = 'processing'
  }
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
</script>

<template>
  <div class="p-6 lg:p-8">
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
          />
          <span class="px-6 py-3 bg-black text-white rounded-full font-medium ins hover:bg-gray-800 transition-colors inline-flex items-center gap-2">
            <Upload class="w-4 h-4" />
            Choose Files
          </span>
        </label>

        <p class="text-sm text-gray-400 mt-4">Supported: PDF, TXT, DOC, DOCX, PNG, JPG (Max 10MB)</p>

        <!-- Upload Progress -->
        <div v-if="isUploading" class="mt-6 max-w-md mx-auto">
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
                    <component :is="doc.icon" :class="['w-5 h-5', doc.color]" />
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
          <p class="text-gray-500">Try adjusting your search or filters</p>
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
            <span class="text-sm">Storage Used</span>
            <span class="text-sm font-medium">234 MB</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
