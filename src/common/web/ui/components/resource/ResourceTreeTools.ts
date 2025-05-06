import type { TreeNode } from "primevue/treenode";
import { type Ref } from "vue";

import { flattenResourcesTreeNodes } from "../../../data/entities/resource/ResourceUtils";

export function useResourceTreeTools() {
    function expandRootNodes(nodes: TreeNode[], expandedNodes: Ref<Record<string, boolean>>): void {
        const rootResources: Record<string, boolean> = {};
        for (const node of nodes) {
            rootResources[node.key] = true;
        }
        expandedNodes.value = rootResources;
    }

    function expandAllNodes(nodes: TreeNode[], expandedNodes: Ref<Record<string, boolean>>): void {
        const allResources: Record<string, boolean> = {};
        flattenResourcesTreeNodes(nodes as TreeNode[]).forEach((resource) => (allResources[resource] = true));
        expandedNodes.value = allResources;
    }

    function collapseAllNodes(expandedNodes: Ref<Record<string, boolean>>): void {
        expandedNodes.value = {};
    }

    return {
        expandRootNodes,
        expandAllNodes,
        collapseAllNodes
    };
}
