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
const baseRate = 15 // базовая процентная ставка в процентах

// Примерные данные из calcData.ranges:
// cost — стоимость недвижимости
// start — первоначальный взнос (%)
// years — срок кредита в годах

// Сумма кредита
const loanAmount = computed(() => {
    const propertyPrice = sliderValues.value.cost || 0
    const downPaymentPercent = sliderValues.value.start || 0
    return propertyPrice * (1 - downPaymentPercent / 100)
})

// Срок кредита в месяцах
const loanTermMonths = computed(() => {
    const years = sliderValues.value.years || 0
    return years * 12
})

// Процентная ставка с учетом сервисов
const interestRate = computed(() => {
    let rate = calcData.value?.base_rate ?? 15
    if (!calcData.value?.services) return rate

    for (const service of calcData.value.services) {
        if (service.is_active && service.rate_increase) {
            rate += Number(service.rate_increase)
        }
    }

    return Math.max(5, Math.min(30, rate)) // Ограничиваем ставку между 5% и 30%
})

// Формула аннуитетного платежа
const monthlyPayment = computed(() => {
    const P = loanAmount.value
    const r = interestRate.value / 100 / 12 // ежемесячная ставка
    const n = loanTermMonths.value

    if (!P || !r || !n) return 0

    const payment = (P * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1)
    return Math.round(payment)
})

// Необходимый доход (примерно 2x от ежемесячного платежа)
const requiredIncome = computed(() => {
    return (monthlyPayment.value * 2)
})

const calcResult = computed(() => {
    return {
        monthlyPayment: monthlyPayment.value,
        loanAmount: loanAmount.value,
        interestRate: interestRate.value,
        requiredIncome: requiredIncome.value,
        term: sliderValues.value.years || 0,
    }
})

// Форматирование чисел для удобного отображения
const formatNumber = (num: number): string => {
    return num.toFixed(2).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
}

const formatCurrency = (value: number): string => {
    return value.toLocaleString('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    })
}

const formatYears = (value: number): string => {
    const lastTwoDigits = value % 100
    if (lastTwoDigits >= 11 && lastTwoDigits <= 14) {
        return `${value} лет`
    }
    switch (value % 10) {
        case 1:
            return `${value} год`
        case 2:
        case 3:
        case 4:
            return `${value} года`
        default:
            return `${value} лет`
    }
}
const formatRangeValue = (range: Range, value: number | string): string => {
    const numValue = typeof value === 'string' ? parseFloat(value) : value

    switch (range.data_type) {
        case 'decimal':
            return new Intl.NumberFormat('ru-RU', {
                style: 'currency',
                currency: 'RUB',
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            }).format(numValue)
        case 'percent':
            return `${numValue}%`
        case 'integer':
            if (range.label === 'years') {
                const lastTwoDigits = numValue % 100
                if (lastTwoDigits >= 11 && lastTwoDigits <= 14) return `${numValue} лет`
                switch (numValue % 10) {
                    case 1:
                        return `${numValue} год`
                    case 2:
                    case 3:
                    case 4:
                        return `${numValue} года`
                    default:
                        return `${numValue} лет`
                }
            }
            return numValue.toString()
        default:
            return numValue.toString()
    }
}
const sliderDisplayValues = computed(() => {
    if (!calcData.value?.ranges) return {}

    const values = {} as Record<string, string>

    for (const range of calcData.value.ranges) {
        const key = range.label
        const value = sliderValues.value[key] || 0
        values[key] = formatRangeValue(range, value)
    }

    return values
})
</script>
<template>
    <BlockWrapper :block="block">
        <div class="container p-4 py-16 grid grid-cols-1 xl:grid-cols-[2fr_1fr] gap-6">
            <template v-if="loading || !calcData">
                <div class="col-span-full flex items-center justify-center text-2xl">
                    <Icon name="mdi:reload" class="animate-spin" />
                </div>
            </template>
            <template v-else>
                <div class="col-span-full text-7xl md:text-[6.5vh] font-bleu uppercase leading-tight">
                    {{ block.title }}
                </div>
                <div class="space-y-6">
                    <!-- Рендерим каждый range -->
                    <div v-for="range in calcData.ranges" :key="range.label" class="mb-4">
                        <!-- Заголовок -->
                        <label class="flex w-full gap-2 items-center mb-4">
                            {{ range.name }}
                            <span class="text-xl font-bleu">
                                {{ sliderDisplayValues[range.label] }}
                            </span>
                        </label>

                        <!-- Слайдер -->
                        <input v-model.number="sliderValues[range.label]" type="range" :min="Number(range.min_value)"
                            :max="Number(range.max_value)" :step="getStep(range)" />

                        <!-- Отображение min/max -->
                        <div class="flex justify-between text-xs text-gray-500 mt-1">
                            <span>{{ formatRangeValue(range, range.min_value) }}</span>
                            <span>{{ formatRangeValue(range, range.max_value) }}</span>
                        </div>
                    </div>
                </div>
                <div class="space-y-3">
                    <div class="flex justify-between text-sm sm:text-base">
                        <span>Сумма кредита:</span>
                        <span class="font-medium ">
                            {{ formatNumber(calcResult.loanAmount) }} ₽
                        </span>
                    </div>

                    <div class="flex justify-between text-sm sm:text-base">
                        <span>Ежемесячный платеж:</span>
                        <span class="font-medium text-secondary-400">
                            {{ formatNumber(calcResult.monthlyPayment) }} ₽
                        </span>
                    </div>

                    <div class="flex justify-between text-sm sm:text-base">
                        <span>Процентная ставка:</span>
                        <span class="font-medium ">
                            {{ calcResult.interestRate }}%
                        </span>
                    </div>

                    <div class="flex justify-between text-sm sm:text-base">
                        <span>Необходимый доход:</span>
                        <span class="font-medium text-secondary-400">
                            {{ formatNumber(calcResult.requiredIncome) }} ₽
                        </span>
                    </div>

                    <div class="flex justify-between text-sm sm:text-base">
                        <span>Срок кредита:</span>
                        <span class="font-medium ">
                            {{ calcResult.term }} лет
                        </span>
                    </div>

                    <div class="prose leading-normal text-lg" v-if="block.content">
                        <span v-html="block.content" />
                    </div>
                </div>
            </template>
        </div>
    </BlockWrapper>
</template>