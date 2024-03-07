<script setup lang="ts">
import { storeToRefs } from "pinia";
import { computed, onUnmounted, unref } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { isUserTokenValid } from "@/authentication/UserToken";

const comp = FrontendComponent.inject();
const userStore = useUserStore();
const { userToken } = storeToRefs(userStore);

const authScheme = computed(() => comp.authenticationScheme);
const isLoggedIn = computed(() => isUserTokenValid(unref(userToken)));

onUnmounted(() => {
    // The app has been closed or refreshed; notify the authentication scheme about this
    authScheme.value.leave();
});
</script>

<template>
    <RouterView v-if="isLoggedIn" />
    <component v-else :is="authScheme.authComponent" :auth-scheme="authScheme" />
</template>

<style scoped lang="scss">

</style>
