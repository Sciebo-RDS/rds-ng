<script setup lang="ts">
import { HostCommuncationAction, sendActionToHost } from "@common/integration/HostCommunication.ts";
import ExternalLink from "@common/ui/components/misc/ExternalLink.vue";
import Button from "primevue/button";
import { onMounted, type PropType, ref, toRefs, unref } from "vue";

import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { AuthorizationRequest } from "@common/integration/authorization/AuthorizationRequest.ts";
import Header from "@common/ui/views/main/states/Header.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useHostIntegration } from "@/integration/HostIntegration";
import { IntegrationScheme } from "@/integration/IntegrationScheme";

const comp = FrontendComponent.inject();
const props = defineProps({
    scheme: {
        type: Object as PropType<IntegrationScheme>,
        required: true
    }
});
const { scheme } = toRefs(props);
const { getHostUserToken, getHostAuthorizationSettings, getHostResources } = useHostIntegration(comp);

const requiresAuth = ref(false);
const authFingerprint = ref("");

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

    if (authState == AuthorizationState.NotAuthorized && !AuthorizationRequest.requestIssued()) {
        requiresAuth.value = true;
        authFingerprint.value = fingerprint;
    } else {
        executeAuthorization(authState, fingerprint);
    }
}

function executeAuthorization(authState: AuthorizationState, fingerprint: string): void {
    getHostAuthorizationSettings()
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

function reloadApp() {
    sendActionToHost(HostCommuncationAction.Reload);
}

onMounted(async () => performAuthentication());
</script>

<template>
    <div class="r-centered-grid r-text mb-8">
        <Header />

        <div v-if="!!errorMessage" class="text-center">
            <div class="r-text-error">
                <span class="font-bold">
                    An error occurred while logging in <span class="r-text-light">({{ statusMessage }})</span>:
                </span>
                <span>{{ errorMessage }}</span>
            </div>
            <div>&nbsp;</div>
            <div>
                Please <a href="#" @click.prevent="reloadApp" class="r-text-link">refresh</a> your browser to try again. If this error persists,
                <ExternalLink link="mailto:sciebo.rds@uni-muenster.de" text="send us an email" />
                describing the error.
            </div>
        </div>
        <div v-else-if="requiresAuth">
            <div class="r-centered-grid content max-w-[55rem]">
                <div>
                    <h2 class="text-3xl font-extrabold">Welcome to {{ comp.data.title }}!</h2>
                </div>
                <div>I'm your helpful assistant for secure FAIR-aligned research data sharing – and I help you to prepare, annotate, and share your data.</div>
                <div>
                    <strong>Secure cloud access</strong><br />
                    To get started, I need access to your files stored in your cloud account. This is necessary in order for me to be able to display your files
                    and upload them to the target services. But no worries, your files stay safe, unchanged, and private.
                </div>
                <div class="font-semibold">
                    Click below to authorize access and start your data sharing project! Once granted, you’ll be redirected to the
                    {{ comp.data.title }} application and are ready to start.
                </div>
                <div>&nbsp;</div>
                <Button
                    size="large"
                    severity="warn"
                    icon="material-icons-outlined mi-verified-user"
                    :label="`Authorize ${comp.data.title}`"
                    @click="() => executeAuthorization(AuthorizationState.NotAuthorized, authFingerprint)"
                />
            </div>
        </div>
        <div v-else>
            <div class="r-centered-grid">
                <div>
                    <span class="italic">
                        Logging in, please wait <span class="r-text-light">({{ statusMessage }})</span>...
                    </span>
                </div>
                <div>
                    <span class="material-icons-outlined mi-hourglass-empty animate-spin" style="font-size: 32px" />
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
.content div {
    @apply mb-4;
}
</style>
