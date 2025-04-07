<script setup lang="ts">
import("~/assets/tailwind.scss");
const { fetchData } = useApiFetch()
const { data: settings } = fetchData<SiteSettings>('site-settings')

const menuRef = ref()
const { isVisible: isSliderVisible } = useMainSlider();
</script>
<template>
    <div>
        <div class="w-full text-provincial-pink-200 z-10" :ref="menuRef" :class="[
            isSliderVisible ? 'h-40 absolute top-20' : 'h-20 fixed bg-primary-800/75',
            'transition-all duration-300 ease-in-out'
        ]">
            <div class="container grid grid-cols-3 items-center gap-4 px-2 h-full">
                <HeaderMenu />
                <HeaderLogo :logo="settings?.logo" />
                <template v-if="settings?.phone_number">
                    <HeaderPhone :phone="settings?.phone_number" class="text-right" />
                </template>
            </div>
        </div>
        <Suspense>
            <slot />
        </Suspense>
        <div class="bg-primary-800 text-white mt-8">
            <div class="container flex items-center gap-4 p-2 py-8">
                <div class="grid grid-cols-3">
                    <div class="col-span-2">
                        <div class="text-xs">
                            {{ settings?.footer_text }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
