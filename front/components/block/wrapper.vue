<script setup lang="ts">
const props = defineProps<{
    block: Block;
}>();
const scheme = `var(--image-overlay-${props.block.color_scheme})`
</script>
<style scoped>
.scheme-light,
.scheme-dark {
    --image-overlay-color: v-bind(scheme);
}
</style>
<template>
    <div class="relative" :id="block.slug" :class="[{
        'scheme-light': block.color_scheme == 'light',
        'scheme-dark': block.color_scheme == 'dark',
    }]" :block_type="block.type">
        <slot />
    </div>
</template>