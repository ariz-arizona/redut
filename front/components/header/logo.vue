<script setup lang="ts">
// Определяем типы для пропсов
const props = defineProps<{
    logo?: string | null; // Логотип (необязательный пропс)
}>();

const config = useRuntimeConfig()
const imgBase = config.public.imgBase
</script>

<template>
    <div class="flex justify-center items-center gap-2 overflow-hidden p-4 h-[inherit]">
        <NuxtLink to="/" class="contents">
            <img v-if="props.logo" :src="`${imgBase}/${props.logo}`" alt="Логотип" class="w-full h-full object-contain" />
            <Icon v-else name="mdi:city-variant" class="w-full h-full" />
        </NuxtLink>
    </div>
</template>