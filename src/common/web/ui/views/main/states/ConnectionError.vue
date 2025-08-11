<script setup lang="ts">
import { WebComponent } from "../../../../component/WebComponent";
import { useComponentStore } from "../../../../data/stores/ComponentStore";
import { HostCommuncationAction, sendActionToHost } from "../../../../integration/HostCommunication";

import LinkedText from "../../../components/misc/LinkedText.vue";
import Header from "./Header.vue";

const comp = WebComponent.injectComponent();

const compStore = useComponentStore();

function reloadApp() {
    sendActionToHost(HostCommuncationAction.Reload);
}
</script>

<template>
    <div class="r-centered-grid r-text">
        <Header></Header>
        <div>Unable to connect to the {{ comp.data.title }} server!</div>
        <div class="r-text-error italic">
            {{ compStore.componentStateMessage }}
        </div>
        <div>&nbsp;</div>
        <div>
            Please <a href="#" @click.prevent="reloadApp" class="r-text-link">refresh</a> your browser to try again. If this error persists,
            <LinkedText link="mailto:sciebo.rds@uni-muenster.de" text="send us an email" />
            describing the error.
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
