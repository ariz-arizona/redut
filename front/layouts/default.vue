<script setup lang="ts">
import("~/assets/tailwind.scss");
import { useSiteSettings } from '@/composables/useSiteSettings';

const { settings, loading, error, fetchSettings } = useSiteSettings();

const menuRef = ref()
const { isVisible: isSliderVisible } = useMainSlider();

const config = useRuntimeConfig()
const imgBase = config.public.imgBase
</script>
<template>
    <div>
        <div class="w-full z-20" :ref="menuRef" :class="[
            isSliderVisible ? 'h-36 absolute top-20' : 'h-28 fixed bg-primary-800/75',
            'transition-all duration-300 ease-in-out'
        ]">
            <div class="container grid grid-cols-1 md:grid-cols-[1fr_10rem_1fr] xl:grid-cols-[1fr_14rem_1fr] items-start gap-4 px-2 h-full"
                :class="[isSliderVisible ? 'items-start' : 'items-center']">
                <div class="gap-2 xl:gap-8 items-center basetext hidden md:flex flex-wrap xl:flex-nowrap">
                    <HeaderMenu />
                    <NuxtLink to="/contacts">Контакты</NuxtLink>
                </div>
                <HeaderLogo :logo="settings?.logo" />
                <div class="justify-end gap-2 xl:gap-8 items-center hidden md:flex flex-wrap xl:flex-nowrap">
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
            <div class="container flex items-center gap-4 p-2 py-8 basetext">
                <div class="grid grid-cols-3 w-full">
                    <div class="col-span-1" v-if="settings?.documents">
                        <span class="text-secondary-400/50">
                            {{ new Date().getFullYear() }} © {{ settings.name }}<br />
                        </span>
                        <template v-for="doc in settings.documents">
                            <a :href="`${imgBase}/${doc.file}`" download>{{ doc.title }}</a><br />
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
</template>
