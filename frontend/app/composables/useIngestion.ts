import { ref } from 'vue'
import type { TextInput, VectorInsertInput, IngestionResponse, Document } from '../types/ingestion'

export const useIngestion = () => {
  const config = useRuntimeConfig()
  const { getAuthHeader } = useAuth()

  const INGESTION_API_URL = config.public.ingestionApiUrl || 'https://ingest.nerdie.lol'

  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const uploadProgress = ref(0)

  const getHeaders = () => {
    const authHeader = getAuthHeader()
    return {
      ...authHeader,
    }
  }

  const ingestText = async (input: TextInput): Promise<IngestionResponse> => {
    try {
      isLoading.value = true
      error.value = null

      const response = await fetch(`${INGESTION_API_URL}/ingest/text`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders(),
        },
        body: JSON.stringify(input),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Failed to ingest text' }))
        throw new Error(errorData.message || errorData.detail?.[0]?.msg || 'Failed to ingest text')
      }

      const data = await response.json()
      return data
    } catch (err: any) {
      console.error('Ingest text error:', err)
      error.value = err.message || 'Failed to ingest text'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const ingestPDF = async (file: File): Promise<IngestionResponse> => {
    try {
      isLoading.value = true
      error.value = null
      uploadProgress.value = 0

      const formData = new FormData()
      formData.append('file', file)

      const xhr = new XMLHttpRequest()

      return new Promise((resolve, reject) => {
        xhr.upload.addEventListener('progress', (e) => {
          if (e.lengthComputable) {
            uploadProgress.value = Math.round((e.loaded / e.total) * 100)
          }
        })

        xhr.addEventListener('load', () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            try {
              const data = JSON.parse(xhr.responseText)
              uploadProgress.value = 100
              resolve(data)
            } catch (err) {
              reject(new Error('Invalid response from server'))
            }
          } else {
            try {
              const errorData = JSON.parse(xhr.responseText)
              reject(new Error(errorData.message || errorData.detail?.[0]?.msg || 'Failed to ingest PDF'))
            } catch {
              reject(new Error('Failed to ingest PDF'))
            }
          }
        })

        xhr.addEventListener('error', () => {
          reject(new Error('Network error during upload'))
        })

        xhr.open('POST', `${INGESTION_API_URL}/ingest/pdf`)

        const headers = getHeaders()
        Object.entries(headers).forEach(([key, value]) => {
          xhr.setRequestHeader(key, value as string)
        })

        xhr.send(formData)
      })
    } catch (err: any) {
      console.error('Ingest PDF error:', err)
      error.value = err.message || 'Failed to ingest PDF'
      throw err
    } finally {
      isLoading.value = false
      uploadProgress.value = 0
    }
  }

  const ingestImage = async (file: File): Promise<IngestionResponse> => {
    try {
      isLoading.value = true
      error.value = null
      uploadProgress.value = 0

      const formData = new FormData()
      formData.append('file', file)

      const xhr = new XMLHttpRequest()

      return new Promise((resolve, reject) => {
        xhr.upload.addEventListener('progress', (e) => {
          if (e.lengthComputable) {
            uploadProgress.value = Math.round((e.loaded / e.total) * 100)
          }
        })

        xhr.addEventListener('load', () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            try {
              const data = JSON.parse(xhr.responseText)
              uploadProgress.value = 100
              resolve(data)
            } catch (err) {
              reject(new Error('Invalid response from server'))
            }
          } else {
            try {
              const errorData = JSON.parse(xhr.responseText)
              reject(new Error(errorData.message || errorData.detail?.[0]?.msg || 'Failed to ingest image'))
            } catch {
              reject(new Error('Failed to ingest image'))
            }
          }
        })

        xhr.addEventListener('error', () => {
          reject(new Error('Network error during upload'))
        })

        xhr.open('POST', `${INGESTION_API_URL}/ingest/image`)

        const headers = getHeaders()
        Object.entries(headers).forEach(([key, value]) => {
          xhr.setRequestHeader(key, value as string)
        })

        xhr.send(formData)
      })
    } catch (err: any) {
      console.error('Ingest image error:', err)
      error.value = err.message || 'Failed to ingest image'
      throw err
    } finally {
      isLoading.value = false
      uploadProgress.value = 0
    }
  }

  const uploadFileLegacy = async (file: File): Promise<IngestionResponse> => {
    try {
      isLoading.value = true
      error.value = null
      uploadProgress.value = 0

      const formData = new FormData()
      formData.append('file', file)

      const xhr = new XMLHttpRequest()

      return new Promise((resolve, reject) => {
        xhr.upload.addEventListener('progress', (e) => {
          if (e.lengthComputable) {
            uploadProgress.value = Math.round((e.loaded / e.total) * 100)
          }
        })

        xhr.addEventListener('load', () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            try {
              const data = JSON.parse(xhr.responseText)
              uploadProgress.value = 100
              resolve(data)
            } catch (err) {
              reject(new Error('Invalid response from server'))
            }
          } else {
            try {
              const errorData = JSON.parse(xhr.responseText)
              reject(new Error(errorData.message || errorData.detail?.[0]?.msg || 'Failed to upload file'))
            } catch {
              reject(new Error('Failed to upload file'))
            }
          }
        })

        xhr.addEventListener('error', () => {
          reject(new Error('Network error during upload'))
        })

        xhr.open('POST', `${INGESTION_API_URL}/ingest/upload`)

        const headers = getHeaders()
        Object.entries(headers).forEach(([key, value]) => {
          xhr.setRequestHeader(key, value as string)
        })

        xhr.send(formData)
      })
    } catch (err: any) {
      console.error('Upload file error:', err)
      error.value = err.message || 'Failed to upload file'
      throw err
    } finally {
      isLoading.value = false
      uploadProgress.value = 0
    }
  }

  const insertVector = async (input: VectorInsertInput): Promise<IngestionResponse> => {
    try {
      isLoading.value = true
      error.value = null

      const response = await fetch(`${INGESTION_API_URL}/vector/insert`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getHeaders(),
        },
        body: JSON.stringify(input),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ message: 'Failed to insert vector' }))
        throw new Error(errorData.message || errorData.detail?.[0]?.msg || 'Failed to insert vector')
      }

      const data = await response.json()
      return data
    } catch (err: any) {
      console.error('Insert vector error:', err)
      error.value = err.message || 'Failed to insert vector'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const healthCheck = async (): Promise<any> => {
    try {
      const response = await fetch(`${INGESTION_API_URL}/health`, {
        method: 'GET',
      })

      if (!response.ok) {
        throw new Error('Health check failed')
      }

      const data = await response.json()
      return data
    } catch (err: any) {
      console.error('Health check error:', err)
      throw err
    }
  }

  const processFile = async (file: File): Promise<IngestionResponse> => {
    const fileType = file.type.toLowerCase()

    if (fileType.includes('pdf')) {
      return await ingestPDF(file)
    } else if (fileType.includes('image') || fileType.includes('png') || fileType.includes('jpg') || fileType.includes('jpeg')) {
      return await ingestImage(file)
    } else if (fileType.includes('text')) {
      const text = await file.text()
      return await ingestText({ text, metadata: { filename: file.name } })
    } else {
      return await uploadFileLegacy(file)
    }
  }

  return {
    isLoading,
    error,
    uploadProgress,
    ingestText,
    ingestPDF,
    ingestImage,
    uploadFileLegacy,
    insertVector,
    healthCheck,
    processFile,
  }
}
