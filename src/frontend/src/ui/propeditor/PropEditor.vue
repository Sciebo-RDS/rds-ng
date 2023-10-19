<script setup lang="ts">
import { ref } from "vue";
import { testProfile } from "@/ui/propeditor/PropertySet";
import PropCategory from "./PropCategory.vue";
</script>

<template>
  <div class="">
    <!-- Profile: {{ testProfile.name }} -->

    <PropCategory
      v-for="category in testProfile.categories"
      :category="category"
      class="my-5 mx-10"
    />
  </div>
</template>
