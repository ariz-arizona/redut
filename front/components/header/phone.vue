<script setup lang="ts">
import { parsePhoneNumber } from 'libphonenumber-js/min';

const props = defineProps<{
    phone: string;
}>();

</script>

<template>
    <div v-if="props.phone">
        <a :href="`tel:${parsePhoneNumber(props.phone).getURI()}`">
            {{ parsePhoneNumber(props.phone, 'RU').formatInternational() }}
        </a>
    </div>
</template>