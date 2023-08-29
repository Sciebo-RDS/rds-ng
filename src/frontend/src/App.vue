<script setup lang="ts">
import initNetworkService from "@/services/NetworkService";

import { networkStore } from "@/stores/NetworkStore";
import { WebComponent } from "@common/component/WebComponent";
import Button from "primevue/button"
import { onMounted, watch } from "vue"

const comp = WebComponent.instance;

onMounted(() => {
    comp.run();
    initNetworkService(comp);
});

const nwStore = networkStore();

watch(() => nwStore.connected, (connected, prevConnected) => {
    console.log("Connected? IS: " + String(connected) + "; WAS: " + String(prevConnected));
});

function clickButton(event: any): void {
    console.log("CLICKED BUTTON");
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
