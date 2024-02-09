<script setup lang="ts">
import { ref, inject } from "vue";
import InputNumber from "primevue/inputnumber";

import { PropertyController } from "@common/ui/components/propertyeditor/PropertyController";

const props = defineProps(["property"]);

const controller: PropertyController = inject("controller");
const categoryId = inject("categoryId");
const profileId = inject("profileId");

// TODO: Handle overflows
const value = ref(controller.getValue(profileId, categoryId, props.property.id));

let debounce: number | null = null;

const handleInput = (e: Event) => {
    debounce = controller.setValue(profileId, debounce, categoryId, props.property.id, e.value);
};
</script>

<template>
    <div class="">
        <InputNumber @input="handleInput" v-model="value" :useGrouping="false" class="w-full" />
    </div>
</template>
