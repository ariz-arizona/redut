<script setup lang="ts">
interface CategoryItemProps {
    item: PageData; // Данные страницы (новости или категории)
    imgBase: string; // Базовый путь для изображений
}

const props = defineProps<CategoryItemProps>();

// Функция для получения фонового изображения
const getBg = () => {
    return props.item.preview_image || props.item.blocks.find(el => el.type == 'text' && el.images.length > 0)?.images[0].image;
};
</script>

<template>
    <NuxtLink :to="`/${item.slug}`" class="border p-6 xl:p-10 border-secondary-400 flex flex-col gap-4 justify-between"
        :style="{
            backgroundImage: getBg() ? createBgWithGrad(
                `${imgBase}/${getBg()}`,
                'var(--image-overlay-color)',
                '0.9',
                '0.7'
            ) : 'transparent',
        }">
        <div class="w-1/2 xl:w-3/4 basetext leading-8">
            {{ item.title }}
        </div>
        <div class="w-1/2 xl:w-3/4">
            <span v-html="item.preview_text" />
        </div>
        <div class="flex justify-between items-end">
            <div class="text-7xl font-bleu">{{ new Date(item.updated_at).getDate() }}</div>
            <div class="basetext">
                {{ new Date(item.updated_at).toLocaleString('ru', { month: 'long' }) }}
            </div>
        </div>
    </NuxtLink>
</template>