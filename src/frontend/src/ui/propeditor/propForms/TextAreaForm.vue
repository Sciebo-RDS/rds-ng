<script setup lang="ts">
import { ref } from "vue";
import Textarea from "primevue/textarea";

const props = defineProps(["property"]);

const value = ref("");
</script>

<template>
  <Textarea v-model="value" autoResize class="w-full" />
</template>
