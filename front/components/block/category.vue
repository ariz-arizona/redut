<script setup lang="ts">
const { fetchData } = useApiFetch()

const props = defineProps<{
    block: Block;
    imgBase: string;
}>();

// Состояние для хранения данных новостей
const pages = ref<PageData[]>([]);


// === Загрузка по ID ===
async function loadPagesByIds(ids: number[]) {
    try {
        const idsQuery = ids.join(',')
        const res = await useApiFetch().fetchData<PaginatedResponse<PageData>>(
            `page/?id__in=${idsQuery}`
        )
        pages.value = res.data.value?.results || []
    } catch (error) {
        console.error('Ошибка при загрузке страниц по ID:', error)
    }
}

// === Загрузка по категории ===
async function loadPagesByCategory(slug: string) {
    try {
        const { fetchData } = useApiFetch()
        const res = await fetchData<PaginatedResponse<PageData>>(
            `page/?limit=4&category__slug=${slug.trim()}`
        )
        pages.value = res.data.value?.results || []
    } catch (error) {
        console.error('Ошибка при загрузке страниц по категории:', error)
    }
}

// === Основная логика загрузки ===
async function loadPages() {
    // Если есть selected_pages — грузим их
    if (props.block.selected_pages?.length > 0) {
        await loadPagesByIds(props.block.selected_pages)
        return
    }

    // Иначе грузим по категории, если она указана
    const catSlug = props.block.category?.slug
    if (catSlug) {
        await loadPagesByCategory(catSlug)
        return
    }

    // Иначе — ничего не загружаем
    pages.value = []
}
onMounted(() => { loadPages() })
</script>
<template>
    <BlockWrapper :block="block">
        <div class="container p-4 py-16 grid grid-cols-1 gap-4" :class="{
            'xl:grid-cols-[1fr_2fr]': block.is_text_right,
            'xl:grid-cols-[2fr_1fr]': !block.is_text_right,
        }">
            <div class="col-span-1 flex items-end justify-center cat-title" :class="[{
                'order-first': block.is_text_right,
                'order-last': !block.is_text_right
            }]">
                <div class="text-5xl md:text-7xl md:sideways-writing-lr md:indent-20 font-bleu uppercase text-left"
                    v-html="block.title || block.category.title" />
                <NuxtLink :to="`cat/${block.category.slug}`"
                    class="flex items-center justify-center leading-none size-24 rounded-full border border-secondary-400">
                    <Icon :name="block.is_text_right ? `mdi:arrow-right` : `mdi:arrow-left`" class="w-3/4 h-3/4" />
                </NuxtLink>
            </div>
            <div class="col-span-1 grid grid-cols-1 xl:grid-cols-2 gap-8 ">
                <template v-for="item in pages">
                    <BlockCategoryItem :img-base="imgBase" :item="item" />
                </template>
            </div>
        </div>
    </BlockWrapper>
</template>