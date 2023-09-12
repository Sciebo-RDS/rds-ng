<script setup lang="ts">
import Header from "./Header.vue";
</script>

<template>
    <Header></Header>
    <div class="grid grid-flow-row auto-rows-max justify-items-center text-slate-700">
        <div>
            <span class="italic">Hang on tight while I'm initializing...</span>
        </div>
        <div class="text-slate-500">
            <span class="material-icons-outlined animate-spin" style="font-size: 32px;">hourglass_empty</span>
        </div>
    </div>
</template>

<style scoped lang="scss">
div {
    margin: 0.1rem;
}
</style>
