export default defineNuxtPlugin(() => {
  const { initAuthListener } = useAuth()

  // Initialize Firebase auth state listener on client side
  initAuthListener()
})
