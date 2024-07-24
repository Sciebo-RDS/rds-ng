import { type TreeNode } from "primevue/treenode";

import { ResourcesList } from "./ResourcesList";

/**
 * Transforms a `ResourcesList` into a Vue *TreeNode*.
 *
 * @param resources - The resources list to transform.
 * @param simpleData - Whether to use simple data.
 *
 * @returns - The tree nodes list.
 */
export function resourcesListToTreeNodes(resources: ResourcesList, simpleData: boolean = false): TreeNode[] {
    const sortNodes = (nodes: TreeNode[]): TreeNode[] => {
        return nodes.sort((node1, node2) => (node1.label && node2.label ? node1.label.localeCompare(node2.label) : 0));
    };

    const folderNodes: TreeNode[] = [];
    for (const [_, folderResources] of Object.entries(resources.folders)) {
        folderNodes.push(...resourcesListToTreeNodes(folderResources, simpleData));
    }

    const fileNodes: TreeNode[] = [];
    for (const fileResource of resources.files) {
        fileNodes.push({
            key: fileResource.filename,
            label: fileResource.basename,
            data: simpleData ? fileResource.filename : fileResource,
            icon: "material-icons-outlined mi-description",
        } as TreeNode);
    }

    return [
        {
            key: resources.resource.filename,
            label: resources.resource.basename || "/",
            data: simpleData ? resources.resource.filename : resources.resource,
            icon: "material-icons-outlined mi-folder",
            children: [...sortNodes(folderNodes), ...sortNodes(fileNodes)],
        } as TreeNode,
    ];
}

/**
 * Flattens resources tree nodes into a single, flat array.
 *
 * @param nodes - The nodes to flatten.
 */
export function flattenResourcesTreeNodes(nodes: TreeNode[]): string[] {
    const flatten = (nodes: TreeNode[], results: string[]) => {
        nodes.forEach((node) => {
            results.push(node.key || "(unknown)");

            if (Array.isArray(node.children)) {
                flatten(node.children, results);
            }
        });
    };

    let results: string[] = [];
    flatten(nodes, results);
    return results;
}

/**
 * Filters a list of resources tree nodes according to the provided keys.
 *
 * @param nodes - The nodes to filter.
 * @param keys - The keys to keep.
 *
 * @returns - A flat list of all matching nodes.
 */
export function filterResourcesTreeNodes(nodes: TreeNode[], keys: string[]): TreeNode[] {
    const filteredNodes: TreeNode[] = [];

    function _filter(nodes: TreeNode[]): void {
        for (const node of nodes) {
            if (node.key && keys.includes(node.key)) {
                filteredNodes.push(node);
            }

            if (node.children) {
                _filter(node.children);
            }
        }
    }

    _filter(nodes);
    return filteredNodes;
}
