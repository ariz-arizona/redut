<script setup lang="ts">
defineProps<{
    block: Block;
}>();
</script>
<style scoped>
.scheme-light,
.scheme-dark {
    --image-overlay-color: v-bind("block.color_scheme === 'dark' ? 'var(--image-overlay-dark)' : 'var(--image-overlay-light)'"
        );
}
</style>
<template>
    <div :id="block.slug" :class="[{
        'scheme-light': block.color_scheme == 'light',
        'scheme-dark': block.color_scheme == 'dark',
    }]">
        <slot />
    </div>
</template>