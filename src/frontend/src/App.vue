<script setup lang="ts">
import { ClientConnectedEvent } from "@common/api/NetworkEvents";
import { WebComponent } from "@common/component/WebComponent";
import { Channel } from "@common/core/messaging/Channel";
import { Event } from "@common/core/messaging/Event";
import type { MessageContext } from "@common/core/messaging/handlers/MessageContext";
import { Message } from "@common/core/messaging/Message"
import { networkStore } from "@common/stores/NetworkStore";
import Button from "primevue/button"
import { onMounted, watch } from "vue"

@Message.define("msg/event")
class MyEvent extends Event {
    public some_cool_text: string = "";
    public a_number: number = 0;
}

const comp = WebComponent.instance;

onMounted(() => {
    comp.run();
});

const nwStore = networkStore();

watch(() => nwStore.connected, (connected, prevConnected) => {
    console.log("Connected? IS: " + String(connected) + "; WAS: " + String(prevConnected));
});

const svc = comp.createService("Mega test-service");

function clickme(event: any): void {
    console.log("LETS TRY THIS");
    svc.messageEmitter.emitEvent(MyEvent, Channel.direct("infra/gate/default"), { some_cool_text: "Hi Gate!", a_number: 4711 });
}

svc.messageHandler("msg/event", MyEvent, (msg: MyEvent, ctx: MessageContext) => {
    console.log("GOT EVENT! " + String(msg));
});

svc.messageHandler(ClientConnectedEvent.Name, ClientConnectedEvent, (msg: ClientConnectedEvent, ctx: MessageContext) => {
    console.log(ClientConnectedEvent.Name);
});

</script>

<template>
    <div style="padding: 25px;">
        <header>
            <img alt="Vue logo" class="logo" src="@assets/img/rds-octopus-bl.svg" width="250" height="250"/><br>
        </header>
        <Button label="Send message" class="bg-red-500 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded" @click="clickme" :disabled="!nwStore.connected" unstyled/>
        <div>Connected={{ nwStore.connected }}</div>
        <h1 class="text-3xl font-bold underline bg-amber-200">
            Hello world!
        </h1>
    </div>
</template>
