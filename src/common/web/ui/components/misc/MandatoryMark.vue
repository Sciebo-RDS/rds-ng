<script setup lang="ts">
const props = defineProps({
    color: {
        type: String,
        default: ""
    },
    title: {
        type: String,
        default: "This field is required"
    }
});
</script>

<template>
    <span :title="title">
        <span v-if="!!color" class="font-bold" :style="`color: ${color} !important;`">*</span>
        <span v-else class="p-error font-bold">*</span>
    </span>
</template>

<style scoped lang="scss"></style>
