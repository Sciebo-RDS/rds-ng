<script setup lang="ts">
import PropertyCategory from "./PropertyCategory.vue";

const props = defineProps(["controller", "project"]);

let defaultCategories = props.controller.getDefaultCategories();
let defaultProfile = props.controller.getDefaultProfile();
</script>

<template>
    <PropertyCategory
        v-for="[i, category] of defaultCategories.entries()"
        :project="project"
        :category="category"
        :profileId="defaultProfile"
        :index="i"
        class="mt-5"
        defaultSet
    />
</template>
