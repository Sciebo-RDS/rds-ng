<script setup lang="ts">
import Button from "primevue/button";
import Column from "primevue/column";
import IconField from "primevue/iconfield";
import InputIcon from "primevue/inputicon";
import InputText from "primevue/inputtext";
import type { TreeNode } from "primevue/treenode";
import TreeTable from "primevue/treetable";
import { onMounted, type PropType, ref, toRefs, watch } from "vue";

import { ResourceType } from "../../../data/entities/resource/Resource";
import { flattenResourcesTreeNodes } from "../../../data/entities/resource/ResourceUtils";
import { humanReadableFileSize } from "../../../utils/Strings";

const props = defineProps({
    data: {
        type: Object as PropType<Object[]>,
        required: true,
    },
    refreshable: {
        type: Boolean,
        default: false,
    },
});
const { data, refreshable } = toRefs(props);
const selectedNodes = defineModel<Object>("selectedNodes", { default: {} });
const emits = defineEmits<{
    (e: "refresh"): void;
}>();

const filters = ref({} as Record<string, string>);
const expandedNodes = ref({} as Record<string, boolean>);

const isLoading = ref(true);
watch(data, () => {
    isLoading.value = false;
    expandAll();
});
onMounted(() => {
    refresh();
});

function refresh(): void {
    isLoading.value = true;
    emits("refresh");
}

function expandAll(): void {
    if (data!.value) {
        const allResources: Record<string, boolean> = {};
        flattenResourcesTreeNodes(data!.value as TreeNode[]).forEach((resource) => (allResources[resource] = true));
        expandedNodes.value = allResources;
    }
}

function collapseAll(): void {
    expandedNodes.value = {};
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
        auto-layout
        class="grid content-start border-0 border-t-2 border-slate-50"
        :pt="{
            header: 'r-shade-gray h-fit',
            footer: 'r-shade-dark-gray sticky top-[100vh] border-0',
            wrapper: '!overflow-auto',
        }"
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

        <Column field="basename" header="Name" class="p-0 pl-2 truncate" expander :pt="{ rowToggler: 'mb-1', headerCell: 'r-shade-gray' }">
            <template #body="entry">
                <span :class="entry.node.icon" class="opacity-75 relative top-1.5 mr-1" /><span>{{ entry.node.data.basename }}</span>
            </template>
        </Column>

        <Column header="Size" class="w-48 text-right truncate" :pt="{ headerCell: 'r-shade-gray' }">
            <template #body="entry">
                {{ humanReadableFileSize(entry.node.data.size) }}
            </template>
        </Column>

        <Column header="Elements in folder" class="w-32 text-right truncate" :pt="{ headerCell: 'r-shade-gray' }">
            <template #body="entry">
                <span v-if="entry.node.data.type === ResourceType.Folder">{{ entry.node.children.length }}</span>
            </template>
        </Column>

        <template #footer>
            <div class="flex justify-end gap-2">
                <Button icon="material-icons-outlined mi-keyboard-arrow-down" label="Expand all" size="small" text @click="expandAll" />
                <Button icon="material-icons-outlined mi-keyboard-arrow-right" label="Collapse all" size="small" text @click="collapseAll" />
                <Button v-if="refreshable" icon="material-icons-outlined mi-refresh" label="Refresh" size="small" text severity="warning" @click="refresh" />
            </div>
        </template>
    </TreeTable>
</template>

<style scoped lang="scss"></style>
