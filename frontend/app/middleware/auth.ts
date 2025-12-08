export default defineNuxtRouteMiddleware((to, from) => {
  // Skip middleware on server-side
  if (process.server) return

  const isAuthenticated = () => {
    const idToken = localStorage.getItem('idToken')
    const userData = localStorage.getItem('userData')
    return !!(idToken && userData)
  }

  // Check if user is authenticated
  if (!isAuthenticated()) {
    // Redirect to auth page if not authenticated
    return navigateTo('/auth')
  }
})
