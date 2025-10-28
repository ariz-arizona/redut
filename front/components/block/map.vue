<script setup lang="ts">
const props = defineProps<{
    block: Block
    imgBase: string
}>()
const { settings, loading } = useSiteSettings();

const point = computed((): [number, number] => {
    const defaultPoint: [number, number] = [37.620070, 55.753630]

    if (!settings.value?.yandex_api_point) {
        return defaultPoint
    }

    const [lngStr, latStr] = settings.value.yandex_api_point
        .split(',')
        .map(coord => coord.trim())

    const lng = parseFloat(lngStr)
    const lat = parseFloat(latStr)

    if (!isNaN(lng) && !isNaN(lat)) {
        return [lng, lat]
    }

    return defaultPoint
})

const zoom = computed(() => {
    return 13
})

const mapUrl = computed(() => {
    if (!settings.value?.yandex_api_key) {
        return ''
    }
    
    const [lng, lat] = point.value
    const size = '450,450'
    
    return `https://static-maps.yandex.ru/v1?ll=${lng},${lat}&lang=ru_RU&size=${size}&z=${zoom.value}&pt=${lng},${lat},pmwtm1&apikey=${settings.value.yandex_api_key}`
})
</script>
<template>
    <BlockDefault :block="block" :img-base="imgBase">
        <template #image>
            <img 
                v-if="mapUrl" 
                :src="mapUrl" 
                alt="Карта" 
                class="w-full h-[500px] object-cover"
            />
        </template>
    </BlockDefault>
</template>