<script setup lang="ts">
import { ref } from "vue";
import InputText from "primevue/inputtext";

const props = defineProps(["property"]);

const value = ref("");
</script>

<template>
  <div class="grid grid-rows-2 grid-cols-4 gap-x-10">
    <div class="row-start-1 row-span-1">
      {{ props.property.name }}
      <div class="text-sm text-slate-600">
        {{ props.property.description }}
      </div>
    </div>

    <div class="row-span-2 col-span-3">
      <InputText type="text" v-model="value" class="w-full" />
    </div>
  </div>
</template>
