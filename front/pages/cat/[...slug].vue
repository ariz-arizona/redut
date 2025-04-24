<script setup lang="ts">
const { fetchData } = useApiFetch()
const route = useRoute()

const config = useRuntimeConfig()
const imgBase = config.public.imgBase
const { settings, loading: settingLoading } = useSiteSettings();

const fetchCatData = async () => {
    // Приводим slug к массиву
    const slug = Array.isArray(route.params.slug)
        ? route.params.slug
        : [route.params.slug].filter(Boolean);

    let path: string;
    let data: any = null;
    let status: { value: string } = { value: 'error' };
    let error: any = null;

    try {
        if (slug.length === 1) {
            // Запрашиваем категорию
            path = ['cat', slug[0]].filter(Boolean).join('/');
            ({ data, status, error } = await fetchData<CategoryData>(path));
        } else if (slug.length > 1) {
            // Запрашиваем страницу по последнему элементу
            const lastSegment = slug[slug.length - 1];
            path = ['cat', lastSegment].filter(Boolean).join('/');
            ({ data, status, error } = await fetchData<PageData>(path));
        } else {
            // Запрашиваем все категории
            path = 'cat';
            ({ data, status, error } = await fetchData<CategoryData[]>(path));
        }
    } catch (err) {
        // Обработка ошибок
        error = err;
        status = { value: 'error' };
    }

    // Возвращаем результат
    return { data, status, error };
};
const { data, status, error } = await fetchCatData()
console.log(data.value)
</script>
<template>
    123
</template>