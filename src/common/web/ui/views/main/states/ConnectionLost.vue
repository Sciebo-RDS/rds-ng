<script setup lang="ts">
import Header from "./Header.vue";
</script>

<template>
    <Header></Header>
    <div class="grid grid-flow-row auto-rows-max justify-items-center text-slate-700">
        <div>
            It seems that I lost my connection to the server...
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
