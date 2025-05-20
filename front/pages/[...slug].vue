<script setup lang="ts">
import { useFavicon, useScroll } from '@vueuse/core';
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
    const res = await fetchData<PaginatedResponse<PageData>>(cat.value.link || `page?category__slug=${slug[1].trim()}`);
    if (res.data.value && res.status.value == 'success') {
        const { results, ...pagination } = res.data.value;

        cat.value.items = results;
        cat.value.pagination = {
            count: pagination.count,
            next: pagination.next,
            previous: pagination.previous,
        };

        console.log(cat.value.items)
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
        if (settings.value?.favicon) {
            useFavicon(`${imgBase}/${settings.value?.favicon}`)
        }
    }
})

const mainSlider = computed(() =>
    combineData.value.find((el: Block) => el.type == 'slider')
)

const blocksByType = (types: BlockType[]) => {
    return combineData.value.filter((el: Block) => types.includes(el.type)) || []
}
const dummyCatBlock = { color_scheme: 'light', slug: 'cat' } as Block
</script>

<template>
    <div>
        <template v-if="mainSlider">
            <BlockWrapper :block="mainSlider">
                <Slider :slides="mainSlider.images" />
            </BlockWrapper>
        </template>
        <template v-if="!mainSlider">
            <div class="h-40" />
        </template>
        <template
            v-for="(block, index) in blocksByType(['text', 'gallery', 'lead', 'full_image', 'feedback', 'category'])"
            :key="block.id">
            <template v-if="(index + 1) === Math.floor(combineData.length / 2)">
                <template v-if="cat.items?.length">
                    <BlockWrapper :block="dummyCatBlock">
                        <div class="container px-4 py-10 grid grid-cols-2 xl:grid-cols-3 gap-6">
                            <template v-for="item in cat.items" :key="item.slug">
                                <BlockCategoryItem :item="item" :img-base="imgBase" class="min-h-72" />
                            </template>
                        </div>
                    </BlockWrapper>
                </template>
                <template v-if="cat.pagination?.previous || cat.pagination?.next">
                    <BlockWrapper :block="dummyCatBlock">
                        <div class="container px-4 py-10 w-full md:max-w-screen-md items-center justify-center flex gap-4">
                            <template v-if="cat.pagination?.previous">
                                <a :href="cat.pagination.previous" @click.prevent="paginate"
                                    class="leadbtn px-8 p-4">Назад</a>
                            </template>
                            <template v-if="cat.pagination?.next">
                                <a :href="cat.pagination.next" @click.prevent="paginate"
                                    class="leadbtn px-8 p-4">Вперед</a>
                            </template>
                        </div>
                    </BlockWrapper>
                </template>
            </template>
            <BlockText v-if="block.type === 'text'" :block="block" :img-base="imgBase" />
            <BlockGallery v-else-if="block.type === 'gallery'" :block="block" />
            <BlockLead v-else-if="block.type === 'lead'" :block="block" :img-base="imgBase" />
            <BlockFullImage v-else-if="block.type === 'full_image'" :block="block" :img-base="imgBase" />
            <BlockFeedback v-else-if="block.type === 'feedback'" :block="block" />
            <BlockCategory v-else-if="block.type === 'category'" :block="block" :img-base="imgBase" />
        </template>
    </div>
</template>