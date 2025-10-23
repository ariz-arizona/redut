<script setup lang="ts">
import type { PropType } from 'vue';

import { Swiper, SwiperSlide } from 'swiper/vue';
import type { SwiperOptions } from 'swiper/types';

import 'swiper/css';
import 'swiper/css/effect-fade';

const props = defineProps({
    'slides': {
        required: true,
        type: Array as PropType<Image[]>,
    },
    'block_id': Number
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
    // effect: 'fade',
    // fadeEffect: { crossFade: true }, // Плавное перекрытие слайдов
    centeredSlides: true, // Центрирование активного слайда
    grabCursor: true, // Включение курсора "рука" для перетаскивания
    allowTouchMove: true, // Разрешение перетаскивания
    enabled: true
};

// Ссылка на Swiper для управления (например, пауза/воспроизведение)
const swiperRef = ref<any>(null);

const onSwiper = (swiper: any) => {
    swiperRef.value = swiper;
    console.log('Swiper initialized:', swiper);
}

// Методы для управления слайдером
const goToPrev = () => {
    console.log('goToPrev clicked, swiperRef:', swiperRef.value);
    if (swiperRef.value) {
        swiperRef.value.slidePrev();
    }
}

const goToNext = () => {
    console.log('goToNext clicked, swiperRef:', swiperRef.value);
    if (swiperRef.value) {
        swiperRef.value.slideNext();
    }
}
const extendedSlides = computed(() => {
    const TARGET_SLIDES = 10
    if (props.slides.length < TARGET_SLIDES) {
        let result = [...props.slides]
        for (let i = 0; i <= ~~(TARGET_SLIDES / props.slides.length); i++) {
            result = result.concat(props.slides)
        }
        return result
    } else {
        return props.slides
    }
})
</script>
<template>
    <div v-if="slides.length" class="relative">
        <swiper :id="`swiper_${block_id}`" :key="`swiper_${block_id}`"
            v-bind="(swiperOptions as any)" class="w-full" @swiper="onSwiper">
            <swiper-slide v-for="(slide, index) in extendedSlides" :key="index" class="w-auto">
                <div class="bg-no-repeat bg-cover bg-center h-[50vh]  flex justify-start align-bottom p-4 mb-12"
                    :style="{ backgroundImage: createBgWithGrad(`${imgBase}/${slide.image}`) }">
                    <NuxtImg :src="`${imgBase}/${slide.image}`" class="invisible" />
                </div>
            </swiper-slide>
        </swiper>
        
        <!-- Кнопки навигации -->
        <div class="absolute top-1/2 -translate-y-1/2 left-4 z-20">
            <button @click="goToPrev" 
                class="w-12 h-12 bg-white/80 hover:bg-white rounded-full flex items-center justify-center shadow-lg transition-all duration-200 hover:scale-110">
                <Icon name="mdi:chevron-left" class="w-6 h-6 text-gray-700" />
            </button>
        </div>
        
        <div class="absolute top-1/2 -translate-y-1/2 right-4 z-20">
            <button @click="goToNext" 
                class="w-12 h-12 bg-white/80 hover:bg-white rounded-full flex items-center justify-center shadow-lg transition-all duration-200 hover:scale-110">
                <Icon name="mdi:chevron-right" class="w-6 h-6 text-gray-700" />
            </button>
        </div>
    </div>
</template>