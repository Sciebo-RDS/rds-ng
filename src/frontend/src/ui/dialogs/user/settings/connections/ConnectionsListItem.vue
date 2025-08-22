<script setup lang="ts">
import { storeToRefs } from "pinia";
import Button from "primevue/button";
import Menu from "primevue/menu";
import Tag from "primevue/tag";
import { computed, type PropType, ref, toRefs, unref, watch } from "vue";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { connectorInstanceIsAuthorized } from "@common/data/entities/connector/ConnectorInstanceUtils";
import { connectorRequiresAuthorization, findConnectorByID } from "@common/data/entities/connector/ConnectorUtils";

import { useConnectorsStore } from "@/data/stores/ConnectorsStore";
import { useUserStore } from "@/data/stores/UserStore";

const consStore = useConnectorsStore();
const userStore = useUserStore();
const props = defineProps({
    instance: {
        type: Object as PropType<ConnectorInstance>,
        required: true
    },
    isNew: {
        type: Boolean,
        default: false
    }
});
const emits = defineEmits<{
    (e: "authorize-instance", instance: ConnectorInstance): void;
    (e: "unauthorize-instance", instance: ConnectorInstance): void;
    (e: "edit-instance", instance: ConnectorInstance): void;
    (e: "delete-instance", instance: ConnectorInstance): void;
}>();

const { instance, isNew } = toRefs(props);
const { userAuthorizations } = storeToRefs(userStore);

const connector = computed(() => findConnectorByID(consStore.connectors, instance.value.connector_id));
const requiresAuthorization = computed(() => (!!unref(connector) ? connectorRequiresAuthorization(unref(connector)!) : false));
const isAuthorized = computed(() => connectorInstanceIsAuthorized(unref(instance)!, unref(userAuthorizations)));
const isUnAuthorizing = ref(false);

const editMenu = ref();
const editMenuItems = computed(() => {
    const menuItems = {
        label: "Edit connection",
        items: [] as Record<any, any>[]
    };

    if (unref(requiresAuthorization)) {
        if (unref(isAuthorized)) {
            menuItems.items.push({
                label: () => (unref(isUnAuthorizing) ? `Disconnecting from ${unref(instance).name}...` : `Disconnect from ${unref(instance).name}`),
                icon: "material-icons-outlined mi-link-off",
                disabled: () => unref(isUnAuthorizing),
                command: onUnauthorize
            });
        } else {
            menuItems.items.push({
                label: () => (unref(isUnAuthorizing) ? `Connecting to ${unref(instance).name}...` : `Connect to ${unref(instance).name}`),
                icon: "material-icons-outlined mi-link",
                disabled: () => unref(isUnAuthorizing),
                command: onAuthorize
            });
        }
    }

    menuItems.items.push(
        {
            label: "Connection settings",
            icon: "material-icons-outlined mi-settings",
            command: () => emits("edit-instance", unref(instance)!)
        },
        { separator: true },
        {
            label: "Delete connection",
            icon: "material-icons-outlined mi-delete-forever",
            class: "r-text-error",
            command: () => emits("delete-instance", unref(instance)!)
        }
    );

    return [menuItems];
});
const editMenuShown = ref(false);

function onAuthorize(): void {
    isUnAuthorizing.value = true;
    emits("authorize-instance", unref(instance)!);
}

function onUnauthorize(): void {
    isUnAuthorizing.value = true;
    emits("unauthorize-instance", unref(instance)!);
}

// Whenever any authorization state changes, any pending (un)authorizations have completed
watch(userAuthorizations, () => {
    isUnAuthorizing.value = false;
});

// If the new state changes, we're automatically performing a connect operation
watch(isNew, (newValue) => {
    if (newValue) {
        isUnAuthorizing.value = true;
    }
});
</script>

<template>
    <div class="grid grid-rows-auto grid-cols-[min-content_1fr_min-content_min-content] gap-2.5 place-content-start content-center items-center w-full">
        <div :class="{ 'pt-1': instance!.description }">
            <Tag
                :severity="isAuthorized || !requiresAuthorization ? 'success' : 'danger'"
                :title="isAuthorized || !requiresAuthorization ? 'Connected' : 'Not connected'"
                class="w-10 h-10 rounded-full"
            >
                <span class="material-icons-outlined" :class="isAuthorized ? 'mi-link' : 'mi-link-off'" />
            </Tag>
        </div>

        <div class="grid grid-flow-row content-center">
            <div :id="'connector-instance-' + instance!.instance_id" class="r-text-caption h-6 truncate" :title="instance!.name">{{ instance!.name }}</div>
            <div v-if="instance!.description" class="truncate" :title="instance!.description">{{ instance!.description }}</div>
        </div>

        <div v-if="requiresAuthorization">
            <Button
                v-if="isAuthorized"
                :label="isUnAuthorizing ? 'Disconnecting...' : 'Disconnect'"
                size="small"
                icon="material-icons-outlined mi-link-off"
                class="r-button-small"
                :loading="isUnAuthorizing"
                @click="onUnauthorize"
            />
            <Button
                v-else
                :label="isUnAuthorizing ? 'Connecting...' : 'Connect'"
                size="small"
                icon="material-icons-outlined mi-link"
                class="r-button-small"
                :loading="isUnAuthorizing"
                @click="onAuthorize"
            />
        </div>
        <div v-else>&nbsp;</div>

        <div class="r-centered-grid">
            <Button
                text
                rounded
                size="small"
                aria-label="Options"
                title="More options"
                class="opacity-60 hover:opacity-100"
                @click="(event) => editMenu.toggle(event)"
            >
                <template #icon>
                    <span class="material-icons-outlined mi-more-vert r-text" style="font-size: 32px" />
                </template>
            </Button>
            <Menu
                ref="editMenu"
                :model="editMenuItems"
                :base-z-index="Number.MAX_SAFE_INTEGER"
                popup
                @focus="editMenuShown = true"
                @blur="editMenuShown = false"
            />
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
