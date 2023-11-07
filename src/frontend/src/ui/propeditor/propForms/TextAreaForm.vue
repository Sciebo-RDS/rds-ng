<script setup lang="ts">
import { ref, inject } from "vue";
import Textarea from "primevue/textarea";

const props = defineProps(["property"]);

const controller = inject("controller");
const categoryId = inject("categoryId");

let value = ref(controller.getValue(categoryId, props.property.id));

let debounce: number | null = null;

let handleInput = (e: Event) => {
    debounce = controller.setValue(
        debounce,
        categoryId,
        props.property.id,
        e.target.value
    );
};
</script>

<template>
    <Textarea @input="handleInput" v-model="value" autoResize class="w-full" />
</template>
