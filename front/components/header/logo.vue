<script setup lang="ts">
// Определяем типы для пропсов
const props = defineProps<{
    logo?: string | null; // Логотип (необязательный пропс)
}>();
</script>

<template>
    <div class="flex justify-center items-center gap-2">
        <!-- Общий контейнер для логотипа или иконки -->
        <span class="size-14">
            <img v-if="props.logo" :src="props.logo" alt="Логотип" class="w-full h-full object-contain" />
            <Icon v-else name="mdi:city-variant" class="w-full h-full" />
        </span>
        <span class="uppercase text-4xl font-black leading-3">Редут</span>
    </div>
</template>