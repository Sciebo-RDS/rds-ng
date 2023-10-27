<script setup lang="ts">
import { ref, watch } from "vue";
import InputText from "primevue/inputtext";

const props = defineProps(["property", "category_name", "controller"]);

const value = ref("");
watch(value, () => {
    //TODO debounce, implement for other Type Forms as well.
    props.controller.setValue(props.category_name, props.property.name, value);
    console.log(props.controller.propertySet);
});
</script>

<template>
    <InputText type="text" v-model="value" />
</template>
