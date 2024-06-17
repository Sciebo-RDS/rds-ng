<script setup lang="ts">
import Button from "primevue/button";
import { computed, type PropType, toRefs, unref } from "vue";

import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { OAuth2Strategy } from "@common/integration/authorization/strategies/oauth2/OAuth2Strategy";
import { requestConnectorInstanceAuthorization, revokeConnectorInstanceAuthorization } from "@common/integration/authorization/AuthorizationUtils";

const props = defineProps({
    connector: {
        type: Object as PropType<Connector>,
        required: true,
    },
    connectorInstance: {
        type: Object as PropType<ConnectorInstance>,
        required: true,
    },
});
const { connector, connectorInstance } = toRefs(props);

const isAuthorized = computed(() => unref(connectorInstance)!.authorization_state == AuthorizationState.Authorized);

function onConnect() {
    requestConnectorInstanceAuthorization(OAuth2Strategy.Strategy, unref(connector)!, unref(connectorInstance)!);
}

function onDisconnect() {
    revokeConnectorInstanceAuthorization(OAuth2Strategy.Strategy, unref(connector)!, unref(connectorInstance)!);
}
</script>

<template>
    <div class="grid grid-cols-[1fr_min-content] !text-sm">
        <span />
        <Button
            v-if="isAuthorized"
            label="Disconnect"
            severity="warning"
            size="small"
            rounded
            icon="material-icons-outlined mi-link-off"
            class="r-button-small"
            @click="onDisconnect"
        />
        <Button v-else label="Connect" severity="info" size="small" rounded icon="material-icons-outlined mi-link" class="r-button-small" @click="onConnect" />
    </div>
</template>

<style scoped lang="scss"></style>
