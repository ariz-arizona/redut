<script setup lang="ts">
interface CategoryItemProps {
    item: PageData; // Данные страницы (новости или категории)
    imgBase: string; // Базовый путь для изображений
}

const props = defineProps<CategoryItemProps>();

// Функция для получения фонового изображения
const getBg = () => {
    return props.item.blocks.find(el => el.type !== 'slider' && el.images.length > 0)?.images[0];
};
</script>

<template>
    <NuxtLink
        :to="`/${item.slug}`"
        class="border p-8 xl:p-16 border-secondary-400 flex flex-col justify-between"
        :style="{
            backgroundImage: getBg() ? createBgWithGrad(
                `${imgBase}/${getBg()}`,
                'rgba(var(--color-primary), 0.5)',
                'rgba(var(--color-primary), 0.5)'
            ) : 'transparent',
        }"
    >
        <div class="w-1/2 xl:w-3/4 basetext leading-8">
            {{ item.title }}
        </div>
        <div class="flex justify-between items-end">
            <div class="text-7xl font-bleu">{{ new Date(item.updated_at).getDate() }}</div>
            <div class="basetext">
                {{ new Date(item.updated_at).toLocaleString('ru', { month: 'long' }) }}
            </div>
        </div>
    </NuxtLink>
</template>