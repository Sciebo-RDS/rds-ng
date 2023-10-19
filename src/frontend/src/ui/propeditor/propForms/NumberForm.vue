<script setup lang="ts">
import { ref } from "vue";
import InputNumber from "primevue/inputnumber";

const props = defineProps(["property"]);

const value = ref();
</script>

<template>
  <div>
    <div>
      {{ props.property.name }}
    </div>
    <div class="italic">
      {{ props.property.description }}
    </div>
    <InputNumber showButtons v-model="value" />
  </div>
</template>
