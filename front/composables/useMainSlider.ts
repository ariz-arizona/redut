// composables/useMainSlider.ts
// Ссылка на элемент слайдера
const mainSlider = ref<HTMLElement | null>(null);

// Состояние видимости слайдера
const isVisible = ref(false);

export function useMainSlider() {
    // Функция для установки референса на слайдер
    const setMainSliderRef = (el: HTMLElement | null) => {
        mainSlider.value = el;
    };

    // Флаг для отслеживания, был ли обсервер запущен
    let isObserverInitialized = false;

    // Инициализация IntersectionObserver
    let observer: IntersectionObserver | null = null;

    // Отслеживаем изменение mainSlider
    watch(mainSlider, (newSlider) => {
        if (newSlider && !isObserverInitialized) {
            // Создаем IntersectionObserver
            observer = new IntersectionObserver(
                (entries) => {
                    entries.forEach((entry) => {
                        isVisible.value = entry.isIntersecting;
                        console.log(isVisible.value ? "Слайдер виден" : "Слайдер скрыт");
                    });
                },
                {
                    threshold: 0.5, // Порог видимости (50% элемента должно быть видно)
                }
            );

            // Начинаем наблюдать за слайдером
            observer.observe(newSlider);

            // Устанавливаем флаг, чтобы предотвратить повторный запуск
            isObserverInitialized = true;
        }
    });

    // Очистка при размонтировании компонента
    onUnmounted(() => {
        if (observer) {
            observer.disconnect();
        }
    });

    return {
        mainSlider,
        isVisible,
        setMainSliderRef,
    };
}