<script setup lang="ts">
// Пропсы для компонента
const props = defineProps({
  slide: {
    type: Object,
    required: true,
    default: () => ({
      image: '', // Путь к изображению
      title: '', // Заголовок слайда
      alt_text: '', // Дополнительный текст
    }),
  },
});

const { settings } = useSiteSettings()
const config = useRuntimeConfig()
const imgBase = config.public.imgBase
</script>

<template>
  <div class="h-full bg-cover relative" :style="{ backgroundImage: createBgWithGrad(`${imgBase}/${slide.image}`) }">
    <div class="absolute bottom-2 right-2 left-2 text-left">
      <div class="container m-auto">
        <div class="max-w-[66%] select-none leading-none relative">
          <h3 class="text-[5vw] font-bleu" v-html="slide.title"></h3>
          <p v-if="slide.alt_text"
            class="font-wonder text-[8vw] text-secondary-200 absolute right-0 top-1/4 left-3/4">
            {{ slide.alt_text }}
          </p>
        </div>
      </div>
    </div>
    <div class="container relative grid grid-cols-1 md:grid-cols-3 h-full items-center">
      <div class="col-span-1 col-start-3 p-8 overflow-hidden bg-midnight-950 mt-48 mb-4">
        <div class="text-center">
          <span class="size-24">
            <HeaderLogo :logo="settings?.logo" />
          </span>
          <div class="font-bleu text-3xl text-secondary-400">
            {{ settings?.name }}
          </div>
        </div>
        <div class="prose basetext">
          <span v-html="slide.text_rendered" />
        </div>
        <div class="text-center">

          <NuxtLink :to="slide.external_link || slide.link" :target="slide.external_link ? '_blank' : '_self'"
            :external="slide.external_link" v-if="slide.external_link || slide.link"
            class="menubtn bg-secondary-500 hover:bg-secondary-700">
            {{ slide.btn_title || 'Узнать больше' }}
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>