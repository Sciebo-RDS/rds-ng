<script setup lang="ts">
import { componentStore } from "../../../../stores/ComponentStore";

import Header from "./Header.vue";

const compStore = componentStore();
</script>

<template>
    <div class="r-centered-grid r-text">
        <Header></Header>
        <div>
            Oh no, I was unable to connect to the server!
        </div>
        <div class="text-slate-500 italic">
            {{ compStore.componentStateMessage }}
        </div>
        <div>
            Pretty-please refresh your browser to try again.
        </div>
    </div>
</template>

<style scoped lang="scss">
</style>
