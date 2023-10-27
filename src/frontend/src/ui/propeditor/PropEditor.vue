<script setup lang="ts">
import { ref } from "vue";
import PropCategory from "./PropCategory.vue";

const props = defineProps(["controller"]);
</script>

<template>
    <div class="">
        <PropCategory
            v-for="category in props.controller.profile.categories"
            :category="category"
            :controller="props.controller"
            class="my-5 mx-10"
        />
    </div>
</template>
