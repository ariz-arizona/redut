<script setup lang="ts">
import { useImagesData } from '@/composables/useImagesData'

const props = defineProps<{
    block: Block
    imgBase: string
}>()

// Получаем изображения (предположим, что это хук или стор)
const { items: images } = useImagesData()

// Lightbox
const lightboxVisible = ref(false)
const indexRef = computed(() => {
    return images.value.findIndex(el => el.id === props.block.images[0]?.id)
})

const openLightbox = () => {
    lightboxVisible.value = true
}

const closeLightbox = () => {
    lightboxVisible.value = false
}

// Для расчёта соотношения сторон картинки
const aspectRatio = ref('auto')
const onImageLoad = (event: Event) => {
    const img = event.target as HTMLImageElement
    if (img) {
        aspectRatio.value = (img.naturalWidth / img.naturalHeight).toString()
    }
}
</script>

<template>
    <BlockWrapper :block="block">
        <!-- Lightbox -->
        <vue-easy-lightbox :visible="lightboxVisible" :imgs="images.map(el => `${imgBase}/${el.image}`)"
            :index="indexRef" @hide="closeLightbox" />

        <!-- Основной контейнер блока -->
        <div class="container pt-14 pb-20">
            <div class="grid grid-cols-1 md:grid-cols-2 items-center gap-4 md:gap-x-16">
                <!-- Слот для картинки -->
                <div class="col-span-1" :class="[!block.is_text_right ? 'order-last' : '']">
                    <slot name="image">
                        <div v-if="block.images.length" class="relative">
                            <div class="bg-no-repeat bg-cover bg-center p-4 cursor-pointer" :style="{
                                backgroundImage: createBgWithGrad(
                                    `${imgBase}/${block.images[0].image}`,
                                ), aspectRatio: aspectRatio
                            }" @click="openLightbox">
                                <img @load="onImageLoad" :src="`${imgBase}/${block.images[0].image}`" class="invisible"
                                    alt="" />
                            </div>
                        </div>
                    </slot>
                </div>

                <!-- Текстовая часть -->
                <div class="col-span-1 flex flex-col gap-4" :class="{ 'justify-end': !block.is_text_right }">
                    <div class="title" v-if="block.title">
                        {{ block.title }}
                        <span v-if="block.sub_title" class="text-secondary-400">
                            {{ block.sub_title }}
                        </span>
                    </div>
                    <div class="prose" :class="{
                        basetext: block.is_text_styled,
                        'leading-normal text-lg': !block.is_text_styled
                    }" v-html="block.content" />
                </div>
            </div>
        </div>
    </BlockWrapper>
</template>