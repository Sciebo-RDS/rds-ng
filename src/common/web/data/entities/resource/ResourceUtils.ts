import { TreeNode } from "primevue/treenode";

import { ResourcesList } from "./ResourcesList";
import { extractFilenameFromPath } from "../../../utils/Paths";

/**
 * Transforms a `ResourcesList` into a Vue *TreeNode*.
 *
 * @param resources - The resources list to transform.
 *
 * @returns - The tree nodes list.
 */
export function resourcesListToTreeNodes(resources: ResourcesList): TreeNode[] {
    const sortNodes = (nodes: TreeNode[]): TreeNode[] => {
        return nodes.sort((node1, node2) => node1.label.localeCompare(node2.label));
    };

    const folderNodes: TreeNode[] = [];
    for (const [_, folderResource] of Object.entries(resources.folders)) {
        folderNodes.push(...resourcesListToTreeNodes(folderResource));
    }

    const fileNodes: TreeNode[] = [];
    for (const fileResource of resources.files) {
        fileNodes.push({
            key: fileResource,
            label: extractFilenameFromPath(fileResource),
            data: fileResource,
            icon: "material-icons-outlined mi-description"
        } as TreeNode);
    }

    return [{
        key: resources.resource,
        label: extractFilenameFromPath(resources.resource) || "/",
        data: resources.resource,
        icon: "material-icons-outlined mi-folder",
        children: [...sortNodes(folderNodes), ...sortNodes(fileNodes)]
    } as TreeNode];
}
