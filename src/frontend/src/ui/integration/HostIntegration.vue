<script setup lang="ts">
import { onMounted, type PropType, ref, toRefs, unref } from "vue";

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
const { getHostUserToken, getHostAuthorization } = useHostIntegration(comp);

const statusMessage = ref("Initializing [0/2]");
const errorMessage = ref("");

function performAuthentication(): void {
    statusMessage.value = "Authenticating [1/2]";

    getHostUserToken()
        .then((userToken) => {
            unref(scheme)!
                .authenticator(userToken)
                .done(() => performAuthorization())
                .failed((msg) => {
                    errorMessage.value = msg;
                })
                .authenticate();
        })
        .catch((error) => {
            errorMessage.value = error;
        });
}

function performAuthorization(): void {
    statusMessage.value = "Authorizing [2/2]";

    getHostAuthorization()
        .then((hostAuth) => {
            unref(scheme)!.authorizer().authorize();
        })
        .catch((error) => {
            errorMessage.value = error;
        });
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
            <span class="font-bold">An error occurred while logging in ({{ statusMessage }}): </span><span>{{ errorMessage }}</span>
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
