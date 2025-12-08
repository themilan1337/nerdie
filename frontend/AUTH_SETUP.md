# Firebase Google Auth Setup - Frontend

This document explains how Firebase Google Authentication is implemented in the Nerdie frontend (Nuxt 3).

## Overview

The authentication system uses Firebase Authentication for Google OAuth sign-in, which then communicates with the backend auth service at `https://auth.nerdie.lol` to verify tokens and manage user sessions.

## Architecture

```
User clicks "Login with Google"
    ↓
Firebase SDK opens Google OAuth popup
    ↓
User authenticates with Google
    ↓
Firebase returns ID token
    ↓
Frontend sends ID token to backend (https://auth.nerdie.lol/auth/google)
    ↓
Backend verifies token and returns user data + new tokens
    ↓
Frontend stores tokens in localStorage
    ↓
User is redirected to dashboard
```

## File Structure

```
frontend/
├── app/
│   ├── lib/
│   │   └── firebase.ts              # Firebase initialization
│   ├── composables/
│   │   └── useAuth.ts               # Auth composable with all auth logic
│   ├── middleware/
│   │   ├── auth.ts                  # Protects authenticated routes
│   │   └── guest.ts                 # Redirects authenticated users
│   ├── plugins/
│   │   └── auth.client.ts           # Initializes auth on app start
│   ├── pages/
│   │   ├── auth/
│   │   │   └── index.vue            # Login page with Google sign-in
│   │   └── dashboard/
│   │       └── index.vue            # Protected dashboard page
│   └── layouts/
│       └── dashboard.vue            # Dashboard layout with user profile
├── .env                              # Environment variables
└── AUTH_SETUP.md                     # This file
```

## Key Files

### 1. `app/lib/firebase.ts`
Initializes Firebase app with configuration.

### 2. `app/composables/useAuth.ts`
Main auth composable that provides:
- `signInWithGoogle()` - Handles Google OAuth login
- `signOut()` - Logs user out
- `getCurrentUser()` - Fetches current user from backend
- `getAuthHeader()` - Returns auth header for API calls
- `isAuthenticated` - Computed property for auth state
- `userData` - Current user data

### 3. `app/middleware/auth.ts`
Protects routes that require authentication. Redirects to `/auth` if not logged in.

### 4. `app/middleware/guest.ts`
Prevents logged-in users from accessing auth pages. Redirects to `/dashboard` if logged in.

### 5. `app/pages/auth/index.vue`
Login page with Google sign-in button. Shows loading state and error messages.

### 6. `app/layouts/dashboard.vue`
Dashboard layout with:
- User profile picture/avatar
- User name and email
- Logout button

## Usage

### Protect a Route

Add `middleware: 'auth'` to any page that requires authentication:

```vue
<script setup lang="ts">
definePageMeta({
  middleware: 'auth'
})
</script>
```

### Access User Data

Use the `useAuth()` composable:

```vue
<script setup lang="ts">
const { userData, isAuthenticated, signOut } = useAuth()

// Access user data
console.log(userData.value?.displayName)
console.log(userData.value?.email)
console.log(userData.value?.photoUrl)

// Check if authenticated
if (isAuthenticated.value) {
  console.log('User is logged in')
}

// Logout
const handleLogout = async () => {
  await signOut()
}
</script>
```

### Make Authenticated API Calls

Use `getAuthHeader()` to include auth token in requests:

```typescript
const { getAuthHeader } = useAuth()

const response = await fetch('https://api.nerdie.lol/some-endpoint', {
  method: 'GET',
  headers: {
    ...getAuthHeader(),
    'Content-Type': 'application/json'
  }
})
```

## Environment Variables

The following environment variables are configured in `.env`:

```env
# Firebase Configuration
NUXT_PUBLIC_FIREBASE_API_KEY=AIzaSyDQLypmEXwXsEdnGnaZ2NDGwXr1NQgi3rY
NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN=nerdie-85d0a.firebaseapp.com
NUXT_PUBLIC_FIREBASE_PROJECT_ID=nerdie-85d0a
NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET=nerdie-85d0a.firebasestorage.app
NUXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=626685033991
NUXT_PUBLIC_FIREBASE_APP_ID=1:626685033991:web:1c1f36e0e0a0b0fa1c1f36

# Auth API
NUXT_PUBLIC_AUTH_API_URL=https://auth.nerdie.lol
```

