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

const config = useRuntimeConfig()
const imgBase = config.public.imgBase
</script>

<template>
  <div class="h-full bg-[100%_auto] bg-bottom" :style="{ backgroundImage: `url(${imgBase}/${slide.image})` }">
    <div class="absolute bottom-2 right-2 left-2 text-left">
      <div class="container m-auto">
        <div class="max-w-[75%] select-none leading-none relative">
          <h3 class="text-[12vmin] font-bleu" v-html="slide.title"></h3>
          <p v-if="slide.alt_text"
            class="font-wonder text-[24vmin] text-provincial-pink-200 absolute right-0 top-1/4 left-3/4">
            {{ slide.alt_text }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>