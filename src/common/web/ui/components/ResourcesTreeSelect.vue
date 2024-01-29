<script setup lang="ts">
import { type TreeNode } from "primevue/treenode";
import TreeSelect from "primevue/treeselect";
import { type PropType, ref, toRefs, watch } from "vue";

import { type Resource } from "../../data/entities/resource/Resource";

const props = defineProps({
    options: {
        type: Object as PropType<TreeNode[]>,
        required: true
    },
    placeholder: {
        type: String,
        default: "Select a value"
    }
});
const { options, placeholder } = toRefs(props);
const model = defineModel<Resource>({ default: "" });

const selectedResources = ref<Object>({});
watch(selectedResources, (newResources) => {
    const paths = Object.keys(newResources);
    model.value = paths.length > 0 ? paths[0] : "";
});
watch(model, (newPath) => {
    const newSelectedResources: Record<string, boolean> = {};
    newSelectedResources[newPath] = true;
    selectedResources.value = newSelectedResources;
});
</script>

<template>
    <TreeSelect
        :options="options as TreeNode[]"
        v-model="selectedResources"
        selection-mode="single"
        :placeholder="placeholder"
        :pt="{
            panel: 'r-z-index-toplevel'
        }"
    >
        <template #value="value">
            <div v-if="value.value.length > 0" class="flex gap-2"><span :class="value.value[0].icon + ' opacity-75'" /> {{ value.value[0].data }}</div>
            <div v-else>{{ value.placeholder }}</div>
        </template>
    </TreeSelect>
</template>

<style scoped lang="scss">

</style>
