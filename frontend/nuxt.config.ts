import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  ssr: false,
  css: ['./app/assets/css/main.css'],
  modules: ['@nuxt/eslint', '@nuxt/fonts', '@nuxt/image', '@pinia/nuxt'],
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
  runtimeConfig: {
    public: {
      // ingestionServiceUrl: process.env.NUXT_PUBLIC_INGESTION_API_URL || 'https://ingest.nerdie.lol',
      // ragServiceUrl: process.env.NUXT_PUBLIC_RAG_API_URL || 'https://rag.nerdie.lol',
      ingestionServiceUrl: process.env.NUXT_PUBLIC_INGESTION_API_URL || 'http://localhost:8002',
      ragServiceUrl: process.env.NUXT_PUBLIC_RAG_API_URL || 'http://localhost:8001',
    },
  },
});