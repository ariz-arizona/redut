<script setup lang="ts">
import type { PropType } from 'vue';

import { Swiper, SwiperSlide } from 'swiper/vue';
import type { SwiperOptions } from 'swiper/types';

import 'swiper/css';
import 'swiper/css/effect-fade';

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
    slidesPerView: 4, // Количество видимых слайдов
    loop: true, // Зацикливание
    autoplay: { delay: 5000, disableOnInteraction: false }, // Автопрокрутка
    freeMode: true,
    slidesOffsetBefore: (window.innerWidth - 1024) * 0.5,
    effect: 'fade', 
    spaceBetween: 24,
};

// Ссылка на Swiper для управления (например, пауза/воспроизведение)
const swiperRef = ref(null);
</script>
<template>
    <swiper ref="swiperRef" v-bind="(swiperOptions as any)" class="w-screen">
        <swiper-slide v-for="(slide, index) in props.slides" :key="index">
            <div class="bg-no-repeat bg-cover bg-center h-96 rounded-2xl overflow-hidden flex justify-start align-bottom p-4"
                :style="[{ backgroundImage: `url(${imgBase}/${slide.image})` }]">
                <div class="self-end">
                    <h3 class="font-bold text-2xl">{{ slide.title }}</h3>
                    <p>{{ slide.text }}</p>
                </div>
            </div>
        </swiper-slide>
    </swiper>
</template>