<script setup lang="ts">
import { ref } from "vue";
import Textarea from "primevue/textarea";

const props = defineProps(["property", "category_name", "controller"]);

let value = ref(
    props.controller.getValue(props.category_name, props.property.name)
);

let debounce: number | null = null;

function handleInput(e: any) {
    if (debounce) {
        clearTimeout(debounce);
    }
    console.log(typeof e);
    debounce = setTimeout(() => {
        props.controller.setValue(
            props.category_name,
            props.property.name,
            e.target.value
        );
        console.log(props.controller.propertiesToString());
    }, 500);
}
</script>

<template>
  <Textarea @input="handleInput" v-model="value" autoResize class="w-full" />
</template>
