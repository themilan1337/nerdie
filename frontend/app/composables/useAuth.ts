import { ref, computed, onMounted } from 'vue'
import {
  signInWithRedirect,
  GoogleAuthProvider,
  signOut as firebaseSignOut,
  onAuthStateChanged,
  getRedirectResult,
  type User
} from 'firebase/auth'
import { auth } from '../lib/firebase'

interface UserData {
  uid: string
  email: string | null
  displayName: string | null
  photoUrl: string | null
  idToken: string
  refreshToken: string
  expiresIn: string
}

const currentUser = ref<User | null>(null)
const userData = ref<UserData | null>(null)
const isLoading = ref(true)
const error = ref<string | null>(null)

export const useAuth = () => {
  const config = useRuntimeConfig()
  const router = useRouter()

  // Auth API base URL
  const AUTH_API_URL = 'https://auth.nerdie.lol'

  // Check if user is authenticated
  const isAuthenticated = computed(() => !!currentUser.value && !!userData.value)

  // Initialize auth state listener
  const initAuthListener = () => {
    onAuthStateChanged(auth, async (user) => {
      currentUser.value = user

      if (user) {
        // Get stored user data
        const storedUserData = localStorage.getItem('userData')
        if (storedUserData) {
          userData.value = JSON.parse(storedUserData)
        }
      } else {
        userData.value = null
        localStorage.removeItem('userData')
        localStorage.removeItem('idToken')
        localStorage.removeItem('refreshToken')
      }

      isLoading.value = false
    })
  }

  // Sign in with Google
  const signInWithGoogle = async () => {
    try {
      isLoading.value = true
      error.value = null

      // Use redirect instead of popup to avoid COOP issues
      const provider = new GoogleAuthProvider()
      await signInWithRedirect(auth, provider)
      // User will be redirected, no need to continue here
    } catch (err: any) {
      console.error('Google sign-in error:', err)
      error.value = err.message || 'Failed to sign in with Google'
      isLoading.value = false
      throw err
    }
  }

  // Handle redirect result after Google sign-in
  const handleRedirectResult = async () => {
    console.log('🔍 [AUTH] handleRedirectResult called')
    try {
      isLoading.value = true
      console.log('🔍 [AUTH] Getting redirect result from Firebase...')
      const result = await getRedirectResult(auth)

      console.log('🔍 [AUTH] Redirect result:', result)

      if (!result) {
        // No redirect result, user just loaded the page normally
        console.log('ℹ️ [AUTH] No redirect result found (normal page load)')
        isLoading.value = false
        return
      }

      console.log('✅ [AUTH] Redirect result found! User:', result.user.email)

      // Step 1: Get the Firebase ID token
      console.log('🔍 [AUTH] Getting ID token...')
      const idToken = await result.user.getIdToken()
      console.log('✅ [AUTH] Got ID token:', idToken.substring(0, 20) + '...')

      // Step 2: Send token to backend for verification
      console.log('🔍 [AUTH] Sending token to backend:', AUTH_API_URL)
      const response = await fetch(`${AUTH_API_URL}/auth/google`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idToken })
      })

      console.log('🔍 [AUTH] Backend response status:', response.status)

      if (!response.ok) {
        const errorData = await response.json()
        console.error('❌ [AUTH] Backend error:', errorData)
        throw new Error(errorData.message || 'Failed to authenticate with backend')
      }

      const data: UserData = await response.json()
      console.log('✅ [AUTH] Backend response:', data)

      // Step 3: Store tokens and user data
      userData.value = data
      localStorage.setItem('idToken', data.idToken)
      localStorage.setItem('refreshToken', data.refreshToken)
      localStorage.setItem('userData', JSON.stringify(data))
      console.log('✅ [AUTH] Tokens stored in localStorage')

      // Step 4: Redirect to dashboard
      console.log('🔍 [AUTH] Redirecting to dashboard...')
      await router.push('/dashboard')
      console.log('✅ [AUTH] Redirected to dashboard')

      return data
    } catch (err: any) {
      console.error('❌ [AUTH] Redirect result error:', err)
      error.value = err.message || 'Failed to complete sign in'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Sign out
  const signOut = async () => {
    try {
      isLoading.value = true
      error.value = null

      // Sign out from Firebase
      await firebaseSignOut(auth)

      // Clear local storage
      localStorage.removeItem('idToken')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('userData')

      userData.value = null
      currentUser.value = null

      // Redirect to auth page
      await router.push('/auth')
    } catch (err: any) {
      console.error('Sign out error:', err)
      error.value = err.message || 'Failed to sign out'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Get current user info from backend
  const getCurrentUser = async () => {
    try {
      const idToken = localStorage.getItem('idToken')

      if (!idToken) {
        throw new Error('No authentication token found')
      }

      const response = await fetch(`${AUTH_API_URL}/auth/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${idToken}`
        }
      })

      if (!response.ok) {
        if (response.status === 401) {
          // Token expired, sign out
          await signOut()
          throw new Error('Session expired. Please sign in again.')
        }
        throw new Error('Failed to get user info')
      }

      const data = await response.json()
      return data
    } catch (err: any) {
      console.error('Get current user error:', err)
      error.value = err.message
      throw err
    }
  }

  // Check if token is valid
  const checkTokenValidity = async () => {
    try {
      await getCurrentUser()
      return true
    } catch {
      return false
    }
  }

  // Get auth header for API requests
  const getAuthHeader = () => {
    const idToken = localStorage.getItem('idToken')
    if (!idToken) return null
    return { Authorization: `Bearer ${idToken}` }
  }

  return {
    currentUser,
    userData,
    isAuthenticated,
    isLoading,
    error,
    signInWithGoogle,
    signOut,
    getCurrentUser,
    checkTokenValidity,
    getAuthHeader,
    initAuthListener,
    handleRedirectResult
  }
}
