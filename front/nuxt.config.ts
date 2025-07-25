// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  ssr: false,
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxt/icon',
    '@nuxt/image',
  ],
  // site: { indexable: false },
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost', // can be overridden by NUXT_PUBLIC_API_BASE environment variable
      imgBase: 'http://localhost', // can be overridden by NUXT_PUBLIC_IMG_BASE environment variable
    }
  },
  icon: {
    localApiEndpoint: "/fapi/_nuxt_icon",
    serverBundle: {
      collections: ['hugeicons', 'carbon'],
    }
  },
  nitro: {
    prerender: {
      crawlLinks: false
    }
  },
  tailwindcss: {
    exposeConfig: true,
    config: {
      content: [
        "./components/**/*.{js,vue,ts}",
        "./layouts/**/*.vue",
        "./pages/**/*.vue",
        "./plugins/**/*.{js,ts}",
        "./nuxt.config.{js,ts}",
        "./error.vue",
      ]
    }
  }
})