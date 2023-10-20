<script setup lang="ts">
import { ref } from "vue";
import MultiSelect from "primevue/multiselect";

const props = defineProps(["property"]);

const value = ref();
</script>

<template>
  <div class="">
    <MultiSelect v-model="value" :options="property.options" class="w-full" />
  </div>
</template>
