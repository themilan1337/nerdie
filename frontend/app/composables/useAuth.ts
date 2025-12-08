import { ref, computed, onMounted } from 'vue'
import {
  signInWithRedirect,
  signInWithPopup,
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
    console.log('🔍 [AUTH] Initializing auth state listener...')
    onAuthStateChanged(auth, async (user) => {
      console.log('🔍 [AUTH] Auth state changed!')
      console.log('🔍 [AUTH] User is:', user ? 'logged in' : 'logged out')

      currentUser.value = user

      if (user) {
        console.log('✅ [AUTH] User logged in:', user.email)
        console.log('✅ [AUTH] User UID:', user.uid)
        console.log('✅ [AUTH] User display name:', user.displayName)

        // Get stored user data
        const storedUserData = localStorage.getItem('userData')
        console.log('🔍 [AUTH] Checking localStorage for userData...')
        if (storedUserData) {
          userData.value = JSON.parse(storedUserData)
          console.log('✅ [AUTH] Found stored userData:', userData.value?.email)
        } else {
          console.log('⚠️ [AUTH] No stored userData found in localStorage')
        }
      } else {
        console.log('ℹ️ [AUTH] No user logged in, clearing data...')
        userData.value = null
        localStorage.removeItem('userData')
        localStorage.removeItem('idToken')
        localStorage.removeItem('refreshToken')
        console.log('✅ [AUTH] All auth data cleared from localStorage')
      }

      isLoading.value = false
      console.log('🔍 [AUTH] isLoading set to false')
    })
    console.log('✅ [AUTH] Auth state listener initialized')
  }

  // Sign in with Google using POPUP (more reliable than redirect)
  const signInWithGoogle = async () => {
    console.log('=' .repeat(80))
    console.log('🔍 [AUTH] signInWithGoogle called at:', new Date().toISOString())
    console.log('🔍 [AUTH] Current URL:', window.location.href)
    console.log('=' .repeat(80))

    try {
      isLoading.value = true
      error.value = null
      console.log('🔍 [AUTH] isLoading set to true, error cleared')

      console.log('🔍 [AUTH] Creating GoogleAuthProvider...')
      const provider = new GoogleAuthProvider()
      console.log('✅ [AUTH] GoogleAuthProvider created')

      // Use POPUP instead of redirect - it's more reliable
      console.log('🔍 [AUTH] Calling signInWithPopup...')
      console.log('🔍 [AUTH] This will open a popup window for Google OAuth')

      const result = await signInWithPopup(auth, provider)

      console.log('✅ [AUTH] Popup sign-in successful!')
      console.log('✅ [AUTH] User email:', result.user?.email || 'NO EMAIL')
      console.log('✅ [AUTH] User UID:', result.user?.uid || 'NO UID')

      // Step 1: Get the Firebase ID token
      console.log('🔍 [AUTH] Step 1: Getting ID token...')
      const idToken = await result.user.getIdToken()
      console.log('✅ [AUTH] Got ID token (length:', idToken.length, ')')

      // Step 2: Send token to backend for verification
      console.log('🔍 [AUTH] Step 2: Sending token to backend')
      console.log('🔍 [AUTH] Backend URL:', AUTH_API_URL)

      const response = await fetch(`${AUTH_API_URL}/auth/google`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idToken })
      })
      console.log('✅ [AUTH] Fetch completed, status:', response.status)

      if (!response.ok) {
        const errorData = await response.json()
        console.error('❌ [AUTH] Backend error:', errorData)
        throw new Error(errorData.message || 'Failed to authenticate with backend')
      }

      const data: UserData = await response.json()
      console.log('✅ [AUTH] Backend response:', data)

      // Step 3: Store tokens and user data
      console.log('🔍 [AUTH] Step 3: Storing tokens...')
      userData.value = data
      localStorage.setItem('idToken', data.idToken)
      localStorage.setItem('refreshToken', data.refreshToken)
      localStorage.setItem('userData', JSON.stringify(data))
      console.log('✅ [AUTH] All tokens stored')

      // Step 4: Redirect to dashboard
      console.log('🔍 [AUTH] Step 4: Redirecting to dashboard...')
      await router.push('/dashboard')
      console.log('✅✅✅ [AUTH] AUTHENTICATION COMPLETED! ✅✅✅')

    } catch (err: any) {
      console.log('=' .repeat(80))
      console.error('❌ [AUTH] Google sign-in error!')
      console.error('❌ [AUTH] Error type:', typeof err)
      console.error('❌ [AUTH] Error name:', err.name)
      console.error('❌ [AUTH] Error message:', err.message)
      console.error('❌ [AUTH] Error code:', err.code)
      console.error('❌ [AUTH] Error stack:', err.stack)
      console.error('❌ [AUTH] Full error:', err)
      console.log('=' .repeat(80))
      error.value = err.message || 'Failed to sign in with Google'
      isLoading.value = false
      throw err
    }
  }

  // Handle redirect result after Google sign-in
  const handleRedirectResult = async () => {
    console.log('=' .repeat(80))
    console.log('🔍 [AUTH] handleRedirectResult called at:', new Date().toISOString())
    console.log('🔍 [AUTH] Current URL:', window.location.href)
    console.log('🔍 [AUTH] Current path:', window.location.pathname)
    console.log('🔍 [AUTH] URL search params:', window.location.search)
    console.log('=' .repeat(80))

    try {
      isLoading.value = true
      console.log('🔍 [AUTH] isLoading set to true')

      console.log('🔍 [AUTH] Getting redirect result from Firebase...')
      console.log('🔍 [AUTH] Auth instance:', auth ? 'initialized' : 'NOT initialized')

      const result = await getRedirectResult(auth)
      console.log('🔍 [AUTH] getRedirectResult completed')
      console.log('🔍 [AUTH] Redirect result type:', typeof result)
      console.log('🔍 [AUTH] Redirect result is null?', result === null)
      console.log('🔍 [AUTH] Redirect result is undefined?', result === undefined)
      console.log('🔍 [AUTH] Full redirect result:', JSON.stringify(result, null, 2))

      if (!result) {
        // No redirect result, user just loaded the page normally
        console.log('ℹ️ [AUTH] No redirect result found (normal page load)')
        console.log('ℹ️ [AUTH] This is expected if user just navigated to /auth without OAuth redirect')
        isLoading.value = false
        return
      }

      console.log('✅ [AUTH] Redirect result found!')
      console.log('✅ [AUTH] User email:', result.user?.email || 'NO EMAIL')
      console.log('✅ [AUTH] User UID:', result.user?.uid || 'NO UID')
      console.log('✅ [AUTH] User display name:', result.user?.displayName || 'NO NAME')
      console.log('✅ [AUTH] Provider ID:', result.providerId || 'NO PROVIDER')

      // Step 1: Get the Firebase ID token
      console.log('🔍 [AUTH] Step 1: Getting ID token...')
      const idToken = await result.user.getIdToken()
      console.log('✅ [AUTH] Got ID token (length:', idToken.length, ')')
      console.log('✅ [AUTH] ID token preview:', idToken.substring(0, 50) + '...' + idToken.substring(idToken.length - 20))

      // Step 2: Send token to backend for verification
      console.log('🔍 [AUTH] Step 2: Sending token to backend')
      console.log('🔍 [AUTH] Backend URL:', AUTH_API_URL)
      console.log('🔍 [AUTH] Request URL:', `${AUTH_API_URL}/auth/google`)
      console.log('🔍 [AUTH] Request method: POST')
      console.log('🔍 [AUTH] Request headers:', { 'Content-Type': 'application/json' })
      console.log('🔍 [AUTH] Request body idToken length:', idToken.length)

      let response
      try {
        response = await fetch(`${AUTH_API_URL}/auth/google`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ idToken })
        })
        console.log('✅ [AUTH] Fetch completed successfully')
      } catch (fetchError: any) {
        console.error('❌ [AUTH] Fetch failed with error:', fetchError)
        console.error('❌ [AUTH] Error name:', fetchError.name)
        console.error('❌ [AUTH] Error message:', fetchError.message)
        console.error('❌ [AUTH] Error stack:', fetchError.stack)
        throw new Error(`Network request failed: ${fetchError.message}`)
      }

      console.log('🔍 [AUTH] Backend response status:', response.status)
      console.log('🔍 [AUTH] Backend response ok?', response.ok)
      console.log('🔍 [AUTH] Backend response headers:', Object.fromEntries(response.headers.entries()))

      if (!response.ok) {
        console.error('❌ [AUTH] Backend returned error status:', response.status)
        let errorData
        try {
          errorData = await response.json()
          console.error('❌ [AUTH] Backend error data:', JSON.stringify(errorData, null, 2))
        } catch (jsonError) {
          console.error('❌ [AUTH] Failed to parse error response as JSON')
          const errorText = await response.text()
          console.error('❌ [AUTH] Raw error response:', errorText)
          throw new Error(`Backend error (${response.status}): ${errorText}`)
        }
        throw new Error(errorData.message || errorData.error || 'Failed to authenticate with backend')
      }

      console.log('🔍 [AUTH] Step 3: Parsing backend response...')
      const data: UserData = await response.json()
      console.log('✅ [AUTH] Backend response parsed successfully')
      console.log('✅ [AUTH] Response UID:', data.uid)
      console.log('✅ [AUTH] Response email:', data.email)
      console.log('✅ [AUTH] Response displayName:', data.displayName)
      console.log('✅ [AUTH] Response photoUrl:', data.photoUrl)
      console.log('✅ [AUTH] Response has idToken?', !!data.idToken)
      console.log('✅ [AUTH] Response has refreshToken?', !!data.refreshToken)
      console.log('✅ [AUTH] Response expiresIn:', data.expiresIn)

      // Step 3: Store tokens and user data
      console.log('🔍 [AUTH] Step 4: Storing tokens and user data in localStorage...')
      userData.value = data
      localStorage.setItem('idToken', data.idToken)
      localStorage.setItem('refreshToken', data.refreshToken)
      localStorage.setItem('userData', JSON.stringify(data))
      console.log('✅ [AUTH] All tokens and user data stored successfully')
      console.log('✅ [AUTH] localStorage idToken length:', localStorage.getItem('idToken')?.length || 0)
      console.log('✅ [AUTH] localStorage refreshToken length:', localStorage.getItem('refreshToken')?.length || 0)
      console.log('✅ [AUTH] localStorage userData length:', localStorage.getItem('userData')?.length || 0)

      // Step 4: Redirect to dashboard
      console.log('🔍 [AUTH] Step 5: Redirecting to dashboard...')
      console.log('🔍 [AUTH] Router instance:', router ? 'exists' : 'NOT exists')
      await router.push('/dashboard')
      console.log('✅ [AUTH] Router.push called successfully')
      console.log('✅ [AUTH] New route should be: /dashboard')
      console.log('=' .repeat(80))
      console.log('✅✅✅ [AUTH] AUTHENTICATION FLOW COMPLETED SUCCESSFULLY! ✅✅✅')
      console.log('=' .repeat(80))

      return data
    } catch (err: any) {
      console.log('=' .repeat(80))
      console.error('❌❌❌ [AUTH] ERROR IN REDIRECT RESULT HANDLER ❌❌❌')
      console.error('❌ [AUTH] Error type:', typeof err)
      console.error('❌ [AUTH] Error name:', err.name)
      console.error('❌ [AUTH] Error message:', err.message)
      console.error('❌ [AUTH] Error stack:', err.stack)
      console.error('❌ [AUTH] Full error object:', err)
      console.log('=' .repeat(80))
      error.value = err.message || 'Failed to complete sign in'
      throw err
    } finally {
      isLoading.value = false
      console.log('🔍 [AUTH] isLoading set to false in finally block')
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
