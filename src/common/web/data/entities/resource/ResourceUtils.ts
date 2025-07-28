import type { TreeNode } from "primevue/treenode";
import { ResourceType } from "./Resource";

import { ResourcesList } from "./ResourcesList";

/**
 * Transforms a `ResourcesList` into a Vue *TreeNode*.
 *
 * @param resources - The resources list to transform.
 * @param simpleData - Whether to use simple data.
 * @param includeFiles - Whether to also include files.
 *
 * @returns - The tree nodes list.
 */
export function resourcesListToTreeNodes(resources: ResourcesList, simpleData: boolean = false, includeFiles: boolean = true): TreeNode[] {
    const sortNodes = (nodes: TreeNode[]): TreeNode[] => {
        return nodes.sort((node1, node2) => (node1.label && node2.label ? node1.label.localeCompare(node2.label) : 0));
    };

    const folderNodes: TreeNode[] = [];
    for (const [_, folderResources] of Object.entries(resources.folders)) {
        folderNodes.push(...resourcesListToTreeNodes(folderResources, simpleData, includeFiles));
    }

    const fileNodes: TreeNode[] = [];
    if (includeFiles) {
        for (const fileResource of resources.files) {
            fileNodes.push({
                key: fileResource.filename,
                label: fileResource.basename,
                data: simpleData ? fileResource.filename : fileResource,
                type: ResourceType.File,
                icon: "material-icons-outlined mi-description"
            } as TreeNode);
        }
    }

    return [
        {
            key: resources.resource.filename,
            label: resources.resource.basename || "/",
            data: simpleData ? resources.resource.filename : resources.resource,
            icon: "material-icons-outlined mi-folder",
            type: ResourceType.Folder,
            children: [...sortNodes(folderNodes), ...sortNodes(fileNodes)]
        } as TreeNode
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

            if (!!node.children) {
                _filter(node.children);
            }
        }
    }

    _filter(nodes);
    return filteredNodes;
}

/**
 * Adjust the `leaf` states of all children in the tree nodes, depending on their presence in the resources list and a predicate.
 *
 * @param nodes - The tree nodes to adjust.
 * @param resources - The underlying resources list.
 * @param predicate - A decider function whether to include a path.
 * @param includeFiles - Whether to also take files into account.
 */
export function adjustResourcesTreeNodesLeafStates(
    nodes: TreeNode[],
    resources: ResourcesList,
    predicate: (path: string) => boolean,
    includeFiles: boolean = true
): TreeNode[] {
    function _adjust(nodes: TreeNode[]): void {
        for (const node of nodes) {
            const res = resourcesListFindPath(resources, node.key);
            if (!!res && predicate(node.key)) {
                node.leaf = res.folders.length == 0 && (includeFiles ? res.files.length == 0 : true);
            } else {
                node.leaf = node.type === ResourceType.File;
            }

            if (!!node.children) {
                _adjust(node.children);
            }
        }
    }

    _adjust(nodes);
    return nodes;
}

/**
 * Search for a path within a resources list.
 *
 * @param resources - The resources list to search in.
 * @param path - The path to search for.
 *
 * @returns - The found list or **undefined** otherwise.
 */
export function resourcesListFindPath(resources: ResourcesList, path: string): ResourcesList | undefined {
    if (resources.resource.filename == path) {
        return resources;
    }

    for (const folder of resources.folders) {
        const res = resourcesListFindPath(folder, path);
        if (!!res) {
            return res;
        }
    }

    return undefined;
}

/**
 * Checks if a given path exists in the resources list.
 *
 * @param resources - The resources list to check.
 * @param path - The path to search for.
 */
export function resourcesListContainsPath(resources: ResourcesList, path: string): boolean {
    return !!resourcesListFindPath(resources, path);
}
