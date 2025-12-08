# 🔐 Auth API - Примеры запросов

## Обзор
Сервис авторизации работает **ТОЛЬКО через Google Firebase Auth**. Email/password авторизация удалена.

---

## 📍 Endpoints

### 1. **POST /auth/google** - Авторизация через Google

#### Как это работает:
1. На фронтенде пользователь логинится через Google с помощью Firebase SDK
2. Получаете `idToken` от Firebase
3. Отправляете этот токен на бэкенд
4. Бэкенд проверяет токен и возвращает информацию о пользователе

#### 📤 Request:
```bash
curl -X POST 'http://localhost:8000/auth/google' \
  -H 'Content-Type: application/json' \
  -d '{
    "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjZmNzI1NDEwMWY1NmU0MWNmMzVjZTU4..."
  }'
```

#### JavaScript/TypeScript пример:
```javascript
// 1. Настройка Firebase на фронтенде
import { initializeApp } from 'firebase/app';
import { getAuth, signInWithPopup, GoogleAuthProvider } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// 2. Функция для входа через Google
async function loginWithGoogle() {
  try {
    // Открываем popup для входа через Google
    const provider = new GoogleAuthProvider();
    const result = await signInWithPopup(auth, provider);

    // Получаем ID токен
    const idToken = await result.user.getIdToken();

    // Отправляем токен на ваш бэкенд
    const response = await fetch('http://localhost:8000/auth/google', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ idToken })
    });

    const userData = await response.json();
    console.log('Успешный вход:', userData);

    // Сохраняем токены
    localStorage.setItem('idToken', userData.idToken);
    localStorage.setItem('refreshToken', userData.refreshToken);

    return userData;
  } catch (error) {
    console.error('Ошибка входа:', error);
    throw error;
  }
}
```

#### React пример:
```jsx
import { signInWithPopup, GoogleAuthProvider } from 'firebase/auth';
import { auth } from './firebase-config';

function LoginButton() {
  const handleGoogleLogin = async () => {
    try {
      const provider = new GoogleAuthProvider();
      const result = await signInWithPopup(auth, provider);
      const idToken = await result.user.getIdToken();

      const response = await fetch('http://localhost:8000/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idToken })
      });

      const data = await response.json();
      console.log('User data:', data);

      // Сохраняем токены
      localStorage.setItem('idToken', data.idToken);
      localStorage.setItem('refreshToken', data.refreshToken);

    } catch (error) {
      console.error('Login failed:', error);
    }
  };

  return (
    <button onClick={handleGoogleLogin}>
      Sign in with Google
    </button>
  );
}
```

#### 📥 Response (200 OK):
```json
{
  "uid": "abc123def456",
  "email": "user@gmail.com",
  "displayName": "John Doe",
  "photoUrl": "https://lh3.googleusercontent.com/a/default-user",
  "idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjZmNzI1NDEwMWY1NmU0MWNmMzVjZTU4...",
  "refreshToken": "AMf-vBxW8Z1a2b3c4d5e6f7g8h9i...",
  "expiresIn": "3600"
}
```

#### ❌ Error Responses:

**401 Unauthorized:**
```json
{
  "error": "InvalidToken",
  "message": "The provided Firebase ID token is invalid or expired"
}
```

**400 Bad Request:**
```json
{
  "error": "AuthError",
  "message": "Failed to authenticate with Google"
}
```

---

### 2. **GET /auth/me** - Получить информацию о текущем пользователе

#### 📤 Request:
```bash
curl -X GET 'http://localhost:8000/auth/me' \
  -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjZmNzI1NDEwMWY1NmU0MWNmMzVjZTU4...'
```

#### JavaScript пример:
```javascript
async function getCurrentUser() {
  const idToken = localStorage.getItem('idToken');

  const response = await fetch('http://localhost:8000/auth/me', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${idToken}`
    }
  });

  if (response.ok) {
    const userData = await response.json();
    console.log('Current user:', userData);
    return userData;
  } else {
    console.error('Failed to get user');
    // Токен истёк, нужно перелогиниться
  }
}
```

#### Axios пример:
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

// Добавляем токен ко всем запросам
api.interceptors.request.use(config => {
  const token = localStorage.getItem('idToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Использование
async function getMe() {
  try {
    const response = await api.get('/auth/me');
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('Error:', error);
  }
}
```

#### 📥 Response (200 OK):
```json
{
  "uid": "abc123def456",
  "email": "user@gmail.com",
  "emailVerified": true,
  "displayName": "John Doe",
  "photoUrl": "https://lh3.googleusercontent.com/a/default-user",
  "disabled": false,
  "customClaims": {}
}
```

#### ❌ Error (401 Unauthorized):
```json
{
  "error": "InvalidToken",
  "message": "The provided token is invalid or expired"
}
```

---

### 3. **GET /auth/health** - Health check

#### 📤 Request:
```bash
curl -X GET 'http://localhost:8000/auth/health'
```

#### 📥 Response (200 OK):
```json
{
  "status": "healthy",
  "service": "auth"
}
```

---

## 🔄 Полный Flow авторизации

```javascript
// 1. Инициализация Firebase (один раз при запуске приложения)
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

// 2. Создаём AuthService
class AuthService {
  constructor(apiUrl) {
    this.apiUrl = apiUrl;
  }

  // Вход через Google
  async loginWithGoogle() {
    const provider = new GoogleAuthProvider();
    const result = await signInWithPopup(auth, provider);
    const idToken = await result.user.getIdToken();

    // Отправляем на бэкенд
    const response = await fetch(`${this.apiUrl}/auth/google`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idToken })
    });

    const data = await response.json();

    // Сохраняем токены
    localStorage.setItem('idToken', data.idToken);
    localStorage.setItem('refreshToken', data.refreshToken);

    return data;
  }

  // Получить текущего пользователя
  async getCurrentUser() {
    const idToken = localStorage.getItem('idToken');

    const response = await fetch(`${this.apiUrl}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${idToken}`
      }
    });

    if (!response.ok) {
      throw new Error('Not authenticated');
    }

    return await response.json();
  }

  // Выход
  logout() {
    localStorage.removeItem('idToken');
    localStorage.removeItem('refreshToken');
    return auth.signOut();
  }

  // Проверка авторизации
  isAuthenticated() {
    return !!localStorage.getItem('idToken');
  }
}

// 3. Использование
const authService = new AuthService('http://localhost:8000');

// Вход
await authService.loginWithGoogle();

// Получить пользователя
const user = await authService.getCurrentUser();

// Выход
await authService.logout();
```

---

## 🚀 Запуск сервиса

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера
uvicorn app.main:app --reload --port 8000
```

Swagger UI доступен по адресу: `http://localhost:8000/docs`

---

## 🔑 Важные моменты

1. **Токены имеют срок действия 1 час (3600 секунд)**
2. **Храните токены безопасно** (localStorage или sessionStorage)
3. **Используйте HTTPS в продакшене**
4. **Проверяйте токен на каждый защищённый запрос**
5. **При истечении токена - перелогиньте пользователя**

---

## 🛠️ Troubleshooting

### Ошибка "Invalid token"
- Токен истёк (прошло больше 1 часа)
- Токен неправильный
- **Решение:** Попросите пользователя перелогиниться

### Ошибка "Failed to authenticate with Google"
- Неправильная настройка Firebase
- Проблемы с Firebase credentials
- **Решение:** Проверьте firebase-credentials.json и .env файл

### CORS ошибки
- Добавьте домен фронтенда в `CORS_ORIGINS` в `.env` файле
```
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```
