import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  ssr: false,
  css: ['./app/assets/css/main.css'],
  modules: ['@nuxt/eslint', '@nuxt/fonts', '@nuxt/image'],
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
  runtimeConfig: {
    public: {
      ingestionApiUrl: process.env.NUXT_PUBLIC_INGESTION_API_URL || 'https://ingest.nerdie.lol',
    },
  },
});