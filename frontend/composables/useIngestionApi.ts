export const useIngestionApi = () => {
    const config = useRuntimeConfig()
    const baseUrl = config.public.ingestionServiceUrl

    const uploadDocument = async (file: File) => {
        const formData = new FormData()
        formData.append('file', file)

        let endpoint = '/ingest/upload' // Default or legacy
        if (file.type === 'application/pdf') {
            endpoint = '/ingest/pdf'
        } else if (file.type.startsWith('image/')) {
            endpoint = '/ingest/image'
        } else if (file.type === 'text/plain') {
            // Text endpoint might expect JSON, check API specs.
            // The ingestion.json shows /ingest/text expects JSON with text string.
            // If we have a file, we might need to read it or use a generic upload if available.
            // The swagger shows /ingest/upload as legacy but maybe useful.
            // Let's stick to /ingest/pdf and /ingest/image for now as they are multipart.
            // For text file, we might need to read content and send to /ingest/text or use /ingest/upload if it handles it.
            // Let's use /ingest/upload for others for now if it works, or just restrict to PDF/Image as typically RAG is PDF.
            endpoint = '/ingest/upload'
        }

        try {
            // @ts-ignore
            const { getAuthHeader } = useAuth()
            const headers = (await getAuthHeader()) || undefined

            // @ts-ignore
            const data = await $fetch(`${baseUrl}${endpoint}`, {
                method: 'POST',
                headers,
                body: formData
            })
            return data
        } catch (error) {
            console.error('Error uploading document:', error)
            throw error
        }
    }

    const fetchDocuments = async () => {
        try {
            // Note: The Swagger shows /ingest/documents returns a list.
            // @ts-ignore
            const { getAuthHeader } = useAuth()
            const headers = (await getAuthHeader()) || undefined

            // @ts-ignore
            const data = await $fetch(`${baseUrl}/ingest/documents`, {
                headers
            })
            return (data as any[]) || []
        } catch (error) {
            console.error('Error fetching documents:', error)
            return []
        }
    }

    return {
        uploadDocument,
        fetchDocuments
    }
}
