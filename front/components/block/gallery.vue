<script setup lang="ts">
import Gallery from '../gallery.vue';

defineProps<{
    block: Block;
}>();
</script>
<template>
    <BlockWrapper :block="block" class="pt-16 relative gallery" :class="[{
        'pb-0 -mb-36': block.link || block.external_link
    }]">
        <div class="relative overflow-hidden">
            <div class="text-[50vmin] text-center text-secondary-200 font-wonder pointer-events-none z-10 
                absolute left-0 right-0 top-1/2 -translate-y-1/2 leading-[0.25]" v-if="block.title">
                {{ block.title }}
            </div>
            <Gallery :slides="block.images" />
        </div>
        <template v-if="block.link || block.external_link">
            <div class="relative -translate-y-1/2 z-10 flex justify-center w-full">
                <NuxtLink :to="((block.link || block.external_link) as string)" :external="!!block.external_link"
                    class="size-36 p-4 leadbtn">
                    <span class="leading-4">{{ block.btn_title || 'Читать далее' }}</span>
                </NuxtLink>
            </div>
        </template>
    </BlockWrapper>
</template>
<style lang="css" scoped>
.gallery+* {
    position: relative;
    padding-top: 4rem;
}
</style>