export interface TextInput {
  text: string
  metadata?: Record<string, any> | null
}

export interface VectorInsertInput {
  text: string
  embedding: number[]
  metadata?: Record<string, any> | null
  source?: string | null
}

export interface ValidationError {
  loc: (string | number)[]
  msg: string
  type: string
}

export interface HTTPValidationError {
  detail?: ValidationError[]
}

export interface IngestionResponse {
  status?: string
  message?: string
  chunks?: number
  embeddings?: number
  documentId?: string
}

export interface Document {
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

export type IngestionType = 'text' | 'pdf' | 'image' | 'upload'
