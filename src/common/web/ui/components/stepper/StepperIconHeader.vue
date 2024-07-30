<script setup lang="ts">
import { toRefs } from "vue";

const props = defineProps({
    index: {
        type: Number,
        required: true
    },
    activeIndex: {
        type: Number,
        required: true
    },
    clickCallback: {
        type: true,
        required: true
    },
    icon: {
        type: String,
        required: true
    }
});
const { index, activeIndex, clickCallback, icon } = toRefs(props);
</script>

<template>
    <button class="bg-transparent border-0 inline-flex flex-col gap-2" @click="clickCallback" type="button">
        <span
            :class="[
                'border-2 rounded-md r-border-color w-12 h-12 inline-flex items-center justify-center',
                { 'r-primary-bg': index <= activeIndex, 'surface-border': index > activeIndex }
            ]"
        >
            <i class="r-text material-icons-outlined" :class="[{ 'r-primary-text': index <= activeIndex }, icon]" />
        </span>
    </button>
</template>

<style scoped lang="scss"></style>
