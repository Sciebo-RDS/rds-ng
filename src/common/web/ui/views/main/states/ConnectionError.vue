<script setup lang="ts">
import { componentStore } from "../../../../stores/ComponentStore";

import Header from "./Header.vue";

const compStore = componentStore();
</script>

<template>
    <Header></Header>
    <div class="grid grid-flow-row auto-rows-max justify-items-center text-slate-700">
        <div>
            Oh no, I was unable to connect to the server!
        </div>
        <div class="text-slate-500 italic">
            {{ compStore.componentStateMessage }}
        </div>
        <div>
            Pretty-Please refresh your browser to try again.
        </div>
    </div>
</template>

<style scoped lang="scss">
div {
    margin: 0.1rem;
}
</style>
