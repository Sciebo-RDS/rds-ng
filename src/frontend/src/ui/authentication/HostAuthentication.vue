<script setup lang="ts">
import { onMounted, type PropType, ref, toRefs, unref } from "vue";

import Header from "@common/ui/views/main/states/Header.vue";

import { AuthenticationScheme } from "@/authentication/AuthenticationScheme";
import { FrontendComponent } from "@/component/FrontendComponent";
import { useHostIntegration } from "@/integration/HostIntegration";

const comp = FrontendComponent.inject();
const props = defineProps({
    authScheme: {
        type: Object as PropType<AuthenticationScheme>,
        required: true,
    },
});
const { authScheme } = toRefs(props);

const errorMessage = ref("");
onMounted(async () => {
    const { extractUserToken } = useHostIntegration(comp);

    extractUserToken()
        .then((userToken) => {
            unref(authScheme)!
                .authenticator(userToken)
                .failed((msg) => {
                    errorMessage.value = msg;
                })
                .authenticate();
        })
        .catch((error) => {
            errorMessage.value = error;
        });
});
</script>

<template>
    <div class="r-centered-grid r-text">
        <Header></Header>
        <div v-if="!errorMessage" class="r-centered-grid">
            <div>
                <span class="italic">Logging in, please wait...</span>
            </div>
            <div>
                <span class="material-icons-outlined mi-hourglass-empty animate-spin" style="font-size: 32px" />
            </div>
        </div>
        <div v-else class="r-text-error italic">
            <span class="font-bold">An error occurred while logging in: </span><span>{{ errorMessage }}</span>
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
