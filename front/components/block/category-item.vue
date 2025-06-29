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
// Компьютед поля для отображения заголовка и подзаголовка
const displayTitle = computed(() => {
    return props.item.cat_main
})

const displaySubtitle = computed(() => {
    return props.item.cat_sub || new Date(props.item.updated_at).toLocaleString('ru', { month: 'long' })
})

const displayDay = computed(() => {
    return new Date(props.item.updated_at).getDate().toString()
})
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
        <div class="w-full basetext leading-8">
            {{ item.title }}
        </div>
        <div class="w-full">
            <span v-html="item.preview_text" />
        </div>
        <div class="flex justify-between items-end">
            <div class="text-7xl font-bleu">
                {{ displayTitle || displayDay }}
            </div>
            <div class="basetext text-right">
                {{ displaySubtitle }}
            </div>
        </div>
    </NuxtLink>
</template>