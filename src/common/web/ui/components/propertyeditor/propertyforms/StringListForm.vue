<script setup lang="ts">
import { computed, inject } from "vue";
import Chips from "primevue/chips";

import { PropertyController } from "../PropertyController";
import { PropertySet } from "../PropertySet";
import { type ProfileID } from "../PropertyProfile";

const props = defineProps(["property"]);

const controller = inject("controller") as PropertyController<PropertySet | PropertySet[]>;
const categoryId = inject("categoryId") as string;
const profileId = inject("profileId") as ProfileID;

const value = computed(() => controller.getValue(profileId, categoryId, props.property.id));

let debounce: number | null = null;

const handleInput = (eValue: any) => {
    debounce = controller.setValue(profileId, debounce, categoryId, props.property.id, eValue);
};
</script>

<template>
    <Chips @update:modelValue="handleInput" :modelValue="value" separator="," class="inline" :addOnBlur="true" placeholder="Separate by comma" />
</template>
