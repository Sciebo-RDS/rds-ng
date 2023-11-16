<script setup lang="ts">
import { ref, inject } from "vue";
import InputText from "primevue/inputtext";

const props = defineProps(["property"]);

const controller = inject("controller");
const categoryId = inject("categoryId");
const profileId = inject("profileId");

let value = ref(controller.getValue(profileId, categoryId, props.property.id));

let debounce: number | null = null;

let handleInput = (e: Event) => {
    debounce = controller.setValue(
        profileId,
        debounce,
        categoryId,
        props.property.id,
        e.target.value
    );
};
</script>

<template>
    <InputText type="text" @input="handleInput" v-model="value" />
</template>
