<script setup lang="ts">
defineProps(['loading'])
const blobs = ref<any[]>([])

onMounted(() => {
    const blobCount = 4
    const newBlobs = []

    for (let i = 0; i < blobCount; i++) {
        const size = Math.floor(Math.random() * 150) + 150
        const top = Math.random() * 80 + 10 // %
        const left = Math.random() * 90 // %

        newBlobs.push({
            size,
            top,
            left
        })
    }

    blobs.value = newBlobs
})
</script>
<template>
    <transition enter-active-class="transition-opacity duration-300" enter-from-class="opacity-0"
        enter-to-class="opacity-100" leave-active-class="transition-opacity duration-500 delay-200"
        leave-from-class="opacity-100" leave-to-class="opacity-0">
        <div v-show="loading" class="fixed inset-0 z-50 flex items-center justify-center">
            <!-- Основной фон -->
            <div class="absolute inset-0 bg-primary-950 overflow-hidden">

                <!-- Радиальные градиенты (блоbs) -->
                <div v-for="(blob, index) in blobs" :key="index"
                    class="absolute z-20 rounded-full bg-secondary-400 opacity-70 blur-3xl transition-transform duration-1000 animate-blob"
                    :style="{
                        width: blob.size + 'px',
                        height: blob.size + 'px',
                        top: blob.top + '%',
                        left: blob.left + '%',
                        animationDelay: (index * 1.5) + 's'
                    }">
                </div>

            </div>

            <!-- Фоновое затемнение над блоbs, но под спиннером -->
            <div class="absolute inset-0 bg-black/20 z-30 backdrop-blur-sm"></div>

            <!-- Спиннер поверх всего -->
            <div class="relative z-40 flex items-center justify-center">
                <Icon name="mdi:refresh" class="animate-spin text-white text-8xl" />
            </div>
        </div>
    </transition>
</template>