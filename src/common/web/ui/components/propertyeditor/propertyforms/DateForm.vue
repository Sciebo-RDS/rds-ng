<script setup lang="ts">
import { ref, inject } from "vue";
import Calendar from "primevue/calendar";

import { PropertyController } from "@common/ui/components/propertyeditor/PropertyController";
import { PropertySet } from "@common/ui/types/PropertySet";

const props = defineProps(["property"]);

const controller: PropertyController<PropertySet | PropertySet[]> = inject("controller");
const categoryId = inject("categoryId");
const profileId = inject("profileId");

const value = ref(controller.getValue(profileId, categoryId, props.property.id));

let debounce: number | null = null;

const handleInput = (eValue: string) => {
    const ms: number = new Date(eValue).getTime();
    debounce = controller.setValue(profileId, debounce, categoryId, props.property.id, ms);
};
</script>

<template>
    <div class="">
        <Calendar @update:modelValue="handleInput" dateFormat="yy/mm/dd" v-model="value" class="w-full" view="year" />
    </div>
</template>
