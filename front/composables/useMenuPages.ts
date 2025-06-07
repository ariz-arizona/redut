// useMenuPages.js
const items = ref<any[]>([])

export function useMenuPages() {

    /**
     * Метод для преобразования списка в элементы меню
     * @param {Array} list
     */
    const setItems = (list: any[]) => {
        items.value = list.map(item => ({
            id: item.id,
            title: item.menu_title,
            slug: item.slug || '#',
        }))
    }

    return {
        items,
        setItems
    }
}