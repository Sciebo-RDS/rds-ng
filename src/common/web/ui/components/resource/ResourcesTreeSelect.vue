<script setup lang="ts">
import type { TreeNode } from "primevue/treenode";
import TreeSelect from "primevue/treeselect";
import { type PropType, ref, toRefs, watch } from "vue";

function pathToSelectedResources(path: string): Record<string, boolean> {
    const selectedResources: Record<string, boolean> = {};
    selectedResources[path] = true;
    return selectedResources;
}

const props = defineProps({
    options: {
        type: Object as PropType<Object[]>,
        required: true,
    },
    placeholder: {
        type: String,
        default: "Select a value",
    },
    loading: {
        type: Boolean,
        default: false,
    },
    loadingError: {
        type: String,
        default: "",
    },
    loadingLabel: {
        type: String,
        default: "Loading data...",
    },
});
const { options, placeholder, loading, loadingError, loadingLabel } = toRefs(props);
const model = defineModel<string>({ default: "" });

const isLoading = ref(loading.value);
if (isLoading.value) {
    watch(options, () => {
        isLoading.value = false;
    });
}

const selectedResources = ref<Object>(pathToSelectedResources(model.value));
watch(selectedResources, (newResources) => {
    const paths = Object.keys(newResources);
    model.value = paths.length > 0 ? paths[0] : "";
});
watch(model, (newPath) => {
    selectedResources.value = pathToSelectedResources(newPath);
});
</script>

<template>
    <TreeSelect
        :options="options as TreeNode[]"
        v-model="selectedResources"
        selection-mode="single"
        :placeholder="placeholder"
        :pt="{
            panel: 'r-z-index-toplevel',
        }"
        :disabled="isLoading || !!loadingError"
    >
        <template #value="value">
            <div v-if="!isLoading && !loadingError && value.value.length > 0" class="flex gap-2">
                <span :class="value.value[0].icon + ' opacity-75'" /> {{ value.value[0].data }}
            </div>
            <div v-else>
                <span v-if="loadingError" class="flex">
                    <span class="material-icons-outlined mi-error-outline mr-1" /><span>{{ loadingError }}</span>
                </span>
                <span v-else-if="isLoading" class="flex">
                    <span class="material-icons-outlined mi-refresh animate-spin mr-1" /><span>{{ loadingLabel }}</span>
                </span>
                <span v-else>{{ value.placeholder }}</span>
            </div>
        </template>
    </TreeSelect>
</template>

<style scoped lang="scss"></style>
