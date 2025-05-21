
// Композабл
const calcData = ref<CalcConfig | null>(null)
const loading = ref<boolean>(false)
const error = ref<string | null>(null)

export function useCalcData() {
    const { fetchData } = useApiFetch()

    const fetchCalcData = async () => {
        loading.value = true
        error.value = null

        try {
            const { data } = await fetchData<CalcConfig>('calc/config')
            calcData.value = data.value
        } catch (err) {
            console.error('Ошибка при загрузке данных калькулятора:', err)
            error.value = 'Не удалось загрузить данные калькулятора'
        } finally {
            loading.value = false
        }
    }

    // Автоматически загружаем данные при вызове хука
    onMounted(() => {
        fetchCalcData()
    })

    return {
        calcData,     // Конфиг калькулятора
        loading,      // Флаг загрузки
        error,        // Ошибка, если есть
        fetchCalcData // Метод для повторной загрузки
    }
}