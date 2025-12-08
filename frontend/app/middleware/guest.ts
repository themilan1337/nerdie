export default defineNuxtRouteMiddleware((to, from) => {
  // Skip middleware on server-side
  if (process.server) return

  const isAuthenticated = () => {
    const idToken = localStorage.getItem('idToken')
    const userData = localStorage.getItem('userData')
    return !!(idToken && userData)
  }

  // Redirect to dashboard if already authenticated
  if (isAuthenticated()) {
    return navigateTo('/dashboard')
  }
})
