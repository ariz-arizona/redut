<script setup lang="ts">
const { calcData, loading, error, fetchCalcData } = useCalcData()

const props = defineProps<{
    block: Block;
}>();

onMounted(() => { fetchCalcData() })

// Реактивные значения для слайдеров
const sliderValues = ref<Record<string, number>>({})

// Инициализируем значения при загрузке данных
watchEffect(() => {
    const initial: Record<string, number> = {}
    for (const range of calcData.value?.ranges || []) {
        initial[range.label] = Number(range.min_value)
    }
    sliderValues.value = initial
})
const getStep = (range: Range) => {
    if (range.data_type === 'integer') return 1
    if (range.data_type === 'percent') return 1 // можно 0.1 для дробных процентов
    return 0.01
}
</script>
<template>
    <BlockWrapper :block="block">
        <div class="container p-4 py-16 grid grid-cols-1 xl:grid-cols-[1fr_2fr] gap-4">
            <div class="loading" v-if="loading || !calcData">
                <Icon name="mdi:reload" class="animate-spin" />
            </div>
            <div v-else>
                <div class="space-y-6 max-w-lg mx-auto">
                    <h2 class="text-xl font-bold">Настройки кредита</h2>

                    <!-- Рендерим каждый range -->
                    <div v-for="range in calcData.ranges" :key="range.label" class="mb-4">
                        <!-- Заголовок -->
                        <label>
                            {{ range.name }}
                            <span class="ml-1 text-gray-500 text-xs">
                                ({{ sliderValues[range.label] }}{{ range.data_type === 'percent' ? '%' : '' }})
                            </span>
                        </label>

                        <!-- Слайдер -->
                        <input v-model.number="sliderValues[range.label]" type="range" :min="Number(range.min_value)"
                            :max="Number(range.max_value)" :step="getStep(range)" />

                        <!-- Отображение min/max -->
                        <div class="flex justify-between text-xs text-gray-500 mt-1">
                            <span>{{ range.min_value }}</span>
                            <span>{{ range.max_value }}</span>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </BlockWrapper>
</template>