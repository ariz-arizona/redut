// useMenuPages.js
const items = ref<any[]>([])

export function useImagesData() {
    const setItems = (list: Image[]) => {
        items.value = [...list]
    }

    return {
        items,
        setItems
    }
}