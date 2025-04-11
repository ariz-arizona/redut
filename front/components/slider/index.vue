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
    }
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
    autoplay: { delay: 5000, disableOnInteraction: false } // Автопрокрутка
};

// Ссылка на Swiper для управления (например, пауза/воспроизведение)
const swiperRef = ref(null);
</script>
<template>
    <template v-if="props.slides">
        <div class="h-[calc(100vh-8rem)] min-h-[300px] overflow-visible relative" :ref="(setMainSliderRef as any)">
            <swiper ref="swiperRef" v-bind="(swiperOptions as any)" class="h-full" v-if="props.slides.length > 1">
                <swiper-slide v-for="(slide, index) in props.slides" :key="index">
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