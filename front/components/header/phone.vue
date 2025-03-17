<script setup lang="ts">
const phone = '+7 (978) 888 55 22'
</script>
<template>
    <div>
        <a :href="`tel:${phone.replace(/[^+\d]/g, '')}`">
            {{ phone }}
        </a>
    </div>
</template>