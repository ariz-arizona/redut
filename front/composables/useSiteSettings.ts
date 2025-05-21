// Реактивное состояние для хранения данных
const settings = ref<SiteSettings | null>(null);
const loading = ref<boolean>(false);
const error = ref<string | null>(null);

export function useSiteSettings() {
    const { fetchData } = useApiFetch()

    // Метод для получения данных
    const fetchSettings = async () => {
        loading.value = true;
        error.value = null;

        try {
            const { data } = await fetchData<SiteSettings>('site-settings');
            settings.value = data.value; // Сохраняем данные в реактивную переменную
        } catch (err) {
            console.error('Ошибка при получении настроек сайта:', err);
            error.value = 'Не удалось загрузить настройки сайта';
        } finally {
            loading.value = false;
        }
    };

    // Автоматическая загрузка данных при монтировании компонента
    onMounted(() => {
        fetchSettings();
    });

    return {
        settings, // Данные настроек сайта
        loading,  // Флаг загрузки
        error,    // Ошибка, если она возникла
        fetchSettings, // Метод для повторной загрузки данных
    };
}