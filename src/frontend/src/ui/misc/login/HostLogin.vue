<script setup lang="ts">
import { storeToRefs } from "pinia";
import { onMounted, ref } from "vue";

import Header from "@common/ui/views/main/states/Header.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { useHostIntegration } from "@/integration/HostIntegration";
import { useLogin } from "@/integration/Login";
import { createUserToken } from "@/integration/UserToken";

const comp = FrontendComponent.inject();
const userStore = useUserStore();
const { userToken } = storeToRefs(userStore);

const errorMessage = ref("");
onMounted(async () => {
    const { extractUserToken } = useHostIntegration(comp);
    const { login } = useLogin(comp);

    extractUserToken().then((userToken) => {
        login(createUserToken(userToken.userID, userToken.userName), undefined, (msg) => {
                errorMessage.value = msg;
            }
        );
    }).catch((error) => {
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
                <span class="material-icons-outlined mi-hourglass-empty animate-spin" style="font-size: 32px;" />
            </div>
        </div>
        <div v-else class="r-text-error italic">
            <span class="font-bold">An error occurred while logging in: </span><span>{{ errorMessage }}</span>
        </div>
    </div>
</template>

<style scoped lang="scss">

</style>
