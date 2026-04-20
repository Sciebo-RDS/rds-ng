<script setup lang="ts">
import { Head } from "@unhead/vue/components";
import { computed, onMounted, onUnmounted, shallowReactive } from "vue";
import { RouterView } from "vue-router";

import { NetworkClientSettingIDs } from "@common/settings/NetworkSettingIDs.ts";

import { FrontendComponent } from "@/component/FrontendComponent";

const comp = FrontendComponent.inject();
const integrationScheme = shallowReactive(comp.integrationScheme);
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
    <Head>
        <meta name="rds-comp-id" :content="comp.data.compID.toString()" />
        <meta name="rds-comp-title" :content="comp.data.title" />
        <meta name="rds-comp-name" :content="comp.data.name" />
        <meta name="rds-comp-version" :content="comp.data.version.format()" />

        <meta name="rds-server-address" :content="comp.data.config.value<string>(NetworkClientSettingIDs.ServerAddress)" />
    </Head>

    <RouterView v-if="isIntegrated" />
    <component v-else :is="integrationScheme.integrationComponent" :scheme="integrationScheme" />
</template>

<style scoped lang="scss"></style>
