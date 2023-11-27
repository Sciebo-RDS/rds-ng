<script setup lang="ts">
import Header from "./Header.vue";
</script>

<template>
    <div class="r-centered-grid r-text">
        <Header></Header>
        <div>
            <span class="italic">Hang on tight while I'm connecting to the server...</span>
        </div>
        <div>
            <span class="material-icons-outlined mi-hourglass-empty animate-spin" style="font-size: 32px;"/>
        </div>
    </div>
</template>

<style scoped lang="scss">
</style>
