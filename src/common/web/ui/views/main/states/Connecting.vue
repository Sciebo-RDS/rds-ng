<script setup lang="ts">
import Header from "./Header.vue";
</script>

<template>
    <div class="r-centered-grid r-text">
        <Header></Header>
        <div>
            <span class="italic">Connecting to server, please wait...</span>
        </div>
        <div>
            <span class="material-icons-outlined mi-hourglass-empty animate-spin" style="font-size: 32px" />
        </div>
    </div>
</template>

<style scoped lang="scss"></style>
