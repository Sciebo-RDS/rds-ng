<script setup lang="ts">
import Button from "primevue/button";
import Column from "primevue/column";
import IconField from "primevue/iconfield";
import InputIcon from "primevue/inputicon";
import InputText from "primevue/inputtext";
import type { TreeNode } from "primevue/treenode";
import TreeTable from "primevue/treetable";
import { type PropType, ref, toRefs, unref, watch } from "vue";

import { Resource, ResourceType } from "../../../data/entities/resource/Resource";
import { filterResourcesTreeNodes } from "../../../data/entities/resource/ResourceUtils";
import { humanReadableFileSize } from "../../../utils/Strings";
import { useResourceTreeTools } from "./ResourceTreeTools";

const props = defineProps({
    data: {
        type: Object as PropType<Object[]>,
        required: true
    },
    dynamic: {
        type: Boolean,
        default: false
    },
    refreshable: {
        type: Boolean,
        default: false
    },
    expandFirstOnly: {
        type: Boolean,
        default: false
    }
});
const { data, dynamic, refreshable, expandFirstOnly } = toRefs(props);
const selectedNodes = defineModel<Object>("selectedNodes", { default: {} });
const selectedData = defineModel<Resource[]>("selectedData", { default: [] });
const emits = defineEmits<{
    (e: "refresh"): void;
    (e: "changed", selected: Resource[]): void;
    (e: "nodeExpand", path: string): void;
    (e: "nodeCollapse", path: string): void;
}>();
const { expandAllNodes, expandRootNodes, collapseAllNodes } = useResourceTreeTools();

const filters = ref({} as Record<string, string>);
const expandedNodes = ref({} as Record<string, boolean>);

const isLoading = ref(true);
const loadingMode = ref("mask");
if (isLoading.value) {
    watch(
        data,
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

watch(selectedNodes, () => {
    const selectedPaths = Object.keys(unref(selectedNodes));
    const selectedTreeNodes = filterResourcesTreeNodes(unref(data) as TreeNode[], selectedPaths);
    selectedData.value = selectedTreeNodes.map((node) => node.data);

    emits("changed", selectedData.value);
});

function refresh(): void {
    isLoading.value = true;
    loadingMode.value = "mask";
    emits("refresh");
}

function expandFirst(): void {
    if (unref(data)) {
        expandRootNodes(unref(data) as TreeNode[], expandedNodes);
    }
}

function expandAll(): void {
    if (unref(data)) {
        expandAllNodes(unref(data) as TreeNode[], expandedNodes);
    }
}

function collapseAll(): void {
    collapseAllNodes(expandedNodes);
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
    <TreeTable
        :value="data as TreeNode[]"
        selection-mode="multiple"
        meta-key-selection
        v-model:selection-keys="selectedNodes"
        v-model:expanded-keys="expandedNodes"
        :filters="filters"
        :loading="isLoading"
        :loading-mode="loadingMode"
        auto-layout
        class="grid content-start border-0 border-t-2 border-slate-50"
        :pt="{
            header: 'r-shade-gray h-fit p-3',
            footer: 'r-shade-dark-gray sticky top-[100vh] border-0',
            tableContainer: '!overflow-auto'
        }"
        @node-expand="onNodeExpand"
        @node-collapse="onNodeCollapse"
    >
        <template #header>
            <div class="text-right">
                <IconField iconPosition="left">
                    <InputIcon>
                        <i class="material-icons-outlined mi-search mt-[-4px]" />
                    </InputIcon>
                    <InputText v-model="filters['global']" placeholder="Search objects" class="w-full" />
                </IconField>
            </div>
        </template>

        <Column field="basename" header="Name" class="p-0 pl-2 truncate w-full" expander header-class="r-shade-gray">
            <template #body="entry">
                <div class="flex gap-1 items-center">
                    <span :class="entry.node.icon" class="opacity-65" /><span class="pt-0.5">{{ entry.node.data.basename }}</span>
                </div>
            </template>
        </Column>

        <Column
            header="Size"
            class="w-0"
            header-class="r-shade-gray"
            :pt="{ columnHeaderContent: 'place-self-end truncate', bodyCellContent: 'place-self-end truncate' }"
        >
            <template #body="entry">
                <span v-if="entry.node.data.size >= 0">{{ humanReadableFileSize(entry.node.data.size) }}</span>
                <span v-else class="italic r-text-light-gray">Unknown</span>
            </template>
        </Column>

        <Column
            header="Items in folder"
            class="w-0"
            header-class="r-shade-gray"
            :pt="{ columnHeaderContent: 'place-self-end truncate', bodyCellContent: 'place-self-end truncate' }"
        >
            <template #body="entry">
                <div v-if="entry.node.data.type === ResourceType.Folder">
                    <span v-if="entry.node.data.size >= 0">{{ entry.node.children.length }}</span>
                    <span v-else class="italic r-text-light-gray">Unknown</span>
                </div>
            </template>
        </Column>

        <template #footer>
            <div class="flex justify-end gap-2">
                <Button icon="material-icons-outlined mi-keyboard-arrow-down" label="Expand all" size="small" text @click="expandAll" />
                <Button icon="material-icons-outlined mi-keyboard-arrow-right" label="Collapse all" size="small" text @click="collapseAll" />
                <Button v-if="refreshable" icon="material-icons-outlined mi-refresh" label="Refresh" size="small" text severity="warn" @click="refresh" />
            </div>
        </template>
    </TreeTable>
</template>

<style scoped lang="scss"></style>
