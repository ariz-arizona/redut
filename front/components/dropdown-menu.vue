<script setup lang="ts">
import { useScroll } from '@vueuse/core';
const props = defineProps({
    link: { type: String },
    title: { type: String },
})

const isOpen = ref(false)
const { items: menuItems } = useMenuPages()
const { settings } = useSiteSettings()

const toggleMenu = () => {
    if (!menuItems.value.length) return
    isOpen.value = !isOpen.value
}

/**
 * Плавная прокрутка к якорю.
 */
const scrollToAnchor = (e: PointerEvent) => {
    // Находим элемент по якорю
    isOpen.value = false
    const anchor = (e.currentTarget as HTMLAnchorElement).href.split('#')[1]
    const targetElement = document.getElementById(anchor);

    if (targetElement) {
        // Используем useScroll для плавной прокрутки
        const { y } = useScroll(window, { behavior: 'smooth' });
        y.value = targetElement.getBoundingClientRect().top + window.scrollY;
    } else {
        // Если якорь не найден, перенаправляем на страницу /contacts
        navigateTo(`/#${anchor}`);
    }
};
</script>
<template>
    <div class="relative inline-block text-left">
        <!-- Кнопка меню -->
        <NuxtLink class="menubtn" @click.prevent="toggleMenu" v-if="menuItems.length">
            <Icon name="mdi:chevron-down" class="text-secondary-500 text-xl" v-if="menuItems.length" />
            <span>{{ title }}</span>
        </NuxtLink>
        <NuxtLink class="menubtn" to='/' v-else>
            <span>{{ settings?.name }}</span>
        </NuxtLink>

        <!-- Выпадающий список -->
        <div v-show="isOpen && menuItems.length"
            class="origin-bottom-right absolute left-0 top-full mt-2 w-56 !rounded-[2rem] z-10 menubtn bg-primary-950/70 flex-col items-start">
            <div class="py-1 basetext  w-full text-white" role="menu" aria-orientation="vertical"
                aria-labelledby="options-menu" v-for="item in menuItems">
                <NuxtLink :key="item.id" :href="`#${item.slug}`" @click.prevent="scrollToAnchor" class="text-xs"
                    role="menuitem">
                    {{ item.title }}
                </NuxtLink>
            </div>
        </div>
    </div>
</template>
