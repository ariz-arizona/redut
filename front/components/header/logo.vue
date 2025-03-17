<script setup lang="ts">
// Массив иконок
const icons = [
    "mdi:home-city",
    "fa-solid:building",
    // "carbon:construction",
    // "tabler:shield-check",
    // "heroicons:shield-check-20-solid",
    // "material-symbols:architecture",
    // "bi:tools",
    "mdi:city-variant",
    "jam:building",
];

// Случайная иконка
const randomIcon = ref("");

// Функция для выбора случайной иконки
const getRandomIcon = () => {
    const randomIndex = Math.floor(Math.random() * icons.length);
    randomIcon.value = icons[randomIndex];
};

// Вызываем функцию при монтировании компонента
onMounted(() => {
    getRandomIcon();
});
</script>
<template>
    <div class="flex justify-center items-center gap-2">
        <span class="size-14">
            <Icon :name="randomIcon" class="w-full h-full" />
        </span>
        <span class="uppercase text-4xl font-black leading-3">Редут</span>
    </div>
</template>