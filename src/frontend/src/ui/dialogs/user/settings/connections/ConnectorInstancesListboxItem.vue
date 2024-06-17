<script setup lang="ts">
import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import Button from "primevue/button";
import Menu from "primevue/menu";
import Tag from "primevue/tag";
import { computed, defineAsyncComponent, type PropType, ref, toRefs, unref } from "vue";

import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { findConnectorByID } from "@common/data/entities/connector/ConnectorUtils";

import { useConnectorsStore } from "@/data/stores/ConnectorsStore";

import { AuthorizationStrategyUIsCatalog } from "@/ui/integration/authorization/strategies/AuthorizationStrategyUIsCatalog";

const consStore = useConnectorsStore();
const props = defineProps({
    instance: {
        type: Object as PropType<ConnectorInstance>,
        required: true,
    },
    isSelected: {
        type: Boolean,
        default: false,
    },
});
const emits = defineEmits<{
    (e: "edit-instance", instance: ConnectorInstance): void;
    (e: "delete-instance", instance: ConnectorInstance): void;
}>();

const { instance, isSelected } = toRefs(props);
const connector = computed(() => findConnectorByID(consStore.connectors, instance.value.connector_id));
const authStrategyUI = computed(() => {
    const strategy = unref(connector)!.authorization.strategy;
    if (!!strategy) {
        return AuthorizationStrategyUIsCatalog.findItem(strategy);
    }
    return undefined;
});
const authStrategyComponent = computed(() => {
    if (!!unref(authStrategyUI) && unref(authStrategyUI).hasIntegration) {
        return defineAsyncComponent(unref(authStrategyUI).options.integration!.loader);
    }
    return undefined;
});
const isAuthorized = computed(() => unref(authStrategyComponent) && unref(instance)!.authorization_state == AuthorizationState.Authorized);

const editMenu = ref();
const editMenuItems = computed(() => {
    const items = {
        label: "Edit connection",
        items: [
            {
                label: "Settings",
                icon: "material-icons-outlined mi-engineering",
                command: () => {
                    emits("edit-instance", instance!.value);
                },
            },
            { separator: true },
            {
                label: "Delete",
                icon: "material-icons-outlined mi-delete-forever",
                class: "r-text-error",
                command: () => {
                    emits("delete-instance", instance!.value);
                },
            },
        ],
    };

    if (!!unref(authStrategyUI) && unref(authStrategyUI).hasIntegration && unref(authStrategyUI).options.integration!.providesMenuEntry) {
        const menuItem = unref(authStrategyUI).getMenuEntry(unref(instance)!.authorization_state);
        if (!!menuItem) {
            items.items = [
                {
                    label: menuItem.label,
                    icon: menuItem.icon || "",
                    command: () => menuItem.command(unref(connector)!, unref(instance)!),
                },
                ...items.items,
            ];
        }
    }

    return [items];
});
const editMenuShown = ref(false);
</script>

<template>
    <div class="grid grid-rows-auto grid-cols-[min-content_1fr_min-content] grid-flow-row gap-0 place-content-start group">
        <div v-if="!!authStrategyComponent" class="row-span-3 pt-1 pr-2.5">
            <Tag rounded :severity="isAuthorized ? 'success' : 'danger'" :title="isAuthorized ? 'Connected' : 'Not connected'" class="w-10 h-10">
                <span class="material-icons-outlined" :class="isAuthorized ? 'mi-power' : 'mi-power-off'" />
            </Tag>
        </div>
        <div v-else class="row-span-3" />

        <div :id="'connector-instance-' + instance!.instance_id" class="r-text-caption h-6 truncate" :title="instance!.name">{{ instance!.name }}</div>

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
                    <span class="material-icons-outlined mi-more-vert" :class="[isSelected ? 'r-highlight-text' : 'r-text']" style="font-size: 32px" />
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

        <div class="truncate" :title="instance!.description">{{ instance!.description }}</div>

        <div class="col-span-2 items-center">
            <component v-if="!!authStrategyComponent" :is="authStrategyComponent" :connector="connector" :connector-instance="instance" />
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
