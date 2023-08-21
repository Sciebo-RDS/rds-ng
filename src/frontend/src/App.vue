<script setup lang="ts">
import { Component } from "@common/component/Component";
import { Command } from "@common/core/messaging/Command";
import { CommandReply } from "@common/core/messaging/CommandReply";
import { Message } from "@common/core/messaging/Message"
import { networkStore } from "@common/stores/NetworkStore";
import Button from "primevue/button"
import { onMounted, watch } from "vue"

const comp = Component.instance;

onMounted(() => {
    comp.run();
});

const nwStore = networkStore();

watch(() => nwStore.connected, (connected, prevConnected) => {
    console.log("Connected? IS: " + String(connected) + "; WAS: " + String(prevConnected));
});

@Message.define("msg/command")
class MyCommand extends Command {
    public some_cool_text: string = "";
    public a_number: int = 0;
}

@Message.define("msg/command/reply")
class MyCommandReply extends CommandReply {
}

function clickme(event: any): void {
    console.log("LETS TRY THIS");

    /*
    const socket = io("http://localhost:4200", {
        auth: { "component_id": "web/frontend/default" }
    });

    socket.on("connect", () => {
        let c = comp as Component;
        let s = c.createService("TEST=!=", MyContext);

        s.messageHandler("msg/command", MyCommand,
            (msg: MyCommand, ctx: MyContext): void => {
                console.log("GOT COMMAND AYE");
                console.log(msg);
                console.log(ctx);
                //ctx.messageEmitter.emitReply(MyCommandReply, msg, {}, false, "Nah no good");
            }
        );

                s.messageHandler("msg/command/reply", MyCommandReply, (msg: MyCommandReply, ctx: MyContext) => {
                        console.log("GOT REPLY!!!");
                        console.log(msg);
                        console.log(ctx);
                    }
                );

        function h(cmd: Command, success: boolean, msg: string): void {
            console.log("DONE CALLBACK");
            console.log(success);
            console.log(cmd);
            console.log(msg);
        }

        function h2(failType: CommandFailType, msg: string): void {
            console.log("FAIL CALLBACK");
            console.log(msg);
        }

        s.messageEmitter.emitCommand(MyCommand, Channel.local(), {}, h, h2, 3);
        connected.value = true;
*/
}

</script>

<template>
    <header>
        <img alt="Vue logo" class="logo" src="@assets/img/rds-octopus-bl.svg" width="250" height="250"/>
    </header>
    <Button label="Connect" class="bg-red-500 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded" @click="clickme" unstyled/>
    <div>Connected={{ nwStore.connected }}</div>
    <h1 class="text-3xl font-bold underline bg-amber-200">
        Hello world!
    </h1>
</template>
