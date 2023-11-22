<script setup lang="ts">
const props = defineProps({
    title: {
        type: String,
        required: true
    },
    mandatory: {
        type: Boolean
    }
});
</script>

<template>
    <label>{{ props.title }}<span v-if="props.mandatory" class="p-error font-bold"> *</span></label>
</template>

<style scoped lang="scss">

</style>
