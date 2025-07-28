<script setup lang="ts">
import { useIntervalFn } from "@vueuse/core";

import { HostCommuncationAction, sendActionToHost } from "../../../../integration/HostCommunication";

import Header from "./Header.vue";

const { pause } = useIntervalFn(() => {
    if (document.visibilityState == "visible") {
        pause();
        reloadApp();
    }
}, 1000);

function reloadApp() {
    sendActionToHost(HostCommuncationAction.Reload);
}
</script>

<template>
    <div class="r-centered-grid r-text">
        <Header></Header>
        <div>The connection to the server has been lost.</div>
        <div>If you are not being logged in automatically, click <a href="#" @click.prevent="reloadApp" class="r-text-link">here</a>.</div>
    </div>
</template>

<style scoped lang="scss"></style>
