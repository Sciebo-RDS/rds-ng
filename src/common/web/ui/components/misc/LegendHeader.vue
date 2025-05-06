<script setup lang="ts">
import Popover from "primevue/popover";
import { ref, toRefs } from "vue";

const props = defineProps({
    title: {
        type: String,
        required: true
    },
    description: {
        type: String,
        default: ""
    },
    iconClass: {
        type: String,
        default: "pi pi-question-circle ml-2 text-lg"
    }
});
const { title, description, iconClass } = toRefs(props);

const descriptionPopover = ref();
</script>

<template>
    <span class="p-fieldset-legend-label">
        <slot name="title">
            {{ title }}
        </slot>
    </span>
    <span
        v-if="description"
        :title="description"
        class="opacity-65 cursor-pointer"
        @click="
            (e) => {
                descriptionPopover.toggle(e);
                e.stopPropagation();
            }
        "
    >
        <i :class="iconClass" />
        <Popover ref="descriptionPopover" class="w-fit max-w-[35%] p-2">
            <template #container>
                <div v-html="description" />
            </template>
        </Popover>
    </span>
</template>

<style scoped lang="scss"></style>
