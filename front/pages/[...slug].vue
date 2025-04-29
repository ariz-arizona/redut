<script setup lang="ts">
import { useScroll } from '@vueuse/core';
const { fetchData } = useApiFetch()
const route = useRoute()

const config = useRuntimeConfig()
const imgBase = config.public.imgBase
const { settings, loading: settingLoading } = useSiteSettings();

// Приводим slug к массиву
const slug = Array.isArray(route.params.slug)
    ? route.params.slug.filter(Boolean) // Убираем пустые значения
    : [route.params.slug].filter(Boolean);

const data = ref<PageData | CategoryData | null>()
const status = ref();
const error = ref();

const pageType = ref<'page' | 'category'>()
const combineData = ref()
// Функция для получения данных
const fetchDataBySlug = async () => {
    let path: string;
    let res;

    data.value = null
    error.value = null
    status.value = null

    if (slug[0] === 'cat') {
        pageType.value = 'category'
        // Маршрут начинается с "cat"
        if (slug.length === 2) {
            // Конкретная категория (/cat/CAT)
            const categoryName = slug[1];
            path = ['cat', categoryName].join('/');
            res = await fetchData<CategoryData>(path);
        } else if (slug.length === 3) {
            // Страница внутри категории (/cat/CAT/PAGE)
            const pageName = slug[2];
            path = ['cat', pageName].join('/');
            res = await fetchData<PageData>(path);
        } else {
            // Неизвестный маршрут
            throw new Error('Unknown category route');
        }
    } else {
        pageType.value = 'page'
        // Маршрут без "cat"
        if (slug.length === 0) {
            // Главная страница (/)
            path = ['page', 'homepage'].join('/');
            res = await fetchData<PageData>(path);
        } else if (slug.length === 1) {
            // Страница (/PAGE)
            const pageName = slug[0];
            path = ['page', pageName].join('/');
            res = await fetchData<PageData>(path);
        } else {
            // Неизвестный маршрут
            throw new Error('Unknown page route');
        }
    }

    data.value = res.data.value
    error.value = res.error.value
    status.value = res.status.value

    combineData.value = data.value?.blocks
};

// Получаем данные
await fetchDataBySlug();

if (status.value == 'error') {
    showError({
        statusCode: error.value?.statusCode,
        message: `Ошибка при запросе к ${slug.join('/')}`,
        fatal: true, // Указывает, что ошибка фатальная
    })
}
const cat = ref({
    items: null as PageData[] | null,
    pagination: null as Pagination | null,
    link: null as string | null
})
const fetchPagesInCat = async () => {
    const res = await fetchData<PaginatedResponse<PageData>>(cat.value.link || `page?cat=${slug[1].trim()}`);
    if (res.data.value && res.status.value == 'success') {
        const { results, ...pagination } = res.data.value;

        cat.value.items = results;
        cat.value.pagination = {
            count: pagination.count,
            next: pagination.next,
            previous: pagination.previous,
        };
        const blocksFromPages = results.map(page => page.blocks.find(el => ['text', 'lead'].includes(el.type)))

        if (data.value && data.value.blocks) {
            const half = Math.floor(data.value.blocks.length / 2);
            const newBlocks = [
                ...data.value.blocks.slice(0, half),
                ...blocksFromPages,
                ...data.value.blocks.slice(half),
            ];

            combineData.value = newBlocks as Block[];
        }
    }
}
if (pageType.value == 'category' && slug.length > 1) {
    await fetchPagesInCat()
}
const paginate = async (e: any) => {
    cat.value.link = e.target.href.split('api/')[1]
    await fetchPagesInCat()
    const { y } = useScroll(window, { behavior: 'smooth' });
    y.value = 0
}

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

watch(settingLoading, () => {
    if (settingLoading.value == false) {
        useSeoMeta({ title: settings.value?.name + ' | ' + data.value?.title, })
    }
})

const mainSlider = computed(() =>
    combineData.value.find((el: Block) => el.type == 'slider')
)

const blocksByType = (types: BlockType[]) => {
    return combineData.value.filter((el: Block) => types.includes(el.type)) || []
}
</script>

<template>
    <div>
        <template v-if="mainSlider">
            <Slider :slides="mainSlider.images" />
        </template>
        <template v-if="!mainSlider">
            <div class="h-40" />
        </template>
        <template v-for="block in blocksByType(['text', 'gallery', 'lead', 'feedback'])" :key="block.id">
            <BlockText v-if="block.type === 'text'" :block="block" :img-base="imgBase" />
            <BlockGallery v-else-if="block.type === 'gallery'" :block="block" />
            <BlockLead v-else-if="block.type === 'lead'" :block="block" :img-base="imgBase" />
            <BlockFeedback v-else-if="block.type === 'feedback'" :block="block" />
        </template>
        <template v-if="cat.pagination?.previous || cat.pagination?.next">
            <div class="container py-4 w-full md:max-w-screen-md items-center justify-center flex gap-4">
                <template v-if="cat.pagination?.previous">
                    <a :href="cat.pagination.previous" @click.prevent="paginate" class="leadbtn px-8 p-4">Назад</a>
                </template>
                <template v-if="cat.pagination?.next">
                    <a :href="cat.pagination.next" @click.prevent="paginate" class="leadbtn px-8 p-4">Вперед</a>
                </template>
            </div>
        </template>
    </div>
</template>