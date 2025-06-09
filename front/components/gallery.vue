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
const swiperRef = ref(null);

const onSwiper = () => {
    // console.log(props)
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
    <div>
        <swiper :id="`swiper_${block_id}`" :key="`swiper_${block_id}`" ref="swiperRef"
            v-bind="(swiperOptions as any)" class="w-full" @swiper="onSwiper">
            <swiper-slide v-for="(slide, index) in extendedSlides" :key="index" class="w-auto">
                <div class="bg-no-repeat bg-cover bg-center h-[50vh]  flex justify-start align-bottom p-4 mb-12"
                    :style="{ backgroundImage: createBgWithGrad(`${imgBase}/${slide.image}`) }">
                    <NuxtImg :src="`${imgBase}/${slide.image}`" class="invisible" />
                </div>
            </swiper-slide>
        </swiper>
    </div>
</template>