<script setup lang="ts">
import { onMounted, onUnmounted, ref, shallowReactive, watch } from "vue";
import { RouterView } from "vue-router";

import { FrontendComponent } from "@/component/FrontendComponent";

const comp = FrontendComponent.inject();
const integrationScheme = shallowReactive(comp.integrationScheme);
const isIntegrated = ref(integrationScheme.isIntegrated);

// Circumvent Vue warnings arising from using IntegrationScheme.isIntegrated directly
watch(
    () => integrationScheme.isIntegrated,
    (integrated) => {
        isIntegrated.value = integrated;
    },
);

onMounted(() => {
    // The app has been loaded; notify the authentication scheme about this
    integrationScheme.enter();
});
onUnmounted(() => {
    // The app has been closed or refreshed; notify the authentication scheme about this
    integrationScheme.leave();
});
</script>

<template>
    <RouterView v-if="isIntegrated" />
    <component v-else :is="integrationScheme.integrationComponent" :scheme="integrationScheme" />
</template>

<style scoped lang="scss"></style>
