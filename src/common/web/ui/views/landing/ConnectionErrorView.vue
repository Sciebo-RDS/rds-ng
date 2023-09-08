<script setup lang="ts">
import { useRoute } from "vue-router";

import Header from "./Header.vue";

const route = useRoute();
</script>

<template>
    <Header></Header>
    <div class="grid grid-flow-row auto-rows-max justify-items-center text-slate-700">
        <div>
            Oh no, I was unable to connect to the server!
        </div>
        <div class="text-slate-500 italic">
            {{ route.query.error }}
        </div>
    </div>
</template>

<style scoped lang="scss">
div {
    margin: 0.25rem;
}
</style>
