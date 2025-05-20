<script setup lang="ts">
defineProps<{
    block: Block;
    imgBase: string;
}>();

const lightboxVisible = ref(false);
const indexRef = ref(0)
const openLightbox = () => {
    lightboxVisible.value = true;
};
const closeLightbox = () => {
    lightboxVisible.value = false;
};
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
        <div class="container pt-14 pb-20">
            <div class="grid grid-cols-1 md:grid-cols-2 items-center gap-4">
                <!-- Картинка -->
                <div class="col-span-1" :class="[!block.is_text_right ? 'order-last' : '']">
                    <div v-if="block.images.length">
                        <div class="bg-no-repeat bg-cover bg-center p-4 relative" :style="{
                            backgroundImage: createBgWithGrad(
                                `${imgBase}/${block.images[0].image}`,
                            ),
                            aspectRatio: aspectRatio
                        }" @click="openLightbox">
                            <NuxtImg @load="onImageLoad" :src="`${imgBase}/${block.images[0].image}`" class="invisible" />
                        </div>
                        <vue-easy-lightbox :visible="lightboxVisible"
                            :imgs="block.images.map(el => `${imgBase}/${el.image}`)" :index="indexRef"
                            @hide="closeLightbox" />
                    </div>
                </div>

                <!-- Текст -->
                <div class="col-span-1 flex flex-col gap-4" :class="{ 'justify-end ': !block.is_text_right }">
                    <div class="title" v-if="block.title">
                        {{ block.title }}
                        <span v-if="block.sub_title" class="text-secondary-400">{{ block.sub_title }}</span>
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
