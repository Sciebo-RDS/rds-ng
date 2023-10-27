<script setup lang="ts">
import { ref, toRefs, watch } from "vue";

import Menu from "primevue/menu";

import { convertToStringArray } from "../../utils/Strings";

const props = defineProps(["items", "iconClass", "labelClass"]);
const state = toRefs(props);
const emit = defineEmits(["assign"]);

const iconClasses: string[] = convertToStringArray(props.iconClass);
const labelClasses: string[] = convertToStringArray(props.labelClass);

const popupMenu = ref();
watch(popupMenu, (value) => {
    emit("assign", value);
});
</script>

<template>
    <Menu ref="popupMenu" :model="state.items?.value" :popup="true">
        <template #item="{ item, label, props }">
            <a class="flex" v-bind="props.action">
                <span v-if="props.icon" :class="[...iconClasses, ...convertToStringArray(item.class)]">{{ item.icon }}</span>
                <span v-if="props.label" :class="[...labelClasses, ...convertToStringArray(item.class)]">{{ label }}</span>
            </a>
        </template>
    </Menu>
</template>

<style scoped lang="scss">
</style>
