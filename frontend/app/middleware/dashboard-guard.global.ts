/**
 * Global middleware to protect all /dashboard routes
 * This provides an additional layer of security in case individual pages
 * forget to include the auth middleware
 */
export default defineNuxtRouteMiddleware((to, from) => {
  // Only check dashboard routes
  if (!to.path.startsWith('/dashboard')) {
    return
  }

  console.log('🛡️ [DASHBOARD GUARD] Checking access to:', to.path)

  // Skip on server-side (SSR is disabled in config)
  if (process.server) {
    console.log('🛡️ [DASHBOARD GUARD] Skipping (server-side)')
    return
  }

  const isAuthenticated = () => {
    try {
      const idToken = localStorage.getItem('idToken')
      const userData = localStorage.getItem('userData')

      if (!idToken || !userData) {
        return false
      }

      // Validate userData is valid JSON with required fields
      try {
        const parsedUserData = JSON.parse(userData)
        return !!(parsedUserData.uid && parsedUserData.email)
      } catch {
        return false
      }
    } catch {
      return false
    }
  }

  // Block access if not authenticated
  if (!isAuthenticated()) {
    console.log('❌ [DASHBOARD GUARD] Access denied! Redirecting to /auth')

    // Clear invalid tokens
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem('idToken')
      localStorage.removeItem('userData')
      localStorage.removeItem('refreshToken')
    }

    return navigateTo('/auth')
  }

  console.log('✅ [DASHBOARD GUARD] Access granted to:', to.path)
})
