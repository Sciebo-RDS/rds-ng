import { type TreeNode } from "primevue/treenode";

import { ResourcesList } from "./ResourcesList";
import { extractFilenameFromPath } from "../../../utils/Paths";

/**
 * The type of a resource.
 */
export enum ResourceType {
    Folder,
    File
}

/**
 * Resource node data.
 */
export interface ResourceNodeData {
    resource: string;
    resourceType: ResourceType;

    label: string;
}

/**
 * Transforms a `ResourcesList` into a Vue *TreeNode*.
 *
 * @param resources - The resources list to transform.
 * @param simpleData - Whether to use simple data.
 *
 * @returns - The tree nodes list.
 */
export function resourcesListToTreeNodes(resources: ResourcesList, simpleData: boolean = false): TreeNode[] {
    const createNodeData = (resource: string, resourceType: ResourceType): ResourceNodeData => {
        return {
            resource: resource,
            resourceType: resourceType,
            label: extractFilenameFromPath(resource)
        } as ResourceNodeData;
    };

    const sortNodes = (nodes: TreeNode[]): TreeNode[] => {
        return nodes.sort((node1, node2) => node1.label && node2.label ? node1.label.localeCompare(node2.label) : 0);
    };

    const folderNodes: TreeNode[] = [];
    for (const [_, folderResource] of Object.entries(resources.folders)) {
        folderNodes.push(...resourcesListToTreeNodes(folderResource!, simpleData));
    }

    const fileNodes: TreeNode[] = [];
    for (const fileResource of resources.files) {
        const nodeData = createNodeData(fileResource, ResourceType.File);
        fileNodes.push({
            key: nodeData.resource,
            label: nodeData.label,
            data: simpleData ? nodeData.resource : nodeData,
            icon: "material-icons-outlined mi-description"
        } as TreeNode);
    }

    const nodeData = createNodeData(resources.resource, ResourceType.Folder);
    return [{
        key: nodeData.resource,
        label: nodeData.label || "/",
        data: simpleData ? nodeData.resource : nodeData,
        icon: "material-icons-outlined mi-folder",
        children: [...sortNodes(folderNodes), ...sortNodes(fileNodes)]
    } as TreeNode];
}
