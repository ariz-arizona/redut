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
  <div class="h-full min-h-[50vh] bg-cover relative"
    :style="{ backgroundImage: createBgWithGrad(`${imgBase}/${slide.image}`) }">
    <div class="absolute bottom-2 right-2 left-2 text-left">
      <div class="container m-auto">
        <div class="max-w-full md:max-w-[85%] select-none leading-none relative inline-block">
          <h3 class="text-5xl sm:text-[7rem] font-bleu" v-html="slide.title"></h3>
          <p v-if="slide.alt_text" class="text-9xl sm:text-[16rem] font-wonder 
            text-secondary-200 absolute w-full lg:top-1/2 -translate-y-1/2 left-1/4 lg:left-3/4">
            {{ slide.alt_text }}
          </p>
        </div>
      </div>
    </div>
    <div class="container relative hidden lg:grid grid-cols-1 md:grid-cols-4 h-full items-center">
      <div class="col-span-1 col-start-4 p-6 overflow-hidden bg-midnight-950 mt-48 mb-4">
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