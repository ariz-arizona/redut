<script setup lang="ts">
const { fetchData } = useApiFetch()

const props = defineProps<{
    block: Block;
}>();

// Состояние для хранения данных новостей
const pages = ref<PageData[]>([]);

// Функция для загрузки данных
async function loadPages() {
    try {
        const cat = props.block.category.slug
        // Получаем данные через API
        const res = await fetchData<PaginatedResponse<PageData>>(`page?limit=2&category__slug=${cat.trim()}`);
        pages.value = res.data.value?.results as PageData[]
    } catch (error) {
        console.error('Ошибка при загрузке страниц:', error);
    }
}
onMounted(() => { loadPages() })
</script>
<template>
    <div :id="block.slug">
        <div class="container p-4 grid grid-cols-1 xl:grid-cols-[1fr_2fr] gap-4 mb-8">
            <div class="col-span-1 flex items-end justify-center">
                <div class="text-secondary-400 text-7xl font-bleu uppercase sideways-writing-lr text-left indent-20"
                    v-html="block.title || block.category.title" />
                <NuxtLink :to="`cat/${block.category.slug}`"
                    class=" flex items-center justify-center leading-none size-24 rounded-full border border-secondary-400">
                    <Icon name="mdi:arrow-right" class="w-3/4 h-3/4 text-secondary-200" />
                </NuxtLink>
            </div>
            <div class="col-span-1">
                <template v-for="item in pages">
                    <div class="border">
                        {{ item.title }}
                    </div>
                </template>
            </div>
        </div>
    </div>
</template>