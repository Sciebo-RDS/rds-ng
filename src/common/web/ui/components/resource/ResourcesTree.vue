<script setup lang="ts">
import Tree from "primevue/tree";
import type { TreeNode } from "primevue/treenode";
import { type PropType, ref, toRefs, unref, watch } from "vue";

import { useResourceTreeTools } from "./ResourceTreeTools";

function pathToSelectedResources(path: string): Record<string, boolean> {
    const selectedResources: Record<string, boolean> = {};
    selectedResources[path] = true;
    return selectedResources;
}

const props = defineProps({
    options: {
        type: Object as PropType<Object[]>,
        required: true
    },
    loading: {
        type: Boolean,
        default: false
    },
    dynamic: {
        type: Boolean,
        default: false
    },
    expandFirstOnly: {
        type: Boolean,
        default: false
    }
});
const { options, loading, dynamic, expandFirstOnly } = toRefs(props);
const model = defineModel<string>({ default: "" });
const emits = defineEmits<{
    (e: "changed", path: string): void;
    (e: "nodeExpand", path: string): void;
    (e: "nodeCollapse", path: string): void;
}>();
const { expandRootNodes, expandAllNodes } = useResourceTreeTools();

const isLoading = ref(loading.value);
const loadingMode = ref("mask");
if (isLoading.value) {
    watch(
        options,
        () => {
            isLoading.value = false;
            if (dynamic.value) {
                loadingMode.value = "icon";
            }

            if (unref(expandFirstOnly)) {
                expandFirst();
            } else {
                expandAll();
            }
        },
        { once: true }
    );
}

const selectedResources = ref<Object>(pathToSelectedResources(model.value));
watch(selectedResources, (newResources) => {
    const paths = Object.keys(newResources);
    model.value = paths.length > 0 ? paths[0]! : "";

    emits("changed", model.value);
});
watch(model, (newPath) => {
    selectedResources.value = pathToSelectedResources(newPath);
});

const expandedNodes = ref<Record<string, boolean>>({});

function expandFirst(): void {
    if (unref(options)) {
        expandRootNodes(unref(options) as TreeNode[], expandedNodes);
    }
}

function expandAll(): void {
    if (unref(options)) {
        expandAllNodes(unref(options) as TreeNode[], expandedNodes);
    }
}

function onNodeExpand(node: TreeNode): void {
    if (dynamic.value) {
        node.loading = true;
    }

    emits("nodeExpand", node.key);
}

function onNodeCollapse(node: TreeNode): void {
    emits("nodeCollapse", node.key);
}
</script>

<template>
    <Tree
        :value="options as TreeNode[]"
        :expanded-keys="expandedNodes"
        v-model:selection-keys="selectedResources"
        selection-mode="single"
        :loading="isLoading"
        :loading-mode="loadingMode"
        class="p-0 m-0 bg-transparent rounded"
        :class="{ 'h-full': isLoading }"
        :pt="{ root: 'text-sm', nodeIcon: '!text-xl' }"
        :dt="{ 'node.padding': '0' }"
        @node-expand="onNodeExpand"
        @node-collapse="onNodeCollapse"
    />
</template>

<style scoped lang="scss"></style>
