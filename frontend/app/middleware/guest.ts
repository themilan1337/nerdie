export default defineNuxtRouteMiddleware((to, from) => {
  console.log('=' .repeat(80))
  console.log('🔍 [GUEST MIDDLEWARE] Middleware called')
  console.log('🔍 [GUEST MIDDLEWARE] From:', from.path)
  console.log('🔍 [GUEST MIDDLEWARE] To:', to.path)
  console.log('🔍 [GUEST MIDDLEWARE] Is server?', process.server)
  console.log('=' .repeat(80))

  // Skip middleware on server-side
  if (process.server) {
    console.log('ℹ️ [GUEST MIDDLEWARE] Skipping (server-side)')
    return
  }

  const isAuthenticated = () => {
    try {
      const idToken = localStorage.getItem('idToken')
      const userData = localStorage.getItem('userData')
      console.log('🔍 [GUEST MIDDLEWARE] Checking authentication...')
      console.log('🔍 [GUEST MIDDLEWARE] Has idToken?', !!idToken)
      console.log('🔍 [GUEST MIDDLEWARE] Has userData?', !!userData)

      // Check if tokens exist and userData is valid JSON
      if (!idToken || !userData) {
        console.log('❌ [GUEST MIDDLEWARE] Missing idToken or userData')
        return false
      }

      // Validate userData is valid JSON
      try {
        const parsedUserData = JSON.parse(userData)
        const authenticated = !!(parsedUserData.uid && parsedUserData.email)
        console.log('🔍 [GUEST MIDDLEWARE] Is authenticated?', authenticated)
        return authenticated
      } catch (e) {
        console.log('❌ [GUEST MIDDLEWARE] Invalid userData JSON')
        return false
      }
    } catch (error) {
      console.log('❌ [GUEST MIDDLEWARE] Error checking authentication:', error)
      return false
    }
  }

  // Redirect to dashboard if already authenticated
  if (isAuthenticated()) {
    console.log('✅ [GUEST MIDDLEWARE] Already authenticated! Redirecting to /dashboard')
    return navigateTo('/dashboard')
  }

  console.log('ℹ️ [GUEST MIDDLEWARE] Not authenticated, allowing access to guest page')
  console.log('=' .repeat(80))
})
