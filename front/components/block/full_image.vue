<script setup lang="ts">
const props = defineProps<{
    block: Block;
    imgBase: string;
}>();
const aspectRatio = ref('auto')
const onImageLoad = (event: Event) => {
    const img = event.target as HTMLImageElement
    if (img) {
        aspectRatio.value = (img.naturalWidth / img.naturalHeight).toString()
    }
}
const img_bg = props.block.images[0]
const img_add = props.block.images[1]
</script>
<template>
    <BlockWrapper :block="block">
        <div class="bg-no-repeat bg-cover min-h-[50vh] max-h-[83vh] w-full p-4 relative pointer-events-none"
            :class="[{ '-mt-[33vh]': block.link || block.external_link }]" :style="{
                backgroundImage: img_bg ? createBgWithGrad(
                    `${imgBase}/${img_bg.image}`,
                    'var(--image-overlay-color)',
                    '0',
                    '0',
                ) : '',
                aspectRatio: aspectRatio,
                backgroundPositionY: '75%'
            }">
            <NuxtImg @load="onImageLoad" :src="`${imgBase}/${block.images[0].image}`" class="invisible hidden" />

            <div class="container pt-16 z-10 relative h-full flex items-center bg-no-repeat bg-left-bottom" :style="{
                backgroundImage: img_add ? createBgWithGrad(
                    `${imgBase}/${img_add.image}`,
                    'var(--image-overlay-color)',
                    '0',
                    '0',
                ) : ''
            }">
                <div class="grid grid-cols-6 gap-y-10">
                    <div class="col-span-full xl:col-span-3 xl:col-start-3">
                        <div class="text-7xl md:text-[6.5vh] font-bleu uppercase leading-tight">
                            {{ block.title }}
                        </div>
                    </div>
                    <div class="col-span-full xl:col-span-2 xl:col-start-5">
                        <span v-html="block.content" />
                    </div>
                </div>
            </div>
        </div>
    </BlockWrapper>
</template>