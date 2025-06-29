<script setup lang="ts">
import type { YMap } from '@yandex/ymaps3-types';
import { createYmapsOptions, YandexMap, YandexMapDefaultSchemeLayer, YandexMapDefaultFeaturesLayer } from 'vue-yandex-maps';
const props = defineProps<{
    block: Block
    imgBase: string
}>()
const { settings, loading } = useSiteSettings();
watch(settings, () => {
    if (settings.value?.yandex_api_key) {
        createYmapsOptions({
            apikey: settings.value?.yandex_api_key,
        })
    }
},)
//Можно использовать для различных преобразований
const map = shallowRef<null | YMap>(null);
const point = computed((): [number, number] => {
  const defaultPoint: [number, number] = [37.617644, 55.755819]

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
  // Если вы хотите использовать отдельное поле для zoom — добавьте его в настройки
  // Пока используем дефолтное значение
  return 9
})
</script>
<template>
    <BlockDefault :block="block" :img-base="imgBase">
        <template #image>
            <template v-if="settings?.yandex_api_key">
                <yandex-map v-model="map" :settings="{
                    location: {
                        center: point,
                        zoom: zoom,
                    },

                }" width="100%" height="500px">
                    <yandex-map-default-scheme-layer />
                    <yandex-map-default-features-layer />
                </yandex-map>
            </template>
        </template>
    </BlockDefault>
</template>