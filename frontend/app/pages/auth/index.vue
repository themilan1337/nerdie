<script setup lang="ts">
import { onMounted } from 'vue'
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Pagination, Autoplay } from 'swiper/modules'
import 'swiper/css'
import 'swiper/css/pagination'

// Add guest middleware to redirect if already authenticated
definePageMeta({
  middleware: 'guest'
})

const modules = [Pagination, Autoplay]

const { signInWithGoogle, isLoading, error, handleRedirectResult } = useAuth()

// Handle redirect result when page loads
onMounted(async () => {
  console.log('=' .repeat(80))
  console.log('🔍 [AUTH PAGE] onMounted called')
  console.log('🔍 [AUTH PAGE] Current URL:', window.location.href)
  console.log('🔍 [AUTH PAGE] Path:', window.location.pathname)
  console.log('🔍 [AUTH PAGE] Search params:', window.location.search)
  console.log('🔍 [AUTH PAGE] Hash:', window.location.hash)
  console.log('=' .repeat(80))

  try {
    console.log('🔍 [AUTH PAGE] Calling handleRedirectResult()...')
    await handleRedirectResult()
    console.log('✅ [AUTH PAGE] handleRedirectResult() completed successfully')
  } catch (err: any) {
    console.error('=' .repeat(80))
    console.error('❌ [AUTH PAGE] Failed to handle redirect!')
    console.error('❌ [AUTH PAGE] Error:', err)
    console.error('❌ [AUTH PAGE] Error message:', err.message)
    console.error('❌ [AUTH PAGE] Error stack:', err.stack)
    console.error('=' .repeat(80))
  }
})

const handleGoogleLogin = async () => {
  console.log('=' .repeat(80))
  console.log('🔍 [AUTH PAGE] handleGoogleLogin called (button clicked)')
  console.log('🔍 [AUTH PAGE] Current time:', new Date().toISOString())
  console.log('=' .repeat(80))

  try {
    console.log('🔍 [AUTH PAGE] Calling signInWithGoogle()...')
    await signInWithGoogle()
    console.log('⚠️ [AUTH PAGE] Code after signInWithGoogle executed')
    console.log('⚠️ [AUTH PAGE] This should not happen if redirect is working')
    // User will be redirected to Google
  } catch (err: any) {
    console.error('=' .repeat(80))
    console.error('❌ [AUTH PAGE] Login failed!')
    console.error('❌ [AUTH PAGE] Error:', err)
    console.error('❌ [AUTH PAGE] Error message:', err.message)
    console.error('=' .repeat(80))
    // Error is already stored in the error ref
  }
}
</script>

<template>
  <div class="min-h-screen w-full bg-white text-gray-900 flex p-2 md:p-3 lg:p-4 gap-8">
    <div class="hidden lg:relative lg:flex lg:w-1/2 xl:w-5/12 rounded-3xl overflow-hidden bg-orange-100/50">
      <div class="absolute top-8 left-8 z-20">
        <h1 class="font-['Questrial'] text-2xl font-bold tracking-wider text-white">Nerdie</h1>
      </div>

      <div class="absolute top-8 right-8 z-20">
        <NuxtLink
          to="/"
          class="bg-white backdrop-blur-md ins px-4 py-2 rounded-full text-sm text-black transition-colors flex items-center gap-1"
        >
          Back to website &rarr;
        </NuxtLink>
      </div>

      <div class="absolute bottom-20 left-0 right-0 z-20 text-center px-10">
        <h2 class="text-4xl font-medium font-['Questrial'] leading-tight text-white">
          Capturing Moments,<br>
          Creating Memories
        </h2>
      </div>

      <Swiper
        :modules="modules"
        :slides-per-view="1"
        :space-between="0"
        :pagination="{ clickable: true }"
        :autoplay="{ delay: 5000, disableOnInteraction: false }"
        loop
        class="h-full w-full"
      >
        <SwiperSlide>
          <div class="h-full w-full relative">
            <img 
              src="/images/12.jpg" 
              alt="Auth Background" 
              class="absolute inset-0 w-full h-full object-cover"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
          </div>
        </SwiperSlide>
        <SwiperSlide>
          <div class="h-full w-full relative">
            <img 
              src="/images/auth-bg.jpg" 
              alt="Auth Background" 
              class="absolute inset-0 w-full h-full object-cover"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
          </div>
        </SwiperSlide>
        <SwiperSlide>
          <div class="h-full w-full relative">
            <img 
              src="/images/auth-bg.jpg" 
              alt="Auth Background" 
              class="absolute inset-0 w-full h-full object-cover"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
          </div>
        </SwiperSlide>
      </Swiper>
    </div>

    <div class="w-full lg:w-1/2 xl:w-7/12 flex items-center justify-center">
      <div class="w-full max-w-md space-y-8">
        <div class="space-y-2 text-center">
          <h2 class="text-2xl md:text-3xl ins font-black tracking-tight text-gray-900">Welcome to Nerdie</h2>
          <p class="">Login with google to continue to Nerdie.</p>
        </div>

        <div class="space-y-5">
          <!-- Error message -->
          <div v-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {{ error }}
          </div>

          <button
            type="button"
            @click="handleGoogleLogin"
            :disabled="isLoading"
            class="w-full bg-black ins hover:opacity-80 transition text-white py-3.5 rounded-full transition-all flex items-center justify-center gap-2 group disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <!-- Loading spinner -->
            <svg v-if="isLoading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>

            <!-- Google icon -->
            <svg v-else class="w-5 h-5" viewBox="0 0 24 24">
              <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
              <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
              <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
              <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
            </svg>

            {{ isLoading ? 'Signing in...' : 'Login with Google' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Custom swiper pagination styles if needed */
:deep(.swiper-pagination-bullet) {
  background: #676767;
  opacity: 0.5;
  width: 24px;
  height: 4px;
  border-radius: 2px;
  transition: all 0.3s ease;
}

:deep(.swiper-pagination-bullet-active) {
  opacity: 1;
  background: #ffffff;
  width: 32px;
}

:deep(.swiper-pagination) {
  bottom: 2rem !important;
}

input:-webkit-autofill,
input:-webkit-autofill:hover, 
input:-webkit-autofill:focus, 
input:-webkit-autofill:active{
    -webkit-box-shadow: 0 0 0 30px #2a2b36 inset !important;
    -webkit-text-fill-color: white !important;
    transition: background-color 5000s ease-in-out 0s;
}
</style>
