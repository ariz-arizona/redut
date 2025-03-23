// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  ssr: false,
  modules: [
    '@nuxt/icon',
    '@nuxt/image',
    '@nuxtjs/tailwindcss',
    '@nuxtjs/robots'
  ],
  site: { indexable: false },
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
})