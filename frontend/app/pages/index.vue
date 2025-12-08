<script setup lang="ts">
import { ref } from 'vue'
import { Icon } from '@iconify/vue'

definePageMeta({
  layout: false
})

const features = [
  {
    title: 'Intelligent RAG',
    description: 'Upload your documents and chat with them instantly using advanced vector search.',
    icon: 'hugeicons:database-01'
  },
  {
    title: 'Smart Analytics',
    description: 'Get deep insights into your data with our powerful analytics engine.',
    icon: 'hugeicons:analytics-up'
  },
  {
    title: 'Secure & Private',
    description: 'Enterprise-grade security ensuring your data remains yours alone.',
    icon: 'hugeicons:shield-02'
  },
  {
    title: 'Real-time Chat',
    description: 'Seamless conversation interface with low latency and high accuracy.',
    icon: 'hugeicons:bubble-chat'
  }
]
</script>

<template>
  <div class="min-h-screen bg-zinc-50 font-sans selection:bg-black selection:text-white">
    <!-- Navbar -->
    <nav class="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-xl border-b border-zinc-200/50">
      <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div class="flex items-center gap-2">
           <h1 class="font-['Questrial'] text-2xl font-bold tracking-tight text-zinc-900">nerdie.</h1>
        </div>
        <div class="flex items-center gap-6">
          <NuxtLink to="/auth" class="text-sm font-medium text-zinc-500 hover:text-zinc-900 transition-colors hidden sm:block">
            Sign In
          </NuxtLink>
          <NuxtLink 
            to="/auth" 
            class="px-4 py-2 bg-zinc-900 text-white text-sm font-medium rounded-full hover:bg-zinc-700 transition"
          >
            Get Started
          </NuxtLink>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="relative pt-32 pb-20 overflow-hidden">
      <!-- Background Elements -->
      <div class="absolute top-0 inset-x-0 h-full bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-zinc-100 via-zinc-50 to-zinc-50 -z-10"></div>
      
      <div class="max-w-7xl mx-auto px-6 relative z-10">
        <div class="text-center max-w-3xl mx-auto mb-16">
          <h1 class="text-5xl sm:text-7xl font-['Questrial'] font-bold text-zinc-900 tracking-tight mb-6 leading-[1.1]">
            Your data, <br/>
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-zinc-900 to-zinc-500">intelligently organized.</span>
          </h1>
          <p class="text-lg text-zinc-500 leading-relaxed mb-8 max-w-2xl mx-auto">
            Experience the power of RAG technology in a beautiful, dashboard-style interface. 
            Upload documents, chat with AI, and get instant insights.
          </p>
          <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
            <NuxtLink 
              to="/auth" 
              class="w-full sm:w-auto px-8 py-3.5 bg-zinc-900 text-white font-medium rounded-full hover:bg-black transition-all flex items-center justify-center gap-2"
            >
              Start Free Trial
              <Icon icon="hugeicons:arrow-right-01" class="w-4 h-4" />
            </NuxtLink>
            <button class="w-full sm:w-auto px-8 py-3.5 bg-white border border-zinc-200 text-zinc-700 font-medium rounded-full hover:bg-zinc-50 transition-all">
              View Documentation
            </button>
          </div>
        </div>

        <!-- Dashboard Preview (Mock UI) -->
        <div class="relative max-w-5xl mx-auto mt-12 perspective-container">
          <div class="glass-panel border border-zinc-200/50 bg-white/50 backdrop-blur-xl rounded-[2.5rem] p-4 shadow-[0_50px_100px_-20px_rgba(0,0,0,0.12)] transform rotate-x-12-custom transition-transform duration-700 hover:rotate-x-0">
            <!-- Mock Window Controls -->
            <div class="flex items-center gap-2 mb-4 px-4">
              <div class="w-3 h-3 rounded-full bg-red-400"></div>
              <div class="w-3 h-3 rounded-full bg-amber-400"></div>
              <div class="w-3 h-3 rounded-full bg-green-400"></div>
            </div>

            <!-- Mock Dashboard Layout -->
            <div class="flex h-[500px] bg-zinc-50 rounded-3xl overflow-hidden border border-zinc-200/50">
              <!-- Sidebar -->
              <div class="w-64 bg-white border-r border-zinc-200/50 p-6 flex flex-col hidden md:flex">
                <div class="flex items-center gap-3 mb-8">
                  <div class="h-8 w-8 bg-zinc-900 rounded-lg"></div>
                  <div class="h-4 w-20 bg-zinc-200 rounded"></div>
                </div>
                <div class="space-y-3">
                  <div class="h-10 w-full bg-zinc-100 rounded-xl"></div>
                  <div class="h-10 w-full bg-white rounded-xl"></div>
                  <div class="h-10 w-full bg-white rounded-xl"></div>
                  <div class="h-10 w-full bg-white rounded-xl"></div>
                </div>
                <div class="mt-auto">
                    <div class="flex items-center gap-3">
                        <div class="h-10 w-10 rounded-full bg-zinc-200"></div>
                        <div class="flex flex-col gap-1">
                             <div class="h-3 w-24 bg-zinc-200 rounded"></div>
                             <div class="h-2 w-16 bg-zinc-100 rounded"></div>
                        </div>
                    </div>
                </div>
              </div>

              <!-- Main Area -->
              <div class="flex-1 p-6 md:p-8 overflow-hidden relative">
                 <!-- Header -->
                 <div class="flex justify-between items-center mb-8">
                     <div>
                         <div class="h-8 w-48 bg-zinc-200 rounded-lg mb-2"></div>
                         <div class="h-4 w-32 bg-zinc-100 rounded"></div>
                     </div>
                     <div class="flex gap-3">
                         <div class="h-10 w-10 rounded-full bg-white border border-zinc-100"></div>
                         <div class="h-10 w-10 rounded-full bg-white border border-zinc-100"></div>
                     </div>
                 </div>

                 <!-- Grid -->
                 <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                     <div class="bg-white p-4 rounded-2xl border border-zinc-100 shadow-sm h-32"></div>
                     <div class="bg-white p-4 rounded-2xl border border-zinc-100 shadow-sm h-32"></div>
                     <div class="bg-white p-4 rounded-2xl border border-zinc-100 shadow-sm h-32"></div>
                     <div class="bg-white p-4 rounded-2xl border border-zinc-100 shadow-sm h-32"></div>
                 </div>
                 
                 <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                     <div class="lg:col-span-2 h-64 bg-white rounded-3xl border border-zinc-100 shadow-sm"></div>
                     <div class="h-64 bg-white rounded-3xl border border-zinc-100 shadow-sm"></div>
                 </div>

                 <!-- Floating Chat Bubble (Visual Polish) -->
                 <div class="absolute bottom-8 right-8 bg-zinc-900 text-white px-4 py-3 rounded-2xl rounded-tr-none shadow-xl flex items-center gap-3 animate-bounce">
                     <Icon icon="hugeicons:bubble-chat-spark-01" class="w-5 h-5" />
                     <span class="text-sm font-medium">Hey, how can I help you?</span>
                 </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Grid -->
    <section class="py-24 bg-white">
      <div class="max-w-7xl mx-auto px-6">
        <div class="text-center mb-16">
          <h2 class="text-3xl font-['Questrial'] text-zinc-900 mb-4">Why nerdie. is different</h2>
          <p class="text-zinc-500 max-w-2xl mx-auto">Built with precision and designed for efficiency. Every pixel is crafted to provide the best possible experience.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div 
            v-for="feature in features" 
            :key="feature.title"
            class="group p-8 rounded-[2rem] bg-zinc-50 hover:bg-zinc-100 transition-colors duration-300"
          >
            <div class="w-14 h-14 bg-white rounded-2xl flex items-center justify-center mb-6 shadow-sm group-hover:scale-110 transition-transform duration-300">
              <Icon :icon="feature.icon" class="w-6 h-6 text-zinc-900" />
            </div>
            <h3 class="text-xl font-medium text-zinc-900 mb-3">{{ feature.title }}</h3>
            <p class="text-sm text-zinc-500 leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-zinc-50 border-t border-zinc-200 py-12">
      <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="flex items-center gap-2">
            <h1 class="font-['Questrial'] text-xl font-bold tracking-tight text-zinc-900">nerdie.</h1>
        </div>
        <div class="flex items-center gap-8 text-sm text-zinc-500">
            <a href="#" class="hover:text-zinc-900 transition-colors">Privacy</a>
            <a href="#" class="hover:text-zinc-900 transition-colors">Terms</a>
            <a href="#" class="hover:text-zinc-900 transition-colors">Twitter</a>
            <a href="#" class="hover:text-zinc-900 transition-colors">GitHub</a>
        </div>
        <p class="text-sm text-zinc-400">© {{ new Date().getFullYear() }} nerdie inc.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.glass-panel {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(20px);
}
.perspective-container {
    perspective: 1200px;
}
.rotate-x-12-custom {
    transform: rotateX(12deg);
}
</style>