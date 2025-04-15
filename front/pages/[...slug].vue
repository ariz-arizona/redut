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
            <Slider :slides="mainSlider.images" :content="mainSlider.content_rendered" />
        </template>
        <template v-if="!mainSlider">
            <div class="h-40" />
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
        <template v-for="block in blocksByType(['text', 'gallery', 'lead', 'feedback'])" :key="block.id">
            <div :id="block.slug" v-if="block.type === 'text'">
                <div class="container pt-4">
                    <div class="grid grid-cols-1 md:grid-cols-2 items-center gap-2">
                        <!-- Картинка -->
                        <div v-if="block.images.length" :class="[
                            block.is_text_right ? 'md:col-start-1' : 'md:col-start-2',
                            'col-span-1'
                        ]">
                            <img :src="`${imgBase}/${block.images[0].image}`" :alt="block.title"
                                class="w-full h-auto shadow-md" />
                        </div>

                        <!-- Текст -->
                        <div :class="[
                            block.is_text_right ? 'md:col-start-2' : 'md:col-start-1',
                            'col-span-1'
                        ]">
                            <div class="title mt-16 mb-20">
                                {{ block.title }}
                                <span v-if="block.sub_title" class="text-sandal-400">
                                    {{ block.sub_title }}
                                </span>
                            </div>
                            <div class="basetext mb-20 prose" v-html="block.content_rendered" />
                        </div>
                    </div>
                </div>
            </div>
            <div :id="block.slug" v-if="block.type == 'gallery'" class="overflow-hidden relative">
                <div
                    class="text-[50vh] text-center text-sandal-200 font-wonder pointer-events-none z-20 absolute left-0 right-0 leading-none">
                    {{ block.title }}
                </div>
                <Gallery :slides="block.images" />
                <template v-if="block.link || block.external_link">
                    <div class="relative -translate-y-1/2 z-10 flex justify-center w-full">
                        <NuxtLink :to="((block.link || block.external_link) as string)"
                            :external="!!block.external_link" class="size-36 p-4 leadbtn">
                            <span class="leading-4">
                                Читать далее
                            </span>
                        </NuxtLink>
                    </div>
                </template>
            </div>
            <div :id="block.slug" v-if="block.type == 'lead'" class="overflow-hidden">
                <div class="container pt-4">
                    <h3 class="text-[8vmin] font-bleu text-center w-3/4 m-auto uppercase leading-tight"
                        v-html="block.title"></h3>
                    <div class="relative flex justify-center w-full mt-20" v-if="(block.link || block.external_link)">
                        <NuxtLink :to="((block.link || block.external_link) as string)"
                            :external="!!block.external_link" class="leadbtn p-8">
                            <span class="leading-4">
                                {{ block.sub_title || 'Читать далее' }}
                            </span>
                        </NuxtLink>
                    </div>
                </div>
                <div class="bg-no-repeat bg-cover bg-center h-[50vh] p-4 -z-10 relative pointer-events-none"
                    :class="[{ '-mt-[25vh]': (block.link || block.external_link) }]"
                    :style="{ backgroundImage: createBgWithGrad(`${imgBase}/${block.images[0].image}`, 'rgba(24,29,36,1)', 'rgba(0,0,0,0)') }"
                    v-if="block.images.length">
                    <NuxtImg :src="`${imgBase}/${block.images[0].image}`" class="invisible" />
                </div>
            </div>
            <div :id="block.slug" v-if="block.type == 'feedback'">
                <div class="container p-4 grid grid-cols-1 xl:grid-cols-3">
                    <div class="col-span-full">
                        <div class="text-center font-bleu text-[12vmin] relative">
                            <span v-html="block.title" />
                            <span
                                class="font-wonder text-[24vmin] text-sandal-300 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
                                {{ block.sub_title }}
                            </span>
                        </div>
                    </div>
                    <div class="col-span-full xl:col-span-1 xl:col-start-2 flex justify-center">
                        <Feedback />
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>