<script setup lang="ts">
import { useComponentStore } from "../../../../data/stores/ComponentStore";

import Header from "./Header.vue";

const compStore = useComponentStore();
</script>

<template>
    <div class="r-centered-grid r-text">
        <Header></Header>
        <div>Unable to connect to server!</div>
        <div class="r-text-gray italic">
            {{ compStore.componentStateMessage }}
        </div>
        <div>Please refresh your browser to try again.</div>
    </div>
</template>

<style scoped lang="scss"></style>
