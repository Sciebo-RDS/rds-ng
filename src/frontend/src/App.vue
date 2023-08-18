<script setup lang="ts">
import type { Component } from "@common/component/Component";
import { Channel } from "@common/core/messaging/Channel";
import { Event } from "@common/core/messaging/Event";
import { Message } from "@common/core/messaging/Message"
import { ServiceContext } from "@common/service/ServiceContext"
import Button from "primevue/button"
import { io } from "socket.io-client"
import { inject, ref } from "vue"

const connected = ref(false);

const comp = inject("comp");

@Message.define("msg/event")
class MyEvent extends Event {
    public some_cool_text: string = "";
    public a_number: int = 0;
}

function clickme(event: any): void {
    console.log("LETS TRY THIS");

    const socket = io("http://localhost:4200", {
        auth: { "component_id": "web/frontend/default" }
    });

    socket.on("connect", () => {
        let c = comp as Component;
        let s = c.createService("TEST=!=");

        s.messageHandler("msg/event", MyEvent,
            (msg: MyEvent, ctx: ServiceContext): void => {
                console.log(msg);
                console.log(ctx);
            }
        );

        s.messageEmitter.emitEvent(MyEvent, Channel.local(), {});

        connected.value = true;
    });
    socket.on("disconnect", () => {
        connected.value = false;
    });
};

</script>

<template>
    <header>
        <img alt="Vue logo" class="logo" src="@assets/img/rds-octopus-bl.svg" width="250" height="250"/>
    </header>
    <Button label="Connect" class="bg-red-500 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded" @click="clickme" unstyled/>
    <div>Connected={{ connected }}</div>
    <h1 class="text-3xl font-bold underline bg-amber-200">
        Hello world!
    </h1>
</template>
