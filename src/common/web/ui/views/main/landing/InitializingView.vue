<script setup lang="ts">
import { library } from "@fortawesome/fontawesome-svg-core";
import { faSpinner } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import Header from "./Header.vue";

library.add(faSpinner);

</script>

<template>
    <Header></Header>
    <div class="grid grid-flow-row auto-rows-max justify-items-center text-slate-700">
        <div>
            <span class="italic">Hang on tight while I'm initializing...</span>
        </div>
        <div class="text-slate-500">
            <font-awesome-icon icon="fa-solid fa-spinner" spin-pulse size="xl"/>
        </div>
    </div>
</template>

<style scoped lang="scss">
div {
    margin: 0.1rem;
}
</style>
