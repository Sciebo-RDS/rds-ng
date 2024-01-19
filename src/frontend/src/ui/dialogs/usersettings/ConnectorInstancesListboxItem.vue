<script setup lang="ts">
import Button from "primevue/button";
import Menu from "primevue/menu";
import { ref, toRefs } from "vue";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { findConnectorByID } from "@common/data/entities/connector/ConnectorUtils";

import { useConnectorsStore } from "@/data/stores/ConnectorsStore";

const consStore = useConnectorsStore();
const props = defineProps({
    instance: {
        type: ConnectorInstance,
        required: true
    },
    isSelected: {
        type: Boolean,
        default: false
    }
});
const emits = defineEmits<{
    (e: "edit-instance", instance: ConnectorInstance): void;
    (e: "delete-instance", instance: ConnectorInstance): void;
}>();

const { instance, isSelected } = toRefs(props);
const connector = findConnectorByID(consStore.connectors, instance.value.connector_id);

const editMenu = ref();
const editMenuItems = ref([
    {
        label: "Edit connection",
        items: [
            {
                label: "Settings",
                icon: "material-icons-outlined mi-engineering",
                command: () => {
                    emits("edit-instance", instance!.value);
                }
            },
            { separator: true },
            {
                label: "Delete",
                icon: "material-icons-outlined mi-delete-forever",
                class: "r-text-error",
                command: () => {
                    emits("delete-instance", instance!.value);
                }
            }
        ]
    }
]);
const editMenuShown = ref(false);
</script>

<template>
    <div class="grid grid-rows-auto grid-cols-[1fr_min-content] grid-flow-row gap-0 place-content-start group">
        <div class="r-text-caption h-6 truncate" :title="instance!.name">{{ instance!.name }}</div>

        <div class="row-span-2 pl-1">
            <Button
                text
                rounded
                size="small"
                aria-label="Options"
                title="More options"
                :class="{ invisible: !editMenuShown, 'group-hover:visible': true }"
                @click="(event) => editMenu.toggle(event)"
            >
                <template #icon>
                    <span class="material-icons-outlined mi-more-vert" :class="[isSelected ? 'r-primary-text' : 'r-text']" style="font-size: 32px" />
                </template>
            </Button>
            <Menu ref="editMenu" :model="editMenuItems" :base-z-index="Number.MAX_SAFE_INTEGER" popup @focus="editMenuShown = true" @blur="editMenuShown = false" :pt="{
                root: 'coninst-popup-menu'
            }" />
        </div>

        <div class="truncate" :title="instance!.description">{{ instance!.description }}</div>

        <div class="grid grid-cols-[1fr_max-content] grid-flow-col pt-5 col-span-2">
            <span>
                <b>Status: </b>
                <span class="italic">
                    <span v-if="connector">We don't have that yet...</span>
                    <span v-else class="r-text-error">Connector not found</span>
                </span>
            </span>
            <img v-if="connector && connector.logos.horizontal_logo" :src="connector.logos.horizontal_logo" class="h-4 opacity-50" alt="{{ connector.name }}" :title="connector.name" />
        </div>
    </div>
</template>

<style scoped lang="scss">
:deep(.coninst-popup-menu) {
    @apply w-96 #{!important};
}
</style>
