<script setup lang="ts">
import Button from "primevue/button"
import { io } from "socket.io-client"
import { ref } from "vue"

const connected = ref(false);
function clickme(event) {
    console.log("LETS TRY THIS");

    const socket = io("http://localhost:4200", {
        auth: { "component_id": "web/frontend/default" }
    });

    socket.on("connect", () => {
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
