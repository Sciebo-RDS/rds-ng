<script setup lang="ts">
import { computed, onMounted, onUnmounted, shallowRef } from "vue";
import { RouterView } from "vue-router";

import { FrontendComponent } from "@/component/FrontendComponent";

const comp = FrontendComponent.inject();
const authScheme = shallowRef(comp.authenticationScheme);
const isAuthenticated = computed(() => authScheme.value.isAuthenticated);

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
