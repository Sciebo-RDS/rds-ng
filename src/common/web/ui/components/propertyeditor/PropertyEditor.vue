<script setup lang="ts">
import { provide, type PropType, watch, useAttrs } from "vue";
import PropertySet from "./PropertySet.vue";
import PropertyDefaultSet from "./PropertyDefaultSet.vue";
import { Logger } from "./utils/Logging";

import { MetadataController, PropertyController, type S } from "./PropertyController";
import type { ExporterID } from "./exporters/Exporter";
import { PersistedSet } from "./PropertySet";

const emit = defineEmits(["update"]);
const { controller, logging, project, exporters } = defineProps({
    controller: {
        type: Object as PropType<PropertyController<S>>,
        required: true,
    },
    logging: {
        type: Object as PropType<Logger>,
        default: Logger,
    },
    project: {
        type: Object as PropType<any>,
        default: null,
    },
    exporters: {
        type: Array as PropType<ExporterID[]>,
        default: () => [],
    },
});

const cols = (attr: {}) => {
    return "twoCol" in attr && !("oneCol" in attr) ? "twoCol" : "oneCol";
};

const attrs = useAttrs();

provide("controller", controller);
provide("logging", logging);
provide("cols", cols(attrs));

const model = defineModel();

controller.mountPersistedSets(model.value as PersistedSet[]);

watch(
    () => model.value,
    (nM) => {
        controller.mountPersistedSets(model.value as PersistedSet[]);
    },
    { deep: true },
);

watch(
    () => controller.exportData(),
    () => {
        model.value = controller.exportData();
    },
    { deep: true },
);
</script>

<template>
    <div class="overflow-hidden">
        <PropertyDefaultSet v-if="controller instanceof MetadataController" :controller="controller" :project="project" :exporters="exporters" />

        <div v-for="[i, profileId] of controller.getProfileIds().entries()" :class="i > 0 ? '!mt-5' : ''">
            <PropertySet :controller="controller" :project="project" :exporters="exporters" :profileId="profileId" />
        </div>
    </div>
</template>
