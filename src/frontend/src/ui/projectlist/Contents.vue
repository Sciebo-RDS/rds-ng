<script setup lang="ts">
import { frontendStore } from "@/data/stores/FrontendStore";

const feStore = frontendStore();
</script>

<template>
    <div>
        <ul class="p-1.5">
            <li v-for="proj in feStore.projects" class="pb-5">
                - {{ proj.name }}: {{ proj.description }}
            </li>
        </ul>
    </div>
</template>

<style scoped lang="scss">

</style>
