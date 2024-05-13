<script setup lang="ts">
import { provide, type PropType, watch, useAttrs, onMounted, onBeforeMount } from "vue";
import PropertySet from "./PropertySet.vue";
import PropertyDefaultSet from "./PropertyDefaultSet.vue";
import { Logger } from "./utils/Logging";

import { MetadataController, PropertyController, type S } from "./PropertyController";
import type { ExporterID } from "./exporters/Exporter";
import { PersistedSet } from "./PropertySet";
import { Profile } from "./PropertyProfile";
import { dataCite } from "./profiles/datacite";
import { PropertyProfileStore } from "@common/ui/components/propertyeditor/PropertyProfileStore";
import { ProjectObjectStore } from "@common/ui/components/propertyeditor/ProjectObjectStore";

const profiles: Profile = [dataCite as Profile];

const props = defineProps({
    projectProfiles: {
        type: PropertyProfileStore,
        required: true
    },
    projectObjects: {
        type: ProjectObjectStore,
        required: true
    }
});

/* const { controller, logging, project, exporters } = defineProps({
    controller: {
        type: Object as PropType<PropertyController<S>>,
        required: true
    },
    logging: {
        type: Object as PropType<Logger>,
        default: Logger
    },
    project: {
        type: Object as PropType<any>,
        default: null
    },
    exporters: {
        type: Array as PropType<ExporterID[]>,
        default: () => []
    }
});

provide("controller", controller);
provide("logging", logging);

const model = defineModel();

controller.mountPersistedSets(model.value as PersistedSet[]);

watch(
    () => model.value,
    () => {
        controller.mountPersistedSets(model.value as PersistedSet[]);
    },
    { deep: true }
);

watch(
    () => controller.exportData(),
    () => {
        model.value = controller.exportData();
    },
    { deep: true }
); */
</script>

<template>
    <div class="overflow-hidden">
        <!--         <PropertyDefaultSet v-if="controller instanceof MetadataController" :controller="controller" :project="project" :exporters="exporters" /> -->

        <div v-for="[i, profile] in projectProfiles.list().entries()" :class="i > 0 ? '!mt-5' : ''" class="mx-4 mt-4">
            <PropertySet :profile="profile" :projectObjects="projectObjects" :projectProfiles="projectProfiles" />
        </div>
    </div>
</template>
