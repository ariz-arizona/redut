<script setup lang="ts">
defineProps<{
    block: Block;
    imgBase: string;
}>();
</script>
<template>
    <div :id="block.slug" class="overflow-hidden">
        <div class="container pt-4">
            <div class="relative">
                <h3 class="text-4xl md:text-[6.5vh] font-bleu text-center w-full md:w-3/4 m-auto uppercase leading-tight"
                    v-if="block.title" v-html="block.title"></h3>
                <span v-if="block.sub_title" class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 
                    text-secondary-500/50 font-wonder text-[12vw] pointer-events-none">
                    {{ block.sub_title }}
                </span>
            </div>
            <div class="relative flex justify-center w-full mt-20" v-if="block.link || block.external_link">
                <NuxtLink :to="(block.link || block.external_link) as string" :external="!!block.external_link"
                    class="leadbtn p-8">
                    <span class="leading-4">{{ block.btn_title || 'Читать далее' }}</span>
                </NuxtLink>
            </div>
        </div>
        <div class="bg-no-repeat bg-cover bg-center h-[50vh] p-4 -z-10 relative pointer-events-none"
            :class="[{ '-mt-[25vh]': block.link || block.external_link }]" :style="{
                backgroundImage: createBgWithGrad(
                    `${imgBase}/${block.images[0].image}`,
                    'rgba(var(--color-primary), 1)',
                    'rgba(var(--color-primary), 0.75)'
                ),
            }" v-if="block.images.length">
            <NuxtImg :src="`${imgBase}/${block.images[0].image}`" class="invisible" />
        </div>
    </div>
</template>
