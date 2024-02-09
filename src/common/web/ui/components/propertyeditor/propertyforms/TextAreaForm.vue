<script setup lang="ts">
import { ref, inject } from "vue";
import Textarea from "primevue/textarea";

import { PropertyController } from "@common/ui/components/propertyeditor/PropertyController";

const props = defineProps(["property"]);

const controller: PropertyController = inject("controller");
const categoryId = inject("categoryId");
const profileId = inject("profileId");

const value = ref(controller.getValue(profileId, categoryId, props.property.id));

let debounce: number | null = null;

const handleInput = (e: Event) => {
    debounce = controller.setValue(profileId, debounce, categoryId, props.property.id, e.target.value);
};
</script>

<template>
    <Textarea @input="handleInput" v-model="value" autoResize class="w-full" />
</template>
