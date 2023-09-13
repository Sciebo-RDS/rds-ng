<script setup lang="ts">
import Header from "./Header.vue";
</script>

<template>
    <div class="r-centered-grid r-text">
        <Header></Header>
        <div>
            <span class="italic">Hang on tight while I'm initializing...</span>
        </div>
        <div>
            <span class="material-icons-outlined animate-spin" style="font-size: 32px;">hourglass_empty</span>
        </div>
    </div>
</template>

<style scoped lang="scss">
</style>
