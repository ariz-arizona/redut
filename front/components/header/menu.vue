<script setup lang="ts">
import { useScroll } from '@vueuse/core';

const scrollToFeedback = () => {
    // Находим элемент с id="feedback"
    const feedbackElement = document.getElementById('feedback');

    if (feedbackElement) {
        // Используем useSmoothScroll для плавной прокрутки
        const { x, y } = useScroll(window, { behavior: 'smooth' })

        y.value = feedbackElement.getBoundingClientRect().top
    } else {
        navigateTo('contacts')
    }

}
</script>

<template>
    <NuxtLink to="#feedback" class="menubtn" @click.prevent="scrollToFeedback">
        <Icon name="mdi:chevron-down" class="text-secondary-500 text-xl" />
        <span>
            Обратная связь
        </span>
    </NuxtLink>
</template>