<script setup lang="ts">
const props = defineProps<{
    block: Block
    imgBase: string
}>()
</script>
<template>
    <BlockDefault :block="block" :img-base="imgBase"/>
</template>