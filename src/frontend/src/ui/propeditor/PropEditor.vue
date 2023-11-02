<script setup lang="ts">
import { provide } from "vue";
import PropCategory from "./PropCategory.vue";

const props = defineProps(["controller"]);

provide("controller", props.controller);
</script>

<template>
    <div class="">
        <PropCategory
            v-for="category in props.controller.profile.categories"
            :category="category"
            class="my-5 mx-10"
        />
    </div>
</template>
