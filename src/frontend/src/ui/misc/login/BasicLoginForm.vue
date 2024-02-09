<script setup lang="ts">
import { storeToRefs } from "pinia";
import BlockUI from "primevue/blockui";
import Button from "primevue/button";
import IconField from "primevue/iconfield";
import InputIcon from "primevue/inputicon";
import InputText from "primevue/inputtext";
import { ref, unref } from "vue";

import { useDirectives } from "@common/ui/Directives";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { SetSessionValueAction } from "@/ui/actions/session/SetSessionValueAction";

const comp = FrontendComponent.inject();
const userStore = useUserStore();
const { userToken } = storeToRefs(userStore);
const { vFocus } = useDirectives();

const userName = ref("");
const blockInput = ref(false);
const errorMessage = ref("");

function performLogin(): void {
    blockInput.value = true;
    errorMessage.value = "";


    const token = unref(userName.value);
    const action = new SetSessionValueAction(comp, true);
    action.prepare("user-token", token).done((_, success, msg) => {
        // Wait till the server has actually stored the user token
        blockInput.value = false;

        if (success) {
            userToken.value = token;
        } else {
            errorMessage.value = msg;
        }
    }).failed((_, msg: string) => {
        blockInput.value = false;
        errorMessage.value = msg;
    });
    action.execute();
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
                            <i class="material-icons-outlined mi-account-circle mt-[-12px]" />
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
