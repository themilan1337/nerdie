# Ingestion System Integration

This document describes the complete integration of the Nerdie Ingestion Service into the frontend application.

## Overview

The Nerdie Ingestion Service allows you to upload and process various document types (PDF, images, text files) for RAG (Retrieval-Augmented Generation) capabilities. The system automatically:
1. Extracts text from documents
2. Chunks the content into segments
3. Generates embeddings using Gemini Embeddings
4. Stores vectors in a PostgreSQL database with pgvector

## Backend URL

The ingestion service is hosted at: `https://ingest.nerdie.lol/`

## Project Structure

```
frontend/
├── app/
│   ├── composables/
│   │   └── useIngestion.ts          # Main API client composable
│   ├── types/
│   │   └── ingestion.ts              # TypeScript type definitions
│   └── pages/
│       └── dashboard/
│           └── rag/
│               └── index.vue         # RAG management UI
├── .env                              # Environment variables (not in git)
├── .env.example                      # Example environment config
├── ingestion.json                    # OpenAPI specification
└── nuxt.config.ts                    # Runtime config setup
```

## Configuration

### Environment Variables

Create a `.env` file in the `frontend/` directory:

```bash
NUXT_PUBLIC_INGESTION_API_URL=https://ingest.nerdie.lol
```

The URL is also set in `nuxt.config.ts` as a fallback, but you can override it via environment variables.

### Runtime Config

The ingestion API URL is available throughout the app via Nuxt's runtime config:

```typescript
const config = useRuntimeConfig()
const apiUrl = config.public.ingestionApiUrl
```

## API Endpoints

The ingestion service provides the following endpoints:

### 1. Text Ingestion
- **Endpoint**: `POST /ingest/text`
- **Auth**: Required (Bearer token)
- **Body**:
  ```json
  {
    "text": "Your text content here",
    "metadata": {
      "source": "optional metadata"
    }
  }
  ```

### 2. PDF Ingestion
- **Endpoint**: `POST /ingest/pdf`
- **Auth**: Required (Bearer token)
- **Content-Type**: `multipart/form-data`
- **Body**: File upload with `file` field

### 3. Image Ingestion
- **Endpoint**: `POST /ingest/image`
- **Auth**: Required (Bearer token)
- **Content-Type**: `multipart/form-data`
- **Body**: File upload with `file` field
- **Note**: Uses Gemini Vision for OCR

### 4. Legacy Upload
- **Endpoint**: `POST /ingest/upload`
- **Auth**: Required (Bearer token)
- **Content-Type**: `multipart/form-data`
- **Body**: File upload with `file` field
- **Note**: Auto-detects file type and routes to appropriate handler

### 5. Vector Insert
- **Endpoint**: `POST /vector/insert`
- **Auth**: Optional
- **Body**:
  ```json
  {
    "text": "Text chunk",
    "embedding": [0.1, 0.2, ...],  // 768-dimensional vector
    "metadata": {},
    "source": "manual_insert"
  }
  ```

### 6. Health Check
- **Endpoint**: `GET /health`
- **Auth**: Not required
- **Response**: Service health status

## Using the Composable

### Import

```typescript
import { useIngestion } from '~/composables/useIngestion'
```

### Basic Usage

```typescript
const {
  isLoading,
  error,
  uploadProgress,
  processFile,
  ingestText,
  ingestPDF,
  ingestImage,
  uploadFileLegacy,
  insertVector,
  healthCheck
} = useIngestion()

// Process a file automatically (detects type)
const file = event.target.files[0]
try {
  const result = await processFile(file)
  console.log('Processed:', result)
} catch (err) {
  console.error('Error:', err.message)
}

// Ingest text directly
await ingestText({
  text: 'Your text here',
  metadata: { source: 'user-input' }
})

// Upload PDF with progress tracking
await ingestPDF(pdfFile)
// Monitor uploadProgress.value for progress bar

// Health check
await healthCheck()
```

## TypeScript Types

All types are defined in `app/types/ingestion.ts`:

```typescript
interface TextInput {
  text: string
  metadata?: Record<string, any> | null
}

interface VectorInsertInput {
  text: string
  embedding: number[]
  metadata?: Record<string, any> | null
  source?: string | null
}

interface IngestionResponse {
  status?: string
  message?: string
  chunks?: number
  embeddings?: number
  documentId?: string
}

interface Document {
  id: string
  name: string
  type: 'PDF' | 'Image' | 'Text'
  size: string
  uploadedAt: string
  status: 'processed' | 'processing' | 'failed'
  chunks: number
  embeddings: number
  metadata?: Record<string, any>
}
```

## Authentication

All ingestion endpoints (except `/health`) require authentication. The `useIngestion` composable automatically includes the Bearer token from `useAuth()`:

```typescript
const { getAuthHeader } = useAuth()
const headers = getAuthHeader() // { Authorization: 'Bearer <token>' }
```

Make sure users are authenticated before attempting to upload documents.

## Error Handling

The composable provides built-in error handling:

```typescript
const { error, isLoading } = useIngestion()

try {
  await processFile(file)
} catch (err) {
  // error.value will contain the error message
  console.error(error.value)
}
```

Common error scenarios:
- **401 Unauthorized**: User not authenticated or token expired
- **422 Validation Error**: Invalid input format
- **Network errors**: Service unavailable or timeout

## Upload Progress

For file uploads, monitor the `uploadProgress` ref:

```vue
<template>
  <div v-if="isLoading && uploadProgress > 0">
    <div class="progress-bar" :style="{ width: `${uploadProgress}%` }"></div>
    <span>{{ uploadProgress }}%</span>
  </div>
</template>

<script setup>
const { uploadProgress } = useIngestion()
</script>
```

## RAG Management UI

The main UI for managing ingested documents is at `/dashboard/rag`. Features include:

- File upload with drag-and-drop support
- Real-time upload progress
- Document listing with search and filters
- Status tracking (processing, processed, failed)
- Chunk and embedding statistics
- Success/error notifications

## Vector Database Details

- **Database**: PostgreSQL with pgvector extension
- **Embeddings Model**: Gemini Embeddings
- **Vector Dimensions**: 768
- **Similarity Metric**: Cosine similarity
- **Storage**: Automatic chunking and indexing

## Best Practices

1. **File Size**: Keep files under 10MB for optimal performance
2. **Supported Formats**: PDF, TXT, DOC, DOCX, PNG, JPG, JPEG
3. **Error Handling**: Always wrap API calls in try-catch blocks
4. **Progress Tracking**: Use `uploadProgress` for user feedback on large files
5. **Health Checks**: Verify service availability on mount with `healthCheck()`
6. **Metadata**: Include relevant metadata for better document organization

## Testing

To test the integration:

1. Start the dev server: `pnpm dev`
2. Navigate to `/dashboard/rag`
3. Upload a test document (PDF, image, or text file)
4. Monitor the console for API calls and responses
5. Check the document list for processing status

## Troubleshooting

### "Failed to ingest" errors
- Check authentication token validity
- Verify the ingestion service is running at `https://ingest.nerdie.lol/`
- Check browser console for detailed error messages
- Run health check to verify service availability

### Upload progress stuck at 0%
- Check network connectivity
- Verify file size is within limits
- Check browser console for CORS or network errors

### 401 Unauthorized
- User needs to sign in again
- Token may have expired
- Check that `getAuthHeader()` is returning a valid token

## Future Enhancements

Potential improvements:
- Document preview/viewer
- Batch upload support
- Download processed documents
- Reprocess failed documents
- Advanced metadata editing
- Document versioning
- Search within document content
