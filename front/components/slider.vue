<script setup lang="ts">
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Pagination, Autoplay, Navigation, EffectFade } from 'swiper/modules';

import 'swiper/css';
import 'swiper/css/pagination';
import 'swiper/css/navigation';
import 'swiper/css/effect-fade';
import type { SwiperOptions } from 'swiper/types';

// Массив слайдов
const slides = [
    {
        image: '/slider/all-bong.jpg',
        title: 'Заголовок 1',
        description: 'Описание первого слайда.'
    },
    {
        image: '/slider/danist-soh.jpg',
        title: 'Заголовок 2',
        description: 'Описание второго слайда.'
    },
    {
        image: '/slider/luke-van.jpg',
        title: 'Заголовок 3',
        description: 'Описание третьего слайда.'
    }
];

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
    <div class="max-h-[50vh] h-[300px] overflow-hidden relative">
        <swiper ref="swiperRef" v-bind="swiperOptions as any" class="h-full">
            <swiper-slide v-for="(slide, index) in slides" :key="index">
                <div class="h-full bg-[100%_auto] bg-bottom" :style="[{ backgroundImage: `url(${slide.image})` }]">
                    <div
                        class="container m-auto select-none absolute text-white text-2xl bottom-2 right-2 left-2 text-left font-normal">
                        <h3>{{ slide.title }}</h3>
                        <p>{{ slide.description }}</p>
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