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
    resultMessage: {
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
const { index, timestamp, message, resultMessage, project, connectorInstance, connectorCategory, severity, progress, closable, record } = toRefs(props);
const emits = defineEmits<{
    (e: "dismiss", record: number): void;
}>();
</script>

<template>
    <div class="grid grid-cols-[1fr_min-content]" :class="{ 'pt-2': index != 0 }">
        <InlineMessage :severity="severity" class="flex w-full justify-start group" :pt="{ text: '!w-full !text-sm', icon: 'place-self-start mt-3' }">
            <div>
                <div class="grid grid-cols-[1fr_min-content] grid-flow-col gap-2 w-full">
                    <div>
                        <div class="font-bold">
                            Your {{ connectorCategory?.verbNoun.toLowerCase() || "export" }} of <b>{{ project?.title || "Unknown project" }}</b> to
                            <b>{{ connectorInstance?.name || "Unknown connection" }}</b> {{ resultMessage }}
                        </div>
                        <div>{{ message }}</div>

                        <ProgressBar v-if="progress >= 0.0" class="h-3 mt-1 mb-1" :value="Math.trunc(progress * 100)" :pt="{ value: 'bg-current' }" />

                        <div class="pt-2 text-slate-500">
                            <span class="font-normal">{{ connectorCategory?.verbNoun || "Export" }} &#x2022; </span>
                            <span class="font-light text-xs">{{ formatLocaleTimestamp(timestamp) }}</span>
                        </div>
                    </div>

                    <div v-if="closable">
                        <Button
                            icon="material-icons-outlined mi-close"
                            severity="secondary"
                            rounded
                            text
                            size="small"
                            title="Dismiss"
                            class="-top-1 left-1.5 invisible"
                            :class="{ 'group-hover:visible': true }"
                            :pt="{ root: 'w-8 h-8', icon: '!text-lg' }"
                            @click="emits('dismiss', record)"
                        />
                    </div>
                    <div v-else class="w-0" />
                </div>
            </div>
        </InlineMessage>
    </div>
</template>

<style scoped lang="scss"></style>
