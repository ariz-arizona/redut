<script setup lang="ts">
import("~/assets/tailwind.scss");
const { fetchData } = useApiFetch()
const { data: settings } = fetchData<SiteSettings>('site-settings')

const menuRef = ref()
const { isVisible: isSliderVisible } = useMainSlider();
</script>
<template>
    <div>
        <div class="w-full z-10" :ref="menuRef" :class="[
            isSliderVisible ? 'h-52 absolute top-20' : 'h-32 fixed bg-primary-800/75',
            'transition-all duration-300 ease-in-out'
        ]">
            <div class="container grid grid-cols-[1fr_14rem_1fr] items-start gap-4 px-2 h-full"
                :class="[isSliderVisible ? 'items-start' : 'items-center']">
                <div class="flex gap-8 items-center basetext">
                    <HeaderMenu />
                    <NuxtLink to="/">Контакты</NuxtLink>
                </div>
                <HeaderLogo :logo="settings?.logo" />
                <div class="flex justify-end gap-8 items-center">
                    <template v-if="settings?.phone_number">
                        <HeaderPhone :phone="settings?.phone_number" />
                    </template>
                    <HeaderChange class="basetext" />
                </div>
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
