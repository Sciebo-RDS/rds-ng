<script setup lang="ts">
import { computed, inject } from "vue";
import Textarea from "primevue/textarea";

import { PropertyController } from "../PropertyController";
import { PropertySet } from "../PropertySet";
import { type ProfileID } from "../PropertyProfile";

const props = defineProps(["property"]);

const controller = inject("controller") as PropertyController<PropertySet | PropertySet[]>;
const categoryId = inject("categoryId") as string;
const profileId = inject("profileId") as ProfileID;

const value = computed(() => controller.getValue(profileId, categoryId, props.property.id));

let debounce: number | null = null;

const handleInput = (e: any) => {
    debounce = controller.setValue(profileId, debounce, categoryId, props.property.id, e.target.value);
};
</script>

<template>
    <div>
        <Textarea @input="handleInput" :modelValue="value" autoResize class="w-full" />
    </div>
</template>
