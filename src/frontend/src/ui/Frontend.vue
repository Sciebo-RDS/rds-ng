<script setup lang="ts">
import { storeToRefs } from "pinia";
import { computed, unref } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { isUserTokenValid } from "@/authentication/UserToken";

const comp = FrontendComponent.inject();
const userStore = useUserStore();
const { userToken } = storeToRefs(userStore);

const authScheme = computed(() => comp.authenticationScheme);
const isLoggedIn = computed(() => isUserTokenValid(unref(userToken)));
</script>

<template>
    <RouterView v-if="isLoggedIn" />
    <component v-else :is="authScheme.authComponent" :auth-scheme="authScheme" />
</template>

<style scoped lang="scss">

</style>
