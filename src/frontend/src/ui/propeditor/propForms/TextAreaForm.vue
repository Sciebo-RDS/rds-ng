<script setup lang="ts">
import { ref, inject } from "vue";
import Textarea from "primevue/textarea";

const props = defineProps(["property"]);

const controller = inject("controller");
const categoryId = inject("categoryId");

let value = ref(controller.getValue(categoryId, props.property.id));

let debounce: number | null = null;

function handleInput(e: Event) {
    if (debounce) {
        clearTimeout(debounce);
    }
    debounce = setTimeout(() => {
        controller.setValue(categoryId, props.property.id, e.target.value);
    }, 500);
}
</script>

<template>
    <Textarea @input="handleInput" v-model="value" autoResize class="w-full" />
</template>
