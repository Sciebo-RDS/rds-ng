<script setup lang="ts">
import { ref, inject } from "vue";
import InputText from "primevue/inputtext";

import { PropertyController } from "@common/ui/components/propertyeditor/PropertyController";
import { PropertySet } from "@common/ui/types/PropertySet";

const props = defineProps(["property"]);

const controller: PropertyController<PropertySet | PropertySet[]> = inject("controller");
const categoryId = inject("categoryId");
const profileId = inject("profileId");

const value = ref(controller.getValue(profileId, categoryId, props.property.id));

let debounce: number | null = null;

const handleInput = (e: Event) => {
    debounce = controller.setValue(profileId, debounce, categoryId, props.property.id, e.target.value);
};
</script>

<template>
    <InputText type="text" @input="handleInput" v-model="value" />
</template>
