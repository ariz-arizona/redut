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
    slidesPerView: 'auto', // Автоматическая ширина слайдов
    spaceBetween: 48, // Расстояние между слайдами
    slidesOffsetBefore: -48,
    loop: true, // Бесконечная прокрутка
    autoplay: { 
        delay: 5000, // Задержка между переключениями (в миллисекундах)
        disableOnInteraction: false, // Продолжать автопрокрутку даже после взаимодействия
    },
    freeMode: true,
    effect: 'fade',
    fadeEffect: { crossFade: true }, // Плавное перекрытие слайдов
    centeredSlides: true, // Центрирование активного слайда
    grabCursor: true, // Включение курсора "рука" для перетаскивания
    allowTouchMove: true, // Разрешение перетаскивания
};

// Ссылка на Swiper для управления (например, пауза/воспроизведение)
const swiperRef = ref(null);
</script>
<template>
    <swiper ref="swiperRef" v-bind="(swiperOptions as any)" class="w-full">
        <swiper-slide v-for="(slide, index) in props.slides" :key="index" class="w-auto">
            <div class="bg-no-repeat bg-cover bg-center h-[50vh] flex justify-start align-bottom p-4"
                :style="[{ backgroundImage: `url(${imgBase}/${slide.image})` }]">
                <NuxtImg :src="`${imgBase}/${slide.image}`" class="invisible" />
            </div>
        </swiper-slide>
    </swiper>
</template>