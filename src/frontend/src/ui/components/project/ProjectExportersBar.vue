<script setup lang="ts">
import Button from "primevue/button";
import ButtonGroup from "primevue/buttongroup";
import { computed } from "vue";

import { useProjectExportersStore } from "@/data/stores/ProjectExportersStore";

const props = defineProps({
    scope: {
        type: String,
        default: ""
    }
});

const { exporters } = useProjectExportersStore();

const availableExporters = computed(() => exporters.filter((exporter) => props.scope == "" || exporter.scope.includes(props.scope)).sort());
</script>

<template>
    <div v-if="availableExporters.length > 0" class="grid grid-flow-col gap-1.5 items-center p-0 text-xs">
        <span class="flex items-center gap-0.5 text-sm">
            <span class="material-icons-outlined mi-file-download" />
            <span class="font-bold pr-1">Export</span>
        </span>
        <ButtonGroup>
            <Button v-for="exporter in availableExporters" :label="exporter.name" :title="exporter.description" size="small" />
        </ButtonGroup>
    </div>
</template>

<style scoped lang="scss"></style>
