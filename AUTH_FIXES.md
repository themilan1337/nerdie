# Auth Fixes - CORS & Redirect Issues

## Проблемы которые были исправлены

### 1. CORS Error (404 на /auth/google)
**Проблема:** Backend не принимал запросы с фронтенда из-за CORS
**Решение:** Добавлены правильные CORS origins в backend

**Файл:** `backend/auth/.env`
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://nerdie.lol,https://www.nerdie.lol,http://nerdie.lol,http://www.nerdie.lol
```

### 2. Cross-Origin-Opener-Policy Error
**Проблема:** Firebase popup блокировался браузером из-за COOP политики
**Решение:** Изменен метод авторизации с popup на redirect

**Изменения в frontend:**
- Заменен `signInWithPopup` на `signInWithRedirect`
- Добавлена функция `handleRedirectResult()` для обработки возврата с Google
- Auth page теперь проверяет redirect result при загрузке

## Что нужно сделать

### 1. Перезапустить Backend Auth Service

```bash
cd ~/nerdie/backend
docker compose restart auth
```

Или если нужно полностью пересобрать:

```bash
cd ~/nerdie/backend
docker compose down auth
docker compose up -d auth
```

### 2. Проверить логи Backend

```bash
docker compose logs -f auth
```

Должно быть:
```
✅ Firebase initialized successfully
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3. Проверить что CORS правильно настроен

В логах при запросе с фронтенда не должно быть CORS ошибок.

## Как теперь работает авторизация

### Старый способ (с popup):
1. Пользователь нажимает "Login with Google"
2. Открывается popup окно с Google OAuth
3. ❌ COOP блокирует общение между popup и родительским окном
4. ❌ Ошибка

### Новый способ (с redirect):
1. Пользователь нажимает "Login with Google"
2. Страница перенаправляется на Google OAuth
3. Пользователь авторизуется на Google
4. Google перенаправляет обратно на `/auth`
5. ✅ `handleRedirectResult()` обрабатывает результат
6. ✅ Токен отправляется на backend
7. ✅ Пользователь перенаправляется на `/dashboard`

## Тестирование

1. Открой `https://nerdie.lol/auth` (или твой фронтенд домен)
2. Нажми "Login with Google"
3. Тебя перенаправит на Google
4. Войди с Google аккаунтом
5. Тебя вернет на `/auth`
6. Автоматически перенаправит на `/dashboard`

## Проверка ошибок

### Если все еще 404:
```bash
# Проверь что роутер правильно подключен
curl https://auth.nerdie.lol/auth/health

# Должно вернуть:
{"status":"healthy","service":"auth"}
```

### Если CORS ошибка:
```bash
# Проверь .env файл
cat backend/auth/.env | grep CORS

# Должно быть:
CORS_ORIGINS=http://localhost:3000,...,https://nerdie.lol,...
```

### Если Firebase ошибка:
```bash
# Проверь Firebase credentials
cat backend/auth/.env | grep FIREBASE

# Проверь что файл существует
ls -la backend/auth/firebase-credentials.json
```

## Дополнительные изменения

### Frontend файлы изменены:
1. `app/composables/useAuth.ts`
   - Заменен signInWithPopup на signInWithRedirect
   - Добавлена handleRedirectResult()

2. `app/pages/auth/index.vue`
   - Добавлен onMounted с вызовом handleRedirectResult()
   - Обновлен handleGoogleLogin

### Backend файлы изменены:
1. `backend/auth/.env`
   - Добавлены production CORS origins

## Готово!

После перезапуска backend сервиса, авторизация должна работать без ошибок.

## Troubleshooting

### Проблема: Redirect loop на /auth
**Решение:** Очисти localStorage в браузере и попробуй снова

### Проблема: "Failed to authenticate with backend"
**Решение:**
1. Проверь что backend запущен: `docker compose ps auth`
2. Проверь логи: `docker compose logs auth`
3. Проверь что CORS настроен правильно

### Проблема: Firebase ошибка "auth/operation-not-allowed"
**Решение:** В Firebase Console включи Google Authentication:
1. Зайди в Firebase Console
2. Authentication → Sign-in method
3. Включи Google provider
4. Добавь authorized domains
