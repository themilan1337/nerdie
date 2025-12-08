export default defineNuxtRouteMiddleware((to, from) => {
  console.log('=' .repeat(80))
  console.log('🔍 [AUTH MIDDLEWARE] Middleware called')
  console.log('🔍 [AUTH MIDDLEWARE] From:', from.path)
  console.log('🔍 [AUTH MIDDLEWARE] To:', to.path)
  console.log('🔍 [AUTH MIDDLEWARE] Is server?', process.server)
  console.log('=' .repeat(80))

  // Skip middleware on server-side
  if (process.server) {
    console.log('ℹ️ [AUTH MIDDLEWARE] Skipping (server-side)')
    return
  }

  const isAuthenticated = () => {
    const idToken = localStorage.getItem('idToken')
    const userData = localStorage.getItem('userData')
    console.log('🔍 [AUTH MIDDLEWARE] Checking authentication...')
    console.log('🔍 [AUTH MIDDLEWARE] Has idToken?', !!idToken)
    console.log('🔍 [AUTH MIDDLEWARE] Has userData?', !!userData)
    const authenticated = !!(idToken && userData)
    console.log('🔍 [AUTH MIDDLEWARE] Is authenticated?', authenticated)
    return authenticated
  }

  // Check if user is authenticated
  if (!isAuthenticated()) {
    console.log('❌ [AUTH MIDDLEWARE] Not authenticated! Redirecting to /auth')
    // Redirect to auth page if not authenticated
    return navigateTo('/auth')
  }

  console.log('✅ [AUTH MIDDLEWARE] Authenticated! Allowing navigation')
  console.log('=' .repeat(80))
})
