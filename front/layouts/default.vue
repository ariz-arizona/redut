<script setup lang="ts">
import("~/assets/tailwind.scss");
const { fetchData } = useApiFetch()
const { data: settings } = fetchData<SiteSettings>('site-settings')
</script>
<template>
    <div>
        <div class="bg-primary-800/75 text-white">
            <div class="container flex items-center gap-4 p-2">
                <HeaderLogo :logo="settings?.logo" />
                <HeaderMenu class="grow" />
                <template v-if="settings?.phone_number">
                    <HeaderPhone :phone="settings?.phone_number" />
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
