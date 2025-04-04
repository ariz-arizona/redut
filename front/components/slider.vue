<script setup lang="ts">
import type { PropType } from 'vue';

import { Swiper, SwiperSlide } from 'swiper/vue';
import { Autoplay, Navigation, EffectFade } from 'swiper/modules';

import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/effect-fade';
import type { SwiperOptions } from 'swiper/types';

const props = defineProps({
    'slides': {
        requireв: true,
        type: Array as PropType<Image[]>,
    }
})

const config = useRuntimeConfig()
const imgBase = config.public.imgBase

// Настройки Swiper
const swiperOptions: SwiperOptions = {
    modules: [Autoplay, Navigation, EffectFade], // Подключаем модули
    slidesPerView: 1, // Количество видимых слайдов
    spaceBetween: 0, // Отступ между слайдами
    navigation: true, // Стрелки навигации
    loop: true, // Зацикливание
    effect: 'fade', // Эффект затухания
    fadeEffect: { crossFade: true }, // Плавное перекрытие слайдов
    autoplay: { delay: 5000, disableOnInteraction: false } // Автопрокрутка
};

// Ссылка на Swiper для управления (например, пауза/воспроизведение)
const swiperRef = ref(null);
</script>
<template>
    <div class="h-[calc(100vh-8rem)] min-h-[300px] overflow-hidden relative">
        <swiper ref="swiperRef" v-bind="swiperOptions as any" class="h-full">
            <swiper-slide v-for="(slide, index) in props.slides" :key="index">
                <div class="h-full bg-[100%_auto] bg-bottom" :style="[{ backgroundImage: `url(${imgBase}/${slide.image})` }]">
                    <div
                        class="container m-auto select-none absolute text-white text-2xl bottom-2 right-2 left-2 text-left font-normal">
                        <h3>{{ slide.title }}</h3>
                        <p>{{ slide.alt_text }}</p>
                    </div>
                </div>
            </swiper-slide>
        </swiper>
    </div>
</template>
<style>
.swiper-button-next,
.swiper-button-prev {
    @apply rounded-full size-10 text-white after:text-2xl border-white border-2 flex items-center;
}

.swiper-button-next {
    @apply after:content-['next']
}

.swiper-button-prev {
    @apply after:content-['prev']
}

@media(min-width:1024px) {
    .swiper-button-next,
    .swiper-button-prev {
        @apply right-1/2 left-[auto] top-[auto] bottom-4;
    }

    .swiper-button-next {
        @apply translate-x-[calc((100%_-_1024px)*_-0.5)]
    }

    .swiper-button-prev {
        @apply translate-x-[calc((100%_-_1024px)*_-0.5_-3rem)]
    }
}
</style>