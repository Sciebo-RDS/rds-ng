import { defineStore } from "pinia";
import { ref, unref } from "vue";

import { Connector } from "../entities/connector/Connector";
import { type MetadataProfileContainerList } from "../entities/metadata/MetadataProfileContainer";
import { MetadataProfileContainerRole } from "../entities/metadata/MetadataProfileContainer";
import { filterContainersByRole } from "../entities/metadata/MetadataProfileContainerUtils";

/**
 * The global store for auto-assigned colors.
 */
export const useColorsStore = defineStore("colorsStore", () => {
    const colorIDsTable = ref([] as string[]);

    function color(colorID: string, lightness: number = 90, amount: number = 25, alpha: number = 1.0): string {
        if (unref(colorIDsTable).indexOf(colorID) == -1) {
            unref(colorIDsTable).push(colorID);
        }
        const index = unref(colorIDsTable).indexOf(colorID);
        return `lch(${lightness} ${amount} ${(360.0 / Math.max(5, unref(colorIDsTable).length)) * index} / ${alpha})`;
    }

    function populateFromProfileContainerList(profiles: MetadataProfileContainerList): void {
        filterContainersByRole(profiles, MetadataProfileContainerRole.Global)
            .sort((p1, p2) => p1.profile.metadata.id[0].localeCompare(p2.profile.metadata.id[0]))
            .forEach((profile) => color(profile.profile.metadata.id[0]));
    }

    function populateFromConnectorsList(connectors: Connector[]): void {
        connectors
            .sort((con1, con2) => con1.name.localeCompare(con2.name))
            .forEach((connector) => {
                try {
                    const profileID = connector.metadata_profile.metadata.id[0];
                    color(profileID);
                } catch (e) {
                    // Just ignore any exceptions
                }
            });
    }

    function reset(): void {
        colorIDsTable.value = [] as string[];
    }

    return {
        color,
        populateFromProfileContainerList,
        populateFromConnectorsList,
        reset
    };
});
