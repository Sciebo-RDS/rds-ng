<script setup lang="ts">
import { storeToRefs } from "pinia";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import { ref } from "vue";

import { useDirectives } from "@common/ui/Directives";

import { useUserStore } from "@/data/stores/UserStore";

const userStore = useUserStore();
const { userToken } = storeToRefs(userStore);
const { vFocus } = useDirectives();

const userName = ref("");

function performLogin(): void {
    userToken.value = userName.value;
}
</script>

<template>
    <div class="r-centered-grid grid-cols-[auto_30rem_auto] grid-flow-row">
        <div></div>
        <div class="r-centered-grid grid-cols-1 grid-flow-row w-full">
            <img src="@assets/img/rds_ng-octopus-blue.png" alt="RDS-NG Logo" class="logo">
            <form @submit.prevent="performLogin" class="r-form w-full">
                <span>
                    <label>Enter your username:</label>
                    <span class="p-input-icon-left r-form-field">
                        <i class="material-icons-outlined mi-account-circle mt-[-12px]" />
                        <InputText v-model="userName" placeholder="Username" v-focus />
                    </span>
                </span>
                <Button label="Login" icon="material-icons-outlined mi-login" size="large" @click="performLogin" />
            </form>

            <div class="r-text-light mt-10">
                The RDS-NG system usually does not provide user accounts on its own.
                For testing purposes, however, a simple account mechanism has been added.
                Simply enter a username of your choice; the data you're working with will then be tied to this name.
            </div>
        </div>
        <div></div>
    </div>
</template>

<style scoped lang="scss">

</style>
