<script setup lang="ts">
defineProps<{
    block: Block;
    imgBase: string;
}>();
</script>
<template>
    <div :id="block.slug">
        <div class="container pt-4">
            <div class="grid grid-cols-1 md:grid-cols-2 items-center gap-2">
                <!-- Картинка -->
                <div v-if="block.images.length" class="col-span-1" :class="[!block.is_text_right ? 'order-last' : '']">
                    <div class="p-4">
                        <div class="bg-no-repeat bg-cover bg-center p-4 relative pointer-events-none" :style="{
                            backgroundImage: createBgWithGrad(
                                `${imgBase}/${block.images[0].image}`,
                                'rgba(var(--color-primary), 0.5)',
                                'rgba(var(--color-primary), 0.5)'
                            ),
                        }" v-if="block.images.length">
                            <NuxtImg :src="`${imgBase}/${block.images[0].image}`" class="invisible" />
                        </div>
                    </div>
                </div>

                <!-- Текст -->
                <div class="col-span-1">
                    <div class="title mt-16 mb-20" v-if="block.title">
                        {{ block.title }}
                        <span v-if="block.sub_title" class="text-secondary-400">{{ block.sub_title }}</span>
                    </div>
                    <div class="basetext mb-20 prose" v-html="block.content" />
                </div>
            </div>
        </div>
    </div>
</template>
