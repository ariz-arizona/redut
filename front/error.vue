<script setup lang="ts">
const route = useRoute()
import type { NuxtError } from '#app'

const props = defineProps({
    error: Object as () => NuxtError
})


const errorRedirect = () => {
    if (!props.error) return
    if (props.error.statusCode == 404 && route.path !== '404') {
        navigateTo('/404')
    }
}

onMounted(errorRedirect)
watch(props, errorRedirect, {deep: true})
</script>
<template>
    <NuxtLayout>
        <div class="container pt-4">
            <div class="prose">
                <h1>Error</h1>
                <p>Произошла ошибка</p>
            </div>
        </div>
    </NuxtLayout>
</template>
