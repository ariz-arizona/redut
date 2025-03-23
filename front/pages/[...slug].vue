<script setup lang="ts">
const { fetchData } = useApiFetch()
const route = useRoute()

const path = ['page', route.params.slug].filter(Boolean)
const { data, status } = await fetchData<PageData>(path.join('/'))
useSeoMeta({
    title: data.value?.title,
    description: data.value?.meta_description,
    ogTitle: data.value?.meta_title || data.value?.title,
    ogDescription: data.value?.meta_description,
    ogImage: data.value?.blocks[0]?.images[0]?.image || './og_image.jpg', // Берем первое изображение из блока
    twitterTitle: data.value?.title,
    twitterDescription: data.value?.meta_description,
    twitterImage: data.value?.blocks[0]?.images[0]?.image || './og_image.jpg', // Берем первое изображение из блока
});
</script>

<template>
    <div>
        <template v-for="block in data?.blocks">
            <template v-if="block.type == 'slider'">
                <Slider :slides="block.images" />
            </template>
        </template>
    </div>
</template>