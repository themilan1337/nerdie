export default defineNuxtRouteMiddleware((to, from) => {
  console.log('=' .repeat(80))
  console.log('🔍 [AUTH MIDDLEWARE] Middleware called')
  console.log('🔍 [AUTH MIDDLEWARE] From:', from.path)
  console.log('🔍 [AUTH MIDDLEWARE] To:', to.path)
  console.log('🔍 [AUTH MIDDLEWARE] Is server?', process.server)
  console.log('=' .repeat(80))

  // Skip middleware on server-side (SSR is disabled in config, but keeping this for safety)
  if (process.server) {
    console.log('ℹ️ [AUTH MIDDLEWARE] Skipping (server-side)')
    return
  }

  const isAuthenticated = () => {
    try {
      const idToken = localStorage.getItem('idToken')
      const userData = localStorage.getItem('userData')
      console.log('🔍 [AUTH MIDDLEWARE] Checking authentication...')
      console.log('🔍 [AUTH MIDDLEWARE] Has idToken?', !!idToken)
      console.log('🔍 [AUTH MIDDLEWARE] Has userData?', !!userData)

      // Check if tokens exist and userData is valid JSON
      if (!idToken || !userData) {
        console.log('❌ [AUTH MIDDLEWARE] Missing idToken or userData')
        return false
      }

      // Validate userData is valid JSON
      try {
        const parsedUserData = JSON.parse(userData)
        const authenticated = !!(parsedUserData.uid && parsedUserData.email)
        console.log('🔍 [AUTH MIDDLEWARE] Is authenticated?', authenticated)
        return authenticated
      } catch (e) {
        console.log('❌ [AUTH MIDDLEWARE] Invalid userData JSON')
        return false
      }
    } catch (error) {
      console.log('❌ [AUTH MIDDLEWARE] Error checking authentication:', error)
      return false
    }
  }

  // Check if user is authenticated
  if (!isAuthenticated()) {
    console.log('❌ [AUTH MIDDLEWARE] Not authenticated! Redirecting to /auth')
    // Clear invalid tokens
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem('idToken')
      localStorage.removeItem('userData')
      localStorage.removeItem('refreshToken')
    }
    // Redirect to auth page if not authenticated
    return navigateTo('/auth')
  }

  console.log('✅ [AUTH MIDDLEWARE] Authenticated! Allowing navigation')
  console.log('=' .repeat(80))
})
