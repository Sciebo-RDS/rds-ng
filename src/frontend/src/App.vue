<script setup lang="ts">
import { PingCommand } from "@common/api/NetworkCommands";
import { WebComponent } from "@common/component/WebComponent";
import { Channel } from "@common/core/messaging/Channel";
import { ConnectionState, networkStore } from "@common/stores/NetworkStore";
import Button from "primevue/button"
import { onMounted, watch } from "vue"

const comp = WebComponent.inject();
const svc = comp.createService("Frontend service");
const nwStore = networkStore();

watch(() => nwStore.connectionState, (state, prevState) => {
    console.log("Connection state -> IS: " + String(state) + "; WAS: " + String(prevState));
});

onMounted(() => {
    comp.run();
});

function clickButton(event: any): void {
    svc.messageBuilder.buildCommand(PingCommand).emit(Channel.direct("infra/gate/default"));
}
</script>

<template>
    <div style="padding: 25px;">
        <header>
            <img alt="Vue logo" class="logo" src="@assets/img/rds-octopus-bl.svg" width="250" height="250"/><br>
        </header>
        <Button label="Send Ping" class="bg-red-500 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded" @click="clickButton" :disabled="nwStore.connectionState == ConnectionState.Disconnected" unstyled/>
        <div>Connected={{ nwStore.connectionState }}</div>
        <h1 class="text-3xl font-bold underline bg-amber-200">
            Hello world!
        </h1>
    </div>
</template>
