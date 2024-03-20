<script setup lang="ts">
import { onMounted, onUnmounted, ref, shallowRef, watch } from "vue";
import { RouterView } from "vue-router";

import { FrontendComponent } from "@/component/FrontendComponent";

const comp = FrontendComponent.inject();
const authScheme = shallowRef(comp.authenticationScheme);
const isAuthenticated = ref(authScheme.value.isAuthenticated);

// Circumvent Vue warnings arising from using AuthorizationScheme.isAuthenticated directly
watch(() => authScheme.value.isAuthenticated, (authenticated) => {
    isAuthenticated.value = authenticated;
});

onMounted(() => {
    // The app has been loaded; notify the authentication scheme about this
    authScheme.value.enter();
});
onUnmounted(() => {
    // The app has been closed or refreshed; notify the authentication scheme about this
    authScheme.value.leave();
});
</script>

<template>
    <RouterView v-if="isAuthenticated" />
    <component v-else :is="authScheme.authComponent" :auth-scheme="authScheme" />
</template>

<style scoped lang="scss">

</style>
