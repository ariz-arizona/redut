<script setup lang="ts">
defineProps<{
    block: Block;
}>();
</script>
<template>
    <div :id="block.slug" :class="[{
        'scheme-light': block.color_scheme == 'light',
        'scheme-dark': block.color_scheme == 'dark',
    }]">
        <slot />
    </div>
</template>