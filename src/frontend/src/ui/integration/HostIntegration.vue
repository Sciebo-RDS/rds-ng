<script setup lang="ts">
import { error } from "@common/core/logging/Logging";
import { onMounted, type PropType, ref, toRefs, unref } from "vue";

import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import Header from "@common/ui/views/main/states/Header.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { IntegrationScheme } from "@/integration/IntegrationScheme";
import { useHostIntegration } from "@/integration/HostIntegration";

const comp = FrontendComponent.inject();
const props = defineProps({
    scheme: {
        type: Object as PropType<IntegrationScheme>,
        required: true,
    },
});
const { scheme } = toRefs(props);
const { getHostUserToken, getHostAuthorization, getHostResources } = useHostIntegration(comp);

const statusMessage = ref("0/3: Initializing");
const errorMessage = ref("");

function performAuthentication(): void {
    statusMessage.value = "1/3: Authenticating";

    getHostUserToken()
        .then((userToken) => {
            unref(scheme)!.authenticator(userToken).done(performAuthorization).failed(showError).authenticate();
        })
        .catch(showError);
}

function performAuthorization(authState: AuthorizationState, fingerprint: string): void {
    statusMessage.value = "2/3: Authorizing";

    getHostAuthorization()
        .then((hostAuth) => {
            unref(scheme)!.authorizer(hostAuth).done(performBrokerAssignment).failed(showError).authorize(authState, fingerprint);
        })
        .catch(showError);
}

function performBrokerAssignment(): void {
    statusMessage.value = "3/3: Broker assignment";

    getHostResources()
        .then((hostResources) => {
            unref(scheme)!.resourcesBroker(hostResources).failed(showError).assign();
        })
        .catch(showError);
}

function showError(error: string): void {
    errorMessage.value = error;
}

onMounted(async () => performAuthentication());
</script>

<template>
    <div class="r-centered-grid r-text">
        <Header></Header>
        <div v-if="!errorMessage" class="r-centered-grid">
            <div>
                <span class="italic">
                    Logging in, please wait <span class="r-text-light">({{ statusMessage }})</span>...
                </span>
            </div>
            <div>
                <span class="material-icons-outlined mi-hourglass-empty animate-spin" style="font-size: 32px" />
            </div>
        </div>
        <div v-else class="r-text-error italic">
            <span class="font-bold">
                An error occurred while logging in <span class="r-text-light">({{ statusMessage }})</span>:
            </span>
            <span>{{ errorMessage }}</span>
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
