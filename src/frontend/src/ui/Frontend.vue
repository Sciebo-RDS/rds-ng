<script setup lang="ts">
import { computed, onMounted, onUnmounted } from "vue";
import { RouterView } from "vue-router";

import { FrontendComponent } from "@/component/FrontendComponent";

const comp = FrontendComponent.inject();
const integrationScheme = comp.integrationScheme;
const isIntegrated = computed(() => integrationScheme.isIntegrated);

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
