<script setup lang="ts">
import { provide, type PropType, watch, useAttrs, toRefs } from "vue";
import PropertySet from "./PropertySet.vue";
import PropertyDefaultSet from "./PropertyDefaultSet.vue";
import InlineMessage from "primevue/inlinemessage";
import { Logger } from "./utils/Logging";
import { PropertyController } from "@common/ui/components/propertyeditor/PropertyController";
import type { ExporterID } from "./exporters/Exporter";

const emit = defineEmits(["update"]);
const { controller, logging, project, exporters } = defineProps({
    controller: {
        type: Object as PropType<PropertyController<any>>,
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

if (controller.getProfileIds().length) {
    logging.info(`Loaded ${controller.getProfileIds().length} profiles: ${JSON.stringify(controller.getProfileIds())}`, "propertyeditor");
} else {
    logging.warning(`Could not load any metadata Profiles.`, "propertyeditor");
}

watch(controller.setsToWatch(), () => {
    emit("update", controller.exportData());
});
</script>

<template>
    <div class="overflow-hidden">
        <PropertyDefaultSet v-if="controller.defaultSet" :controller="controller" :project="project" :exporters="exporters" />
        <div v-for="[i, profileId] of controller.getProfileIds().entries()" :class="i > 0 ? '!mt-5' : ''">
            <PropertySet :controller="controller" :project="project" :exporters="exporters" :profileId="profileId" />
        </div>
        <div v-show="!controller.getProfileIds().length" class="flex justify-center text-2xl w-full">
            <InlineMessage class="text-2xl" severity="error">Could not load any metadata profiles</InlineMessage>
        </div>
    </div>
</template>
