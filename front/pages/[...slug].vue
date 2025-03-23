<script setup lang="ts">
const { fetchData } = useApiFetch()
const route = useRoute()

const path = ['page', route.params.slug].filter(Boolean)
const { data, status, error } = await fetchData<PageData>(path.join('/'))
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
console.log(error)
console.log(data)
const mainSlider = computed(() =>
    data.value?.blocks.find(el => el.type == 'slider')
)
const blocksWithoutSlider = computed(() =>
    data.value?.blocks.filter(el => el.type !== 'slider')
)
</script>

<template>
    <div>
        <template v-if="mainSlider">
            <Slider :slides="mainSlider.images" />
        </template>
        <nav class="menu">
            <div class="container flex gap-2 items-stretch">
                <div class="flex items-center">
                    <PageLogo />
                </div>
                <ul class="menu flex gap-2 grow-1">
                    <template v-for="block in blocksWithoutSlider" :key="block.slug">
                        <li>
                            <NuxtLink :href="`#${block.slug}`">{{ block.menu_title || block.title }}</NuxtLink>
                        </li>
                    </template>
                </ul>
            </div>
        </nav>
        <template v-for="block in blocksWithoutSlider" :key="block.id">
            <div :id="block.slug">
                <div class="container">
                    <div class="title">
                        {{ block.title }}
                    </div>
                    <div class="content">
                        <div class="prose prose-base" v-html="block.content_rendered" />
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>