<script setup lang="ts">
import Button from "primevue/button";
import InlineMessage from "primevue/inlinemessage";
import ProgressBar from "primevue/progressbar";
import { type PropType, toRefs } from "vue";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { Project } from "@common/data/entities/project/Project";
import { formatLocaleTimestamp } from "@common/utils/Strings";

import { ConnectorCategory } from "@/data/entities/connector/categories/ConnectorCategory";

const props = defineProps({
    index: {
        type: Number,
        required: true,
    },
    timestamp: {
        type: Number,
        required: true,
    },
    message: {
        type: String,
        required: true,
    },
    project: {
        type: Object as PropType<Project>,
    },
    connectorInstance: {
        type: Object as PropType<ConnectorInstance>,
    },
    connectorCategory: {
        type: Object as PropType<ConnectorCategory>,
    },
    severity: {
        type: String,
        default: "info",
    },
    progress: {
        type: Number,
        default: -1.0,
    },
    closable: {
        type: Boolean,
        default: false,
    },
    record: {
        type: Number,
        default: 0,
    },
});
const { index, timestamp, message, project, connectorInstance, connectorCategory, severity, progress, closable, record } = toRefs(props);
const emits = defineEmits<{
    (e: "dismiss", record: number): void;
}>();
</script>

<template>
    <div class="grid grid-cols-[1fr_min-content] px-1 group" :class="{ 'pt-2': index != 0 }">
        <InlineMessage :severity="severity" class="flex w-full justify-start" :pt="{ text: 'w-full !text-sm' }">
            <div>
                <div class="grid grid-cols-[1fr_auto] items-center text-gray-700 mb-1 w-full">
                    <div class="font-normal">{{ connectorCategory?.verbNoun || "Export" }}</div>
                    <div class="mr-2 font-light text-xs">{{ formatLocaleTimestamp(timestamp) }}</div>
                </div>
                <div class="font-bold">
                    {{ project?.title || "Unknown project" }} &rarr;
                    {{ connectorInstance?.name || "Unknown connection" }}
                </div>
                <div>{{ message }}</div>

                <ProgressBar v-if="progress >= 0.0" class="h-3 mt-2" :value="Math.trunc(progress * 100)" :pt="{ value: 'bg-current' }" />
            </div>
        </InlineMessage>

        <div class="ml-1.5 mt-0.5 invisible" :class="{ 'group-hover:visible': closable }">
            <Button
                icon="material-icons-outlined mi-close"
                severity="secondary"
                rounded
                outlined
                size="small"
                title="Dismiss"
                :pt="{ root: 'w-8 h-8', icon: '!text-lg' }"
                @click="emits('dismiss', record)"
            />
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
