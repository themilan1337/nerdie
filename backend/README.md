# Nerdie Backend

Backend microservices for the Nerdie RAG-powered knowledge assistant.

## Services

### Auth Service (`/auth`)

Firebase authentication microservice.

**Endpoints:**

- `POST /auth/signup` - Create new user
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh token
- `GET /auth/me` - Get current user (requires Bearer token)
- `GET /auth/health` - Health check

## Quick Start

### 1. Setup Firebase Credentials

```bash
cd auth
cp .env.example .env
# Edit .env with your Firebase project settings
# Add your firebase-credentials.json file
```

### 2. Run with Docker Compose

```bash
docker-compose up --build
```

Services:

- **Auth**: http://localhost:8000
- **PostgreSQL (pgvector)**: localhost:5432

### 3. API Documentation

Open http://localhost:8000/docs for Swagger UI.

## API Examples

### Signup

```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### Refresh Token

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refreshToken": "YOUR_REFRESH_TOKEN"}'
```

### Get Current User

```bash
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_ID_TOKEN"
```

## Environment Variables

| Variable               | Description                     |
| ---------------------- | ------------------------------- |
| `FIREBASE_PROJECT_ID`  | Firebase project ID             |
| `FIREBASE_API_KEY`     | Firebase Web API key            |
| `FIREBASE_CREDENTIALS` | Path to service account JSON    |
| `CORS_ORIGINS`         | Comma-separated allowed origins |

## Tech Stack

- **Python 3.10+** / FastAPI
- **Firebase Admin SDK** - Token verification
- **Firebase Auth REST API** - User operations
- **PostgreSQL + pgvector** - Vector store for RAG
