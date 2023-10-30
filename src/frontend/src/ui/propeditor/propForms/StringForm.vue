<script setup lang="ts">
import { ref, watch } from "vue";
import InputText from "primevue/inputtext";

const props = defineProps(["property", "category_name", "controller"]);

let value = ref(
    props.controller.getValue(props.category_name, props.property.name)
);

let debounce: number | null = null;

function handleInput(e: any) {
    if (debounce) {
        clearTimeout(debounce);
    }
    debounce = setTimeout(() => {
        props.controller.setValue(
            props.category_name,
            props.property.name,
            e.target.value
        );
    }, 500);
}
</script>

<template>
    <InputText type="text" @input="handleInput" v-model="value" />
</template>