## Dependencies

The following packages are required:

- `firebase` (v12.6.0) - Firebase SDK for authentication

Install with:
```bash
pnpm add firebase
```

## How to Test

1. **Start the dev server:**
   ```bash
   pnpm dev
   ```

2. **Navigate to the auth page:**
   ```
   http://localhost:3000/auth
   ```

3. **Click "Login with Google"**
   - A Google OAuth popup will appear
   - Sign in with your Google account
   - You'll be redirected to the dashboard

4. **Check the dashboard:**
   - Your profile picture, name, and email should appear in the sidebar
   - Click on your profile to see the logout button

5. **Test logout:**
   - Click logout
   - You should be redirected back to `/auth`

6. **Test protected routes:**
   - Try to access `/dashboard` without being logged in
   - You should be redirected to `/auth`

## Token Storage

Tokens are stored in `localStorage`:
- `idToken` - Firebase ID token for authentication
- `refreshToken` - Refresh token for renewing sessions
- `userData` - User data (uid, email, displayName, photoUrl)

## Token Expiry

- Tokens expire after 1 hour (3600 seconds)
- When a token expires, the user will be automatically logged out
- User needs to sign in again to get a new token

## Security Notes

1. **Never commit `.env` files** - Add `.env` to `.gitignore`
2. **Use HTTPS in production** - Firebase requires HTTPS for OAuth
3. **Validate tokens on backend** - Always verify tokens server-side
4. **Use secure token storage** - Consider using httpOnly cookies in production
5. **Implement token refresh** - Add refresh token logic for better UX

## Troubleshooting

### "No authentication token found"
- User is not logged in
- Tokens were cleared from localStorage
- Solution: Redirect to `/auth` page

### "Session expired. Please sign in again."
- Token has expired (>1 hour old)
- Solution: User needs to log in again

### "Failed to authenticate with backend"
- Backend service is down
- Network error
- Invalid token
- Solution: Check backend logs and network connectivity

### CORS errors
- Backend CORS settings don't allow frontend domain
- Solution: Add frontend domain to backend CORS whitelist

### Firebase errors
- Invalid Firebase configuration
- Firebase project settings incorrect
- Solution: Check Firebase console and environment variables

## Backend Integration

The frontend expects the following endpoints from the backend:

### POST `/auth/google`
**Request:**
```json
{
  "idToken": "eyJhbGciOiJSUzI1NiIs..."
}
```

**Response:**
```json
{
  "uid": "abc123",
  "email": "user@gmail.com",
  "displayName": "John Doe",
  "photoUrl": "https://lh3.googleusercontent.com/...",
  "idToken": "eyJhbGciOiJSUzI1NiIs...",
  "refreshToken": "AMf-vBxW8Z...",
  "expiresIn": "3600"
}
```

### GET `/auth/me`
**Headers:**
```
Authorization: Bearer {idToken}
```

**Response:**
```json
{
  "uid": "abc123",
  "email": "user@gmail.com",
  "emailVerified": true,
  "displayName": "John Doe",
  "photoUrl": "https://lh3.googleusercontent.com/...",
  "disabled": false,
  "customClaims": {}
}
```

## Next Steps

1. **Add token refresh logic** - Automatically refresh tokens before they expire
2. **Add remember me** - Option to persist login across sessions
3. **Add session management** - Track active sessions
4. **Add social providers** - Support more OAuth providers (GitHub, Twitter, etc.)
5. **Add two-factor auth** - Extra security layer
6. **Add email verification** - Verify user emails
7. **Add password reset** - For email/password auth (if added later)

## Support

For issues or questions:
- Check the backend auth service logs
- Verify Firebase console settings
- Check browser console for errors
- Review network requests in DevTools
