# Nerdie RAG Service

Core RAG (Retrieval-Augmented Generation) backend service.

## Features

- **Vector Storage**: PostgreSQL + pgvector for semantic search
- **Gemini Integration**: Embeddings + LLM generation
- **Anti-Hallucination**: Answers only from knowledge base
- **Multi-tenant**: User-isolated document chunks

## Endpoints

| Endpoint         | Method | Description                 |
| ---------------- | ------ | --------------------------- |
| `/vector/insert` | POST   | Insert chunk with embedding |
| `/rag/query`     | POST   | Query knowledge base        |
| `/health`        | GET    | Health check                |

## Quick Start

```bash
# 1. Setup environment
cp .env.example .env
# Edit .env with your GEMINI_API_KEY

# 2. Start services
cd ..
docker-compose up --build

# 3. Wait for postgres to be healthy, then services start
```

**URLs:**

- RAG API: http://localhost:8001
- Docs: http://localhost:8001/docs
- PostgreSQL: localhost:5432

## API Examples

### Insert a chunk

```bash
curl -X POST http://localhost:8001/vector/insert \
  -H "Content-Type: application/json" \
  -d '{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "user_id": "user123",
    "text": "FastAPI is a modern Python web framework.",
    "embedding": [0.1, 0.2, ...],
    "metadata": {"source": "docs.pdf", "page": 1}
  }'
```

### Query RAG

```bash
curl -X POST http://localhost:8001/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is FastAPI?",
    "user_id": "user123",
    "top_k": 5
  }'
```

### Response format

```json
{
  "answer": "FastAPI is a modern Python web framework...",
  "chunks": [
    {"id": "...", "text": "...", "metadata": {...}, "score": 0.15}
  ],
  "context_used": "...",
  "scores": [0.15, 0.23, ...]
}
```

## Environment Variables

| Variable                 | Description           | Default            |
| ------------------------ | --------------------- | ------------------ |
| `POSTGRES_HOST`          | Database host         | postgres           |
| `POSTGRES_PORT`          | Database port         | 5432               |
| `GEMINI_API_KEY`         | Google AI API key     | required           |
| `GEMINI_EMBEDDING_MODEL` | Embedding model       | text-embedding-004 |
| `GEMINI_LLM_MODEL`       | LLM model             | gemini-1.5-flash   |
| `TOP_K`                  | Default results count | 5                  |

## Database Migrations

```bash
# Generate new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Architecture

```
/rag/query request
    │
    ▼
┌─────────────────┐
│ Embed query     │  ← Gemini text-embedding-004
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Similarity      │  ← pgvector cosine distance
│ Search          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Assemble        │  ← Top-K chunks with sources
│ Context         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate        │  ← Gemini Flash + anti-hallucination
│ Answer          │
└────────┬────────┘
         │
         ▼
    Response with answer + sources
```
