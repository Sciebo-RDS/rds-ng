<script setup lang="ts">
import { useRoute } from "vue-router";

import Header from "./Header.vue";

const route = useRoute();
</script>

<template>
    <Header></Header>
    <div class="grid grid-flow-row auto-rows-max justify-items-center text-slate-700">
        <div>
            It seems that I lost my connection...
        </div>
        <div>
            Click
            <router-link to="/">here</router-link>
            to refresh me.
        </div>
    </div>
</template>

<style scoped lang="scss">
div {
    margin: 0.25rem;
}
</style>
