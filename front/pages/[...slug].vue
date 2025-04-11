<script setup lang="ts">
import { useElementBounding, useIntersectionObserver, useWindowScroll } from '@vueuse/core'

const { fetchData } = useApiFetch()
const route = useRoute()

const config = useRuntimeConfig()
const imgBase = config.public.imgBase

const path = ['page', route.params.slug].filter(Boolean)
const { data, status, error } = await fetchData<PageData>(path.join('/'))

if (status.value == 'error') {
    showError({
        statusCode: error.value?.statusCode,
        message: `Ошибка при запросе к ${path.join('/')}`,
        fatal: true, // Указывает, что ошибка фатальная
    })
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

const mainSlider = computed(() =>
    data.value?.blocks.find(el => el.type == 'slider')
)

const blocksByType = (types: BlockType[]) => {
    return data.value?.blocks.filter(el => types.includes(el.type)) || []
}

const activeBlock = ref<string | null>(null);
const { y: scrollY } = useWindowScroll();
const isSticky = ref(false);
const initialMenuPosition = ref()
const menuRef = ref<HTMLElement | null>(null);
const placeholderRef = ref<HTMLElement | null>(null); // Заполнитель


onMounted(async () => {
    // Получаем элементы для наблюдения за блоками контента
    const observerTargets = blocksByType(['text', 'gallery'])
        .map(block => document.getElementById(block.slug))
        .filter(Boolean); // Удаляем null или undefined

    // Наблюдатель за активными блоками
    useIntersectionObserver(
        observerTargets,
        ([entry]) => {
            if (entry.isIntersecting) {
                activeBlock.value = entry.target.id; // Устанавливаем ID активного блока
            }
        },
        {
            threshold: 0.5, // Порог видимости (30% блока должно быть видно)
        }
    );

    await nextTick(); // Ждём, пока DOM обновится

    if (menuRef.value) {
        const { top, height } = useElementBounding(menuRef);
        initialMenuPosition.value = top.value;

        // Создаём заполнитель, если его ещё нет
        if (!placeholderRef.value) {
            placeholderRef.value = document.createElement('div');
            placeholderRef.value.style.height = `${height.value}px`;
            placeholderRef.value.style.display = 'none'; // Скрываем по умолчанию
            menuRef.value.parentNode?.insertBefore(placeholderRef.value, menuRef.value.nextSibling);
        }
    }
});

// Sticky-эффект при скролле
watchEffect(() => {
    if (initialMenuPosition.value !== null) {
        isSticky.value = scrollY.value > initialMenuPosition.value; // Меню становится sticky, если скролл ниже начальной позиции

        if (isSticky.value) {
            // Показываем заполнитель
            if (placeholderRef.value) placeholderRef.value.style.display = 'block';
        } else {
            // Скрываем заполнитель
            if (placeholderRef.value) placeholderRef.value.style.display = 'none';
        }
    }
});
</script>

<template>
    <div>
        <template v-if="mainSlider">
            <Slider :slides="mainSlider.images" />
        </template>
        <nav class="menu z-10 bg-white" :class="{ 'fixed top-0 right-0 left-0': isSticky }" ref="menuRef" v-if="false">
            <div class="container flex gap-2 items-stretch">
                <div class="flex items-center">
                    <PageLogo />
                </div>
                <ul class="menu flex gap-2 grow-1">
                    <template v-for="block in blocksByType(['text', 'gallery'])" :key="block.slug">
                        <li>
                            <NuxtLink :href="`#${block.slug}`"
                                :class="{ 'active': isSticky && activeBlock === block.slug }">{{
                                    block.menu_title || block.title }}</NuxtLink>
                        </li>
                    </template>
                </ul>
            </div>
        </nav>
        <template v-for="block in blocksByType(['text_right', 'gallery'])" :key="block.id">
            <div :id="block.slug" v-if="block.type == 'text_right'">
                <div class="container pt-4">
                    <div class="grid grid-cols-2 items-center gap-2">
                        <div class="col-span-1 col-start-2">
                            <div class="title mt-16 mb-20">
                                {{ block.title }}
                                <span v-if="block.sub_title" class="text-provincial-pink-400">{{ block.sub_title
                                }}</span>
                            </div>
                            <div class="content mb-20 prose prose-invert" v-html="block.content_rendered" />
                        </div>
                    </div>
                </div>
            </div>
            <div :id="block.slug" class="overflow-hidden" v-else>
                <div class="container pt-4">
                    <div class="title">
                        {{ block.title }}
                    </div>
                </div>
                <Gallery :slides="block.images" />
            </div>
        </template>
    </div>
</template>