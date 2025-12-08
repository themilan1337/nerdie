# Nerdie Backend API Documentation

Complete API reference for frontend developers to integrate with the Nerdie Knowledge Brain backend.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URLs](#base-urls)
4. [Ingestion Service API](#ingestion-service-api)
   - [POST /ingest/text](#post-ingesttext)
   - [POST /ingest/pdf](#post-ingestpdf)
   - [POST /ingest/image](#post-ingestimage)
   - [GET /health](#get-health-ingestion)
5. [RAG Service API](#rag-service-api)
   - [POST /rag/query](#post-ragquery)
   - [POST /vector/insert](#post-vectorinsert)
   - [GET /graph/query](#get-graphquery)
   - [GET /health](#get-health-rag)
6. [Auth Service API](#auth-service-api)
   - [POST /auth/verify](#post-authverify)
   - [GET /auth/health](#get-authhealth)
7. [Error Handling](#error-handling)
8. [Data Models](#data-models)

---

## Overview

The Nerdie backend consists of three microservices:

| Service       | Purpose                              | Port |
| ------------- | ------------------------------------ | ---- |
| **Auth**      | Firebase authentication verification | 8000 |
| **RAG**       | Vector search and LLM-powered Q&A    | 8001 |
| **Ingestion** | Document processing, OCR, embeddings | 8002 |

### Architecture Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│  Ingestion  │────▶│    RAG      │
│   (Nuxt.js) │     │   Service   │     │   Service   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                   │
       │                   ▼                   ▼
       │            ┌─────────────┐     ┌─────────────┐
       └───────────▶│  Firebase   │     │  PostgreSQL │
                    │  (Auth/FS)  │     │  (pgvector) │
                    └─────────────┘     └─────────────┘
```

---

## Authentication

All protected endpoints require a **Firebase ID Token** in the Authorization header.

### How to Get a Token

1. User signs in with Firebase Auth on frontend
2. Call `firebase.auth().currentUser.getIdToken()` to get the token
3. Include token in all API requests

### Header Format

```
Authorization: Bearer <firebase_id_token>
```

### Example

```javascript
const token = await firebase.auth().currentUser.getIdToken();

fetch("http://localhost:8002/ingest/text", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  },
  body: JSON.stringify({ text: "Your content here" }),
});
```

---

## Base URLs

| Environment    | Auth                    | RAG                     | Ingestion               |
| -------------- | ----------------------- | ----------------------- | ----------------------- |
| Development    | `http://localhost:8000` | `http://localhost:8001` | `http://localhost:8002` |
| Docker Network | `http://auth:8000`      | `http://rag:8001`       | `http://ingestion:8002` |

---

# Ingestion Service API

The Ingestion Service handles document upload, text extraction, chunking, embedding generation, and knowledge graph extraction.

---

## POST /ingest/text

Ingest raw text into the knowledge base. The text is chunked, embedded, and stored with knowledge graph extraction.

### Authentication

🔒 **Required** - Bearer Token

### Request

```http
POST /ingest/text HTTP/1.1
Host: localhost:8002
Authorization: Bearer <firebase_token>
Content-Type: application/json
```

#### Request Body

| Field      | Type   | Required | Description                           |
| ---------- | ------ | -------- | ------------------------------------- |
| `text`     | string | ✅ Yes   | The text content to ingest            |
| `metadata` | object | ❌ No    | Optional metadata to attach to chunks |

#### Example Request

```json
{
  "text": "Machine learning is a subset of artificial intelligence that enables systems to learn from data. Neural networks are computing systems inspired by biological neural networks. Deep learning uses multiple layers of neural networks to progressively extract higher-level features from raw input.",
  "metadata": {
    "source": "lecture_notes",
    "topic": "AI Fundamentals",
    "date": "2024-01-15"
  }
}
```

### Response

#### Success Response (200 OK)

```json
{
  "status": "success",
  "user_id": "firebase_user_123",
  "chunks_processed": 3,
  "entities_extracted": 5,
  "relations_extracted": 4,
  "message": "Text successfully ingested and indexed"
}
```

#### Response Fields

| Field                 | Type    | Description                                  |
| --------------------- | ------- | -------------------------------------------- |
| `status`              | string  | "success" or "error"                         |
| `user_id`             | string  | Firebase user ID extracted from token        |
| `chunks_processed`    | integer | Number of text chunks created                |
| `entities_extracted`  | integer | Number of entities found for knowledge graph |
| `relations_extracted` | integer | Number of relationships between entities     |
| `message`             | string  | Human-readable status message                |

### Error Responses

| Status | Description                             |
| ------ | --------------------------------------- |
| 401    | Missing or invalid authentication token |
| 500    | Internal server error during processing |

---

## POST /ingest/pdf

Upload and process a PDF file. Extracts text, chunks it, generates embeddings, and builds knowledge graph.

### Authentication

🔒 **Required** - Bearer Token

### Request

```http
POST /ingest/pdf HTTP/1.1
Host: localhost:8002
Authorization: Bearer <firebase_token>
Content-Type: multipart/form-data
```

#### Form Data

| Field  | Type | Required | Description                |
| ------ | ---- | -------- | -------------------------- |
| `file` | file | ✅ Yes   | PDF file (application/pdf) |

#### Example (JavaScript)

```javascript
const formData = new FormData();
formData.append("file", pdfFile); // File object from <input type="file">

const response = await fetch("http://localhost:8002/ingest/pdf", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${token}`,
  },
  body: formData,
});
```

#### Example (cURL)

```bash
curl -X POST http://localhost:8002/ingest/pdf \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf"
```

### Response

#### Success Response (200 OK)

```json
{
  "status": "success",
  "user_id": "firebase_user_123",
  "file_url": "https://storage.googleapis.com/nerdie-85d0a.appspot.com/pdfs/user123/abc123.pdf",
  "chunks_processed": 15,
  "entities_extracted": 23,
  "relations_extracted": 18,
  "message": "PDF processed and indexed"
}
```

#### Response Fields

| Field                 | Type    | Description                              |
| --------------------- | ------- | ---------------------------------------- |
| `file_url`            | string  | Firebase Storage URL where PDF is stored |
| `chunks_processed`    | integer | Number of text chunks extracted          |
| `entities_extracted`  | integer | Entities found for knowledge graph       |
| `relations_extracted` | integer | Relationships between entities           |

### Error Responses

| Status | Description                                     |
| ------ | ----------------------------------------------- |
| 400    | File is not a PDF or no text could be extracted |
| 401    | Missing or invalid authentication token         |
| 500    | Internal server error                           |

---

## POST /ingest/image

Upload and process an image using Gemini Vision OCR. Extracts text from the image, chunks it, and creates embeddings.

### Authentication

🔒 **Required** - Bearer Token

### Request

```http
POST /ingest/image HTTP/1.1
Host: localhost:8002
Authorization: Bearer <firebase_token>
Content-Type: multipart/form-data
```

#### Form Data

| Field  | Type | Required | Description                     |
| ------ | ---- | -------- | ------------------------------- |
| `file` | file | ✅ Yes   | Image file (JPEG, PNG, or WebP) |

#### Supported Formats

- `image/jpeg`
- `image/png`
- `image/webp`

#### Example (JavaScript)

```javascript
const formData = new FormData();
formData.append("file", imageFile);

const response = await fetch("http://localhost:8002/ingest/image", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${token}`,
  },
  body: formData,
});
```

### Response

#### Success Response (200 OK)

```json
{
  "status": "success",
  "user_id": "firebase_user_123",
  "file_url": "https://storage.googleapis.com/nerdie-85d0a.appspot.com/images/user123/def456.png",
  "chunks_processed": 2,
  "entities_extracted": 8,
  "relations_extracted": 5,
  "message": "Image processed with OCR and indexed"
}
```

#### No Text Extracted Response (200 OK)

If the image contains no text:

```json
{
  "status": "success",
  "user_id": "firebase_user_123",
  "file_url": "https://storage.googleapis.com/.../image.png",
  "chunks_processed": 0,
  "message": "Image uploaded but no text could be extracted"
}
```

### Special Behavior

- Image chunks include `image_url` in metadata for frontend display
- Even if no text is extracted, the image is stored in Firebase Storage
- OCR uses Gemini 1.5 Flash Vision for text extraction

---

## GET /health (Ingestion)

Health check endpoint for the ingestion service.

### Authentication

🔓 **Not Required**

### Request

```http
GET /health HTTP/1.1
Host: localhost:8002
```

### Response

```json
{
  "status": "healthy"
}
```

---

# RAG Service API

The RAG (Retrieval-Augmented Generation) Service handles semantic search and LLM-powered question answering.

---

## POST /rag/query

Ask a question against your knowledge base. Returns an AI-generated answer based on your ingested documents.

### Authentication

🔓 **Not Required** (user_id passed in body)

### Request

```http
POST /rag/query HTTP/1.1
Host: localhost:8001
Content-Type: application/json
```

#### Request Body

| Field     | Type   | Required | Description                          |
| --------- | ------ | -------- | ------------------------------------ |
| `user_id` | string | ✅ Yes   | Firebase user ID to scope the search |
| `query`   | string | ✅ Yes   | Natural language question            |

#### Example Request

```json
{
  "user_id": "firebase_user_123",
  "query": "What is machine learning?"
}
```

### Response

#### Success Response (200 OK)

```json
{
  "answer": "Machine learning is a subset of artificial intelligence that enables systems to learn from data without being explicitly programmed. Based on your documents, it involves using algorithms to identify patterns in data and make predictions or decisions.",
  "chunks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "text": "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
      "metadata": {
        "source": "lecture_notes",
        "type": "text"
      },
      "score": 0.15,
      "type": "text",
      "image_url": null
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "text": "Neural networks are computing systems inspired by biological neural networks.",
      "metadata": {
        "source": "lecture_notes",
        "type": "text"
      },
      "score": 0.23,
      "type": "text",
      "image_url": null
    }
  ],
  "context_used": "Machine learning is a subset of artificial intelligence...\n\nNeural networks are computing systems..."
}
```

#### Response Fields

| Field                | Type   | Description                               |
| -------------------- | ------ | ----------------------------------------- |
| `answer`             | string | LLM-generated answer based on context     |
| `chunks`             | array  | Retrieved document chunks used as context |
| `chunks[].id`        | string | Unique chunk identifier                   |
| `chunks[].text`      | string | Text content of the chunk                 |
| `chunks[].metadata`  | object | Source information and custom metadata    |
| `chunks[].score`     | float  | Similarity score (lower is more similar)  |
| `chunks[].type`      | string | "text" or "image"                         |
| `chunks[].image_url` | string | URL if chunk came from image OCR          |
| `context_used`       | string | Full context string sent to LLM           |

### Anti-Hallucination Behavior

If the answer cannot be found in the user's documents:

```json
{
  "answer": "Information not found in the knowledge base.",
  "chunks": [],
  "context_used": ""
}
```

### Frontend Display Tips

1. **Show source chunks** - Display the `chunks` array to show users where the answer came from
2. **Image support** - If `chunk.type === "image"` and `chunk.image_url` exists, show a thumbnail
3. **Confidence indicator** - Lower `score` = higher relevance (cosine distance)

---

## POST /vector/insert

Insert a pre-processed chunk with embedding into the vector store. This is primarily used by the ingestion service internally.

### Authentication

🔓 **Not Required** (internal service endpoint)

### Request

```http
POST /vector/insert HTTP/1.1
Host: localhost:8001
Content-Type: application/json
```

#### Request Body

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "firebase_user_123",
  "text": "Machine learning is a subset of AI.",
  "embedding": [0.123, -0.456, 0.789, ...],
  "metadata": {
    "source": "document.pdf",
    "type": "pdf",
    "page": 1
  }
}
```

#### Fields

| Field       | Type          | Required | Description                     |
| ----------- | ------------- | -------- | ------------------------------- |
| `id`        | string (UUID) | ✅ Yes   | Unique identifier for the chunk |
| `user_id`   | string        | ✅ Yes   | Owner of this chunk             |
| `text`      | string        | ✅ Yes   | Text content                    |
| `embedding` | array[float]  | ✅ Yes   | 768-dimensional vector          |
| `metadata`  | object        | ❌ No    | Optional metadata               |

### Response

```json
{
  "status": "success",
  "chunk_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## GET /graph/query

Query the knowledge graph to get entities and their relationships.

### Authentication

🔓 **Not Required**

### Request

```http
GET /graph/query?entity=machine+learning HTTP/1.1
Host: localhost:8001
```

#### Query Parameters

| Parameter | Type   | Required | Description          |
| --------- | ------ | -------- | -------------------- |
| `entity`  | string | ✅ Yes   | Entity name to query |

### Response

```json
{
  "entity": "machine learning",
  "nodes": [
    { "id": "machine learning", "label": "machine learning", "type": "entity" },
    {
      "id": "artificial intelligence",
      "label": "artificial intelligence",
      "type": "entity"
    },
    { "id": "neural networks", "label": "neural networks", "type": "entity" }
  ],
  "edges": [
    {
      "source": "machine learning",
      "target": "artificial intelligence",
      "relation": "is_a"
    },
    {
      "source": "neural networks",
      "target": "machine learning",
      "relation": "part_of"
    }
  ]
}
```

#### Response Fields

| Field              | Type   | Description               |
| ------------------ | ------ | ------------------------- |
| `entity`           | string | Queried entity            |
| `nodes`            | array  | Graph nodes (entities)    |
| `nodes[].id`       | string | Node identifier           |
| `nodes[].label`    | string | Display label             |
| `nodes[].type`     | string | Always "entity"           |
| `edges`            | array  | Connections between nodes |
| `edges[].source`   | string | Source entity ID          |
| `edges[].target`   | string | Target entity ID          |
| `edges[].relation` | string | Relationship type         |

### Frontend Display

Use a graph visualization library like:

- **D3.js force-directed graph**
- **vis.js Network**
- **Cytoscape.js**

---

## GET /health (RAG)

Health check for RAG service including database connectivity.

### Request

```http
GET /health HTTP/1.1
Host: localhost:8001
```

### Response

```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

# Auth Service API

The Auth Service handles Firebase token verification.

---

## POST /auth/verify

Verify a Firebase ID token and get user information.

### Request

```http
POST /auth/verify HTTP/1.1
Host: localhost:8000
Content-Type: application/json
```

```json
{
  "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Response

```json
{
  "valid": true,
  "user_id": "firebase_user_123",
  "email": "user@example.com"
}
```

---

## GET /auth/health

```http
GET /auth/health HTTP/1.1
Host: localhost:8000
```

```json
{
  "status": "ok"
}
```

---

# Error Handling

All services return consistent error responses.

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

| Status | Meaning        | Common Causes                        |
| ------ | -------------- | ------------------------------------ |
| 400    | Bad Request    | Invalid input, unsupported file type |
| 401    | Unauthorized   | Missing/invalid token                |
| 404    | Not Found      | Resource doesn't exist               |
| 500    | Internal Error | Server-side processing error         |

### Example Error Response

```json
{
  "detail": "Invalid Firebase token: Token has expired"
}
```

---

# Data Models

## Chunk

Represents a piece of text stored in the vector database.

```typescript
interface Chunk {
  id: string; // UUID
  user_id: string; // Firebase UID
  text: string; // Content
  metadata: {
    source: string; // Filename or "text_input"
    type: "text" | "pdf" | "image";
    file_url?: string; // Firebase Storage URL
    image_url?: string; // For image chunks
    page?: number; // For PDFs
  };
  score?: number; // Similarity score (in query responses)
}
```

## Knowledge Graph Node

```typescript
interface GraphNode {
  id: string;
  label: string;
  type: "entity";
}
```

## Knowledge Graph Edge

```typescript
interface GraphEdge {
  source: string;
  target: string;
  relation: string; // "is_a", "has", "part_of", "relates_to", etc.
}
```

---

# Quick Start for Frontend

### 1. Setup Firebase Auth

```javascript
import { initializeApp } from "firebase/app";
import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
```

### 2. Create API Helper

```javascript
class NerdieAPI {
  constructor(baseUrls) {
    this.ingestion = baseUrls.ingestion || "http://localhost:8002";
    this.rag = baseUrls.rag || "http://localhost:8001";
  }

  async getToken() {
    return await auth.currentUser?.getIdToken();
  }

  async ingestText(text, metadata = {}) {
    const token = await this.getToken();
    const res = await fetch(`${this.ingestion}/ingest/text`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text, metadata }),
    });
    return res.json();
  }

  async uploadFile(file, type = "pdf") {
    const token = await this.getToken();
    const formData = new FormData();
    formData.append("file", file);

    const endpoint = type === "pdf" ? "/ingest/pdf" : "/ingest/image";
    const res = await fetch(`${this.ingestion}${endpoint}`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    });
    return res.json();
  }

  async query(query) {
    const userId = auth.currentUser?.uid;
    const res = await fetch(`${this.rag}/rag/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, query }),
    });
    return res.json();
  }

  async getGraph(entity) {
    const res = await fetch(
      `${this.rag}/graph/query?entity=${encodeURIComponent(entity)}`
    );
    return res.json();
  }
}

export const api = new NerdieAPI();
```

### 3. Usage Examples

```javascript
// Ingest some text
await api.ingestText("Machine learning is amazing...", { topic: "AI" });

// Upload a PDF
const fileInput = document.querySelector('input[type="file"]');
await api.uploadFile(fileInput.files[0], "pdf");

// Ask a question
const result = await api.query("What is machine learning?");
console.log(result.answer);
console.log(result.chunks); // Show sources

// Get knowledge graph
const graph = await api.getGraph("machine learning");
// Render with D3.js or vis.js
```

---

## Swagger UI Links

Interactive API documentation:

- **Auth**: http://localhost:8000/docs
- **RAG**: http://localhost:8001/docs
- **Ingestion**: http://localhost:8002/docs
