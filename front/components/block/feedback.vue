<script setup lang="ts">
import Feedback from '../feedback.vue';

defineProps<{
    block: Block;
}>();
</script>
<template>
    <div :id="block.slug">
        <div class="container p-4 grid grid-cols-1 xl:grid-cols-3 mb-8">
            <div class="col-span-full">
                <div class="text-center font-bleu text-[12vmin] relative">
                    <span v-html="block.title" v-if="block.title" />
                    <span
                        class="font-wonder text-[24vmin] text-secondary-300 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
                    >
                        {{ block.sub_title }}
                    </span>
                </div>
            </div>
            <div class="col-span-full xl:col-span-1 xl:col-start-2 flex justify-center">
                <Feedback :btn="(block.btn_title as string)" />
            </div>
        </div>
    </div>
</template>
