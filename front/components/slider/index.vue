<script setup lang="ts">
import type { PropType } from 'vue';

import { Swiper, SwiperSlide } from 'swiper/vue';
import { Autoplay, Navigation, EffectFade } from 'swiper/modules';

const { setMainSliderRef } = useMainSlider();

import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/effect-fade';
import type { SwiperOptions } from 'swiper/types';

const props = defineProps({
    'slides': {
        requireв: true,
        type: Array as PropType<Image[]>,
    },
    'content': String
})

// Настройки Swiper
const swiperOptions: SwiperOptions = {
    modules: [Autoplay, Navigation, EffectFade], // Подключаем модули
    slidesPerView: 1, // Количество видимых слайдов
    spaceBetween: 0, // Отступ между слайдами
    navigation: true, // Стрелки навигации
    loop: true, // Зацикливание
    effect: 'fade', // Эффект затухания
    fadeEffect: { crossFade: true }, // Плавное перекрытие слайдов
    // autoplay: { delay: 5000, disableOnInteraction: false } // Автопрокрутка
};

// Ссылка на Swiper для управления (например, пауза/воспроизведение)
const swiperRef = ref(null);
</script>
<template>
    <template v-if="props.slides">
        <div class="min-h-[300px] overflow-visible relative" :ref="(setMainSliderRef as any)">
            <swiper ref="swiperRef" v-bind="(swiperOptions as any)" class="h-full overflow-visible" v-if="props.slides.length > 1">
                <swiper-slide v-for="(slide, index) in props.slides" :key="index" class="h-auto">
                    <SliderItem :slide="slide" />
                </swiper-slide>
            </swiper>
            <SliderItem :slide="props.slides[0]" v-else />
        </div>
    </template>
</template>
<style>
.swiper-button-next,
.swiper-button-prev {
    @apply text-secondary-500 after:text-6xl flex items-center;
}

.swiper-button-next {
    @apply after:content-['next']
}

.swiper-button-prev {
    @apply after:content-['prev']
}
</style>