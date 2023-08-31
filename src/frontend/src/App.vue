<script setup lang="ts">
import createNetworkService from "@/services/NetworkService";

import { networkStore } from "@/stores/NetworkStore";
import { PingCommand } from "@common/api/NetworkCommands";
import { WebComponent } from "@common/component/WebComponent";
import { Channel } from "@common/core/messaging/Channel";
import Button from "primevue/button"
import { onMounted, watch } from "vue"

const comp = WebComponent.inject();
const svc = createNetworkService(comp);
const nwStore = networkStore();

onMounted(() => {
    comp.run();
});

watch(() => nwStore.connected, (connected, prevConnected) => {
    console.log("Connected? IS: " + String(connected) + "; WAS: " + String(prevConnected));
});

function clickButton(event: any): void {
    svc.messageEmitter.emitCommand(PingCommand, Channel.direct("infra/gate/default"));
}
</script>

<template>
    <div style="padding: 25px;">
        <header>
            <img alt="Vue logo" class="logo" src="@assets/img/rds-octopus-bl.svg" width="250" height="250"/><br>
        </header>
        <Button label="Send Ping" class="bg-red-500 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded" @click="clickButton" :disabled="!nwStore.connected" unstyled/>
        <div>Connected={{ nwStore.connected }}</div>
        <h1 class="text-3xl font-bold underline bg-amber-200">
            Hello world!
        </h1>
    </div>
</template>
