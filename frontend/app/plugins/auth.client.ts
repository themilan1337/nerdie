export default defineNuxtPlugin(() => {
  console.log('=' .repeat(80))
  console.log('🔍 [AUTH PLUGIN] Plugin initializing...')
  console.log('🔍 [AUTH PLUGIN] Current URL:', window.location.href)
  console.log('=' .repeat(80))

  const { initAuthListener } = useAuth()

  // Initialize Firebase auth state listener on client side
  console.log('🔍 [AUTH PLUGIN] Calling initAuthListener()...')
  initAuthListener()
  console.log('✅ [AUTH PLUGIN] Auth plugin initialized successfully')
  console.log('=' .repeat(80))
})
