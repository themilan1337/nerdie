# Nerdie - AI-Powered Knowledge Assistant

> Контекстная ИИ-система на базе Gemini API + RAG + векторизации для Pavlodar GDG Fest Hackathon 2025

![Nerdie](https://img.shields.io/badge/GDG-Hackathon%202025-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Gemini](https://img.shields.io/badge/Google-Gemini%202.5-8E75B2?style=for-the-badge&logo=google&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge&logo=vue.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)

## О проекте

**Nerdie** - это интеллектуальная система для работы с персональной базой знаний, построенная на современной RAG (Retrieval-Augmented Generation) архитектуре. Система позволяет загружать документы (PDF, изображения, текст), автоматически извлекает из них знания, создает векторные представления и предоставляет точные ответы на вопросы пользователя на основе загруженных данных.

### Ключевые преимущества

- **Нулевые галлюцинации**: Ответы формируются строго на основе загруженных документов
- **Прозрачность**: Каждый ответ содержит ссылки на источники и релевантные фрагменты
- **Мультимодальность**: Обработка PDF, изображений с OCR, обычного текста
- **Knowledge Graph**: Автоматическое извлечение сущностей и связей между ними
- **Умная векторизация**: Семантический поиск на основе Gemini Embeddings
- **Персональные данные**: Каждый пользователь имеет изолированную базу знаний

## Демо

- **Live Demo**: [https://www.nerdie.lol](https://www.nerdie.lol)
- **Demo Video**: [Ссылка на видео]

## Технологический стек

### Frontend
- **Nuxt 3** - Vue.js фреймворк для SSR/SPA
- **TailwindCSS** - Utility-first CSS
- **Firebase Auth** - Аутентификация пользователей
- **Firebase Storage** - Хранилище файлов

### Backend Services

#### Auth Service (Port 8000)
- FastAPI
- Firebase Admin SDK
- JWT token validation

#### RAG Service (Port 8001)
- FastAPI
- Gemini 2.5 Flash для генерации ответов
- PostgreSQL + pgvector для векторного поиска
- Conversation history management

#### Ingestion Service (Port 8002)
- FastAPI
- Gemini Embeddings (embedding-001)
- PyMuPDF для парсинга PDF
- Gemini Vision для OCR изображений
- Knowledge Graph extraction
- Cloud Firestore для метаданных

### Infrastructure
- **PostgreSQL 15** с расширением **pgvector**
- **Firebase** (Auth, Firestore, Storage)
- **Docker & Docker Compose**
- **Nginx** (reverse proxy)
- **Let's Encrypt** SSL сертификаты

## Архитектура системы

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                    (Nuxt 3 + Vue 3)                          │
│                   https://www.nerdie.lol                     │
└──────────────┬──────────────────────────────────────────────┘
               │
               ├─────────────────┬────────────────┬────────────┐
               │                 │                │            │
               ▼                 ▼                ▼            ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
    │ Auth Service │  │ RAG Service  │  │  Ingestion   │    │
    │   :8000      │  │    :8001     │  │   Service    │    │
    │              │  │              │  │    :8002     │    │
    │  Firebase    │  │   Gemini     │  │              │    │
    │   Admin      │  │  2.5 Flash   │  │   Gemini     │    │
    └──────────────┘  └──────┬───────┘  │  Embedding   │    │
                             │          │  + Vision    │    │
                             │          └──────┬───────┘    │
                             │                 │            │
                             ▼                 ▼            ▼
                      ┌──────────────────────────────────────┐
                      │      PostgreSQL 15 + pgvector        │
                      │      (Vector embeddings + chunks)     │
                      └──────────────────────────────────────┘
                                        │
                                        ▼
                      ┌──────────────────────────────────────┐
                      │         Firebase Firestore           │
                      │  (Knowledge Graph + Metadata)        │
                      └──────────────────────────────────────┘
```

## RAG Pipeline

### 1. Ingestion Pipeline

```
PDF/Image Upload
    │
    ▼
┌─────────────────────┐
│  File Processing    │
│  - PDF: PyMuPDF     │
│  - Image: Gemini    │
│    Vision OCR       │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Text Chunking     │
│  (500 chars/chunk   │
│   100 overlap)      │
└─────────┬───────────┘
          │
          ├─────────────────┬──────────────────┐
          │                 │                  │
          ▼                 ▼                  ▼
┌─────────────────┐  ┌─────────────┐  ┌──────────────┐
│ Gemini          │  │  Knowledge  │  │  Document    │
│ Embeddings      │  │   Graph     │  │  Summary     │
│ (768-dim)       │  │  Extraction │  │  (Gemini)    │
└────────┬────────┘  └──────┬──────┘  └──────┬───────┘
         │                  │                 │
         ▼                  ▼                 ▼
┌─────────────────┐  ┌─────────────┐  ┌──────────────┐
│  PostgreSQL     │  │  Firestore  │  │  Firestore   │
│  + pgvector     │  │  (Entities  │  │  (Metadata)  │
│  (Chunks)       │  │  Relations) │  │              │
└─────────────────┘  └─────────────┘  └──────────────┘
```

### 2. Retrieval Pipeline

```
User Query
    │
    ▼
┌─────────────────────┐
│ Query Embedding     │
│ (Gemini Embedding)  │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Vector Search      │
│  (pgvector)         │
│  - Cosine similarity│
│  - Top K=5          │
│  - Max distance=1.0 │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Context Assembly    │
│ - Ranked chunks     │
│ - Source metadata   │
│ - Conversation hist │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Gemini 2.5 Flash  │
│   Answer Generation │
│   + Sources         │
└─────────────────────┘
```

## Основной функционал

### Для пользователя

- **Аутентификация**: Вход через Firebase (Google, Email/Password)
- **Загрузка документов**:
  - PDF файлы с автоматическим извлечением текста
  - Изображения с OCR через Gemini Vision
  - Прямой ввод текста
- **Чат интерфейс**:
  - Задавайте вопросы по загруженным документам
  - Получайте точные ответы со ссылками на источники
  - Просматривайте релевантные фрагменты
  - История диалогов сохраняется
- **Управление документами**:
  - Просмотр всех загруженных документов
  - Просмотр извлеченных сущностей и связей
  - Удаление документов

### Технические возможности

- **Векторный поиск**: Семантическое сопоставление запросов и документов
- **Knowledge Graph**: Автоматическое построение графа знаний
- **Суммаризация**: Автоматическое создание резюме документов
- **Multimodal**: Поддержка текста, PDF, изображений
- **Context-aware**: Учет истории диалога для более точных ответов
- **User isolation**: Полная изоляция данных между пользователями

## Установка и запуск

### Требования

- Docker & Docker Compose
- Node.js 18+ (для локальной разработки фронтенда)
- Gemini API Key ([получить здесь](https://ai.google.dev/))
- Firebase проект ([создать здесь](https://console.firebase.google.com/))

### 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/nerdie.git
cd nerdie
```

### 2. Настройка Backend

#### Создайте Firebase проект и credentials

1. Создайте проект в [Firebase Console](https://console.firebase.google.com/)
2. Включите Authentication (Email/Password, Google)
3. Создайте Firestore Database
4. Создайте Storage bucket
5. Скачайте `firebase-credentials.json` (Project Settings → Service Accounts → Generate new private key)
6. Поместите файл в `backend/auth/firebase-credentials.json`

#### Настройте переменные окружения

**backend/auth/.env:**
```env
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_API_KEY=your-api-key
FIREBASE_CREDENTIALS=./firebase-credentials.json
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

**backend/rag_service/.env:**
```env
POSTGRES_USER=nerdie
POSTGRES_PASSWORD=nerdie_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=nerdie_rag

GEMINI_API_KEY=your-gemini-api-key
GEMINI_EMBEDDING_MODEL=embedding-001
GEMINI_LLM_MODEL=gemini-2.5-flash

EMBEDDING_DIMENSION=768
TOP_K=5
MAX_DISTANCE=1.0

FIREBASE_PROJECT_ID=your-project-id
FIREBASE_API_KEY=your-api-key
FIREBASE_CREDENTIALS=./firebase-credentials.json

CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

**backend/ingestion/.env:**
```env
POSTGRES_USER=nerdie
POSTGRES_PASSWORD=nerdie_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=nerdie_rag

GEMINI_API_KEY=your-gemini-api-key
GEMINI_EMBEDDING_MODEL=embedding-001
GEMINI_LLM_MODEL=gemini-2.5-flash

EMBEDDING_DIMENSION=768
TOP_K=5
MAX_DISTANCE=1.0

FIREBASE_PROJECT_ID=your-project-id
FIREBASE_API_KEY=your-api-key
FIREBASE_CREDENTIALS=./firebase-credentials.json

CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

#### Запуск Backend

```bash
cd backend
docker-compose up -d --build
```

Проверьте статус:
```bash
docker-compose ps
```

API будут доступны:
- Auth Service: http://localhost:8000
- RAG Service: http://localhost:8001
- Ingestion Service: http://localhost:8002
- PostgreSQL: localhost:5432

### 3. Настройка Frontend

**frontend/.env:**
```env
# Firebase Configuration
NUXT_PUBLIC_FIREBASE_API_KEY=your-api-key
NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
NUXT_PUBLIC_FIREBASE_PROJECT_ID=your-project-id
NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your-project.firebasestorage.app
NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
NUXT_PUBLIC_FIREBASE_APP_ID=your-app-id

# API Endpoints
NUXT_PUBLIC_AUTH_API_URL=http://localhost:8000
NUXT_PUBLIC_RAG_API_URL=http://localhost:8001
NUXT_PUBLIC_INGESTION_API_URL=http://localhost:8002
```

#### Запуск Frontend

```bash
cd frontend
npm install
npm run dev
```

Приложение будет доступно на http://localhost:3000

### 4. Production Deployment

Для продакшн деплоя используйте nginx с SSL:

```bash
# Обновите конфигурацию nginx (пример в update_nginx_cors.sh)
sudo nano /etc/nginx/sites-available/nerdie.conf

# Проверьте конфигурацию
sudo nginx -t

# Перезагрузите nginx
sudo systemctl reload nginx
```

Frontend можно задеплоить на:
- Vercel (рекомендуется для Nuxt)
- Netlify
- Firebase Hosting
- Собственный VPS с nginx

## API Documentation

### Auth Service (http://localhost:8000)

#### POST /auth/register
Регистрация нового пользователя
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### POST /auth/login
Вход пользователя
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### GET /auth/verify
Проверка токена
```
Headers: Authorization: Bearer <firebase-token>
```

### Ingestion Service (http://localhost:8002)

#### POST /ingest/pdf
Загрузка PDF документа
```
Content-Type: multipart/form-data
Headers: Authorization: Bearer <firebase-token>
Body: file=<pdf-file>
```

#### POST /ingest/image
Загрузка изображения
```
Content-Type: multipart/form-data
Headers: Authorization: Bearer <firebase-token>
Body: file=<image-file>
```

#### POST /ingest/text
Загрузка текста
```json
Headers: Authorization: Bearer <firebase-token>
{
  "text": "Your text content here",
  "metadata": {
    "source": "manual_input"
  }
}
```

#### GET /ingest/documents
Получить список документов пользователя
```
Headers: Authorization: Bearer <firebase-token>
```

### RAG Service (http://localhost:8001)

#### POST /rag/query
Задать вопрос
```json
Headers: Authorization: Bearer <firebase-token>
{
  "query": "What is the main topic of the document?",
  "conversation_id": "optional-conversation-id",
  "top_k": 5
}
```

Response:
```json
{
  "answer": "Based on the documents...",
  "sources": [
    {
      "chunk_id": 123,
      "text": "Relevant fragment...",
      "metadata": {
        "source": "document.pdf",
        "file_url": "https://..."
      },
      "similarity": 0.89
    }
  ],
  "conversation_id": "uuid"
}
```

#### GET /vector/chunks
Получить все chunks пользователя
```
Headers: Authorization: Bearer <firebase-token>
```

#### DELETE /vector/chunks/{chunk_id}
Удалить chunk
```
Headers: Authorization: Bearer <firebase-token>
```

## Примеры использования

### 1. Загрузка документа через CLI

```bash
# Загрузить PDF
curl -X POST https://ingest.nerdie.lol/ingest/pdf \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
  -F "file=@document.pdf"

# Загрузить изображение
curl -X POST https://ingest.nerdie.lol/ingest/image \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
  -F "file=@screenshot.png"
```

### 2. Задать вопрос через CLI

```bash
curl -X POST https://rag.nerdie.lol/rag/query \
  -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key findings?",
    "top_k": 5
  }'
```

## Roadmap

- [ ] Поддержка других форматов документов (DOCX, TXT, MD)
- [ ] Визуализация Knowledge Graph
- [ ] Экспорт диалогов
- [ ] Поддержка аудио/видео транскрипции
- [ ] Collaborative workspaces
- [ ] Fine-tuning для специфических доменов
- [ ] Advanced analytics dashboard

## Требования хакатона

- [x] Использование Gemini API (2.5 Flash + Embeddings)
- [x] Векторизация данных (Gemini Embeddings + pgvector)
- [x] RAG-архитектура (полный pipeline)
- [x] Пользовательский интерфейс (Vue.js/Nuxt 3)
- [x] Работа с реальными данными
- [x] Прозрачность источников
- [x] Защита от галлюцинаций
- [x] Обработка отсутствия данных

## Команда

- **Backend Development**: [Ваше имя]
- **Frontend Development**: [Ваше имя]
- **DevOps & Infrastructure**: [Ваше имя]
- **UI/UX Design**: [Ваше имя]

## Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## Ссылки

- [Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Gemini Embeddings](https://ai.google.dev/gemini-api/docs/embeddings)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [Nuxt 3 Documentation](https://nuxt.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## Acknowledgments

Создано для **Pavlodar GDG Fest Hackathon 2025**

Powered by:
- Google Gemini AI
- Firebase
- PostgreSQL + pgvector
- Vue.js & Nuxt 3

---

Made with ❤️ for GDG Pavlodar
