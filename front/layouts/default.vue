<script setup lang="ts">
import { createYmapsOptions } from "vue-yandex-maps";

import("~/assets/tailwind.scss");

const { settings, loading } = useSiteSettings();
const menuRef = ref()
const { isVisible: isSliderVisible } = useMainSlider();

const config = useRuntimeConfig()
const imgBase = config.public.imgBase

const topItems = computed(() => settings.value?.top_items || [])
const makeLink = (el: TopItem) => {
    if (el.type == 'page') return '/' + el.slug + '#' + el.block
    if (el.type == 'category') return '/cat/' + el.slug + '#' + el.block
}
onMounted(() => {
    const darkBgColor = (twConfig.theme?.extend?.colors as any).primary['950']
    const darkBgColorRGB = (hexToRgb(darkBgColor))
    const lightBgColor = (twConfig.theme?.extend?.colors as any).secondary['50']
    const lightBgColorRGB = (hexToRgb(lightBgColor))

    document.documentElement.style.setProperty('--image-overlay-dark', darkBgColorRGB)
    document.documentElement.style.setProperty('--image-overlay-light', lightBgColorRGB)
    document.documentElement.style.setProperty('--image-overlay-opacity', (settings.value?.overlay_opacity || 0.3).toString())
})
</script>
<template>
    <div class="overflow-hidden">
        <Preloader :loading="loading" />
        <div :class="[{ 'hidden': loading }]">
            <div class="w-full z-20 text-secondary-50" :ref="menuRef" :class="[
                isSliderVisible ? 'h-36 absolute top-20' : 'h-28 fixed bg-primary-800/90',
                'transition-all duration-300 ease-in-out'
            ]">
                <div class="container grid grid-cols-1 md:grid-cols-[1fr_10rem_1fr] xl:grid-cols-[1fr_14rem_1fr] items-start gap-4 px-2 h-full"
                    :class="[isSliderVisible ? 'items-start' : 'items-center']">
                    <div class="gap-2 xl:gap-8 items-center basetext hidden md:flex flex-wrap xl:flex-nowrap">
                        <template v-if="topItems[0]">
                            <DropdownMenu :title="topItems[0].title" />
                        </template>
                    </div>
                    <HeaderLogo :logo="settings?.logo" />
                    <div
                        class="justify-end gap-2 xl:gap-8 items-center basetext hidden md:flex flex-wrap xl:flex-nowrap">
                        <template v-if="settings?.phone_number">
                            <HeaderPhone :phone="settings?.phone_number" />
                        </template>
                        <template v-if="topItems[1]">
                            <NuxtLink :to="makeLink(topItems[1])" class="contents">
                                <div
                                    class="menubtn text-nowrap bg-secondary-500 hover:bg-secondary-700 transition-colors">
                                    <span>{{ topItems[1].title }}</span>
                                </div>
                            </NuxtLink>
                        </template>
                    </div>
                </div>
            </div>
            <Suspense>
                <div class="min-h-[calc(100vh-10rem)]">
                    <slot />
                </div>
            </Suspense>
            <div class="bg-primary-800 text-white">
                <div class="container flex items-center gap-4 p-2 py-8 basetext">
                    <div class="grid grid-cols-3 w-full">
                        <div class="col-span-1" v-if="settings?.documents">
                            <span class="text-secondary-400/50">
                                {{ new Date().getFullYear() }} © {{ settings.name }}<br />
                            </span>
                            <template v-for="doc in settings.documents">
                                <a :href="`${imgBase}/${doc.file}`" :download="doc.file.split('/').pop()"
                                    target="_blank">{{
                                        doc.title }}</a><br />
                            </template>
                        </div>
                        <div class="col-span-1 text-center">
                            <span class="size-24">
                                <HeaderLogo :logo="settings?.logo" />
                            </span>
                        </div>
                        <div class="col-span-1 text-right">
                            <div class="text-xs" v-html="settings?.footer_text" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
