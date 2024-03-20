<script setup lang="ts">
import BlockUI from "primevue/blockui";
import Button from "primevue/button";
import IconField from "primevue/iconfield";
import InputIcon from "primevue/inputicon";
import InputText from "primevue/inputtext";
import { type PropType, ref, toRefs } from "vue";

import { useDirectives } from "@common/ui/Directives";

import { AuthenticationScheme } from "@/authentication/AuthenticationScheme";
import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";

const comp = FrontendComponent.inject();
const props = defineProps({
    authScheme: {
        type: Object as PropType<AuthenticationScheme>,
        required: true
    }
});
const { authScheme } = toRefs(props);
const userStore = useUserStore();
const { vFocus } = useDirectives();

const userName = ref("");
const blockInput = ref(false);
const errorMessage = ref("");

function performLogin(): void {
    blockInput.value = true;
    errorMessage.value = "";

    authScheme!.value.authenticator(userName.value).done(() => {
        blockInput.value = false;
    }).failed((msg) => {
        blockInput.value = false;
        errorMessage.value = msg;
    }).authenticate();
}
</script>

<template>
    <div class="r-centered-grid grid-cols-[auto_32rem_auto] grid-flow-row mt-2">
        <div></div>
        <BlockUI class="r-centered-grid grid-cols-1 grid-flow-row w-full p-10" :blocked="blockInput">
            <img src="@assets/img/rds_ng-octopus-blue.png" alt="RDS-NG Logo" class="logo">
            <form @submit.prevent="performLogin" class="r-form w-full">
                <span>
                    <label>Enter your username:</label>
                    <IconField iconPosition="left">
                        <InputIcon>
                            <i class="material-icons-outlined mi-account-circle mt-[-4px]" />
                        </InputIcon>
                        <InputText v-model.trim="userName" placeholder="Username" v-focus class="w-full" />
                    </IconField>
                </span>

                <Button
                    label="Login"
                    icon="material-icons-outlined mi-login"
                    size="large"
                    :loading="blockInput"
                    loadingIcon="material-icons-outlined mi-refresh animate-spin"
                    @click="performLogin"
                />
            </form>

            <div v-if="errorMessage" class="r-text-error mt-2"><b>Unable to login:</b> {{ errorMessage }}</div>

            <div class="r-text-light mt-10">
                The RDS-NG system usually does not provide user accounts on its own.
                For testing purposes, however, a simple account mechanism has been added.
                Simply enter a username of your choice; the data you're working with will then be tied to this name.
            </div>
        </BlockUI>
        <div></div>
    </div>
</template>

<style scoped lang="scss">

</style>
