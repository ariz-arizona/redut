<script setup lang="ts">
const { calcData, loading, error, fetchCalcData } = useCalcData()

const props = defineProps<{
    block: Block;
}>();

onMounted(() => { fetchCalcData() })
</script>
<template>
    <BlockWrapper :block="block">
        <div class="container p-4 py-16 grid grid-cols-1 xl:grid-cols-[1fr_2fr] gap-4">
            <div class="loading" v-if="loading">
                <Icon name="mdi:reload" class="animate-spin" />
            </div>
            <div v-else>
                <h2>Диапазоны:</h2>
                <ul>
                    <li v-for="range in calcData?.ranges" :key="range.label">
                        {{ range.name }}: {{ range.min_value }} – {{ range.max_value }}
                    </li>
                </ul>

                <h2>Услуги:</h2>
                <ul>
                    <li v-for="service in calcData?.services" :key="service.id">
                        {{ service.name }} (изменение ставки: {{ service.rate_increase }})
                    </li>
                </ul>
            </div>
        </div>
    </BlockWrapper>
</template>