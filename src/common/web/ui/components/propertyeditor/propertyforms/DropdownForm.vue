<script setup lang="ts">
import { ref, inject } from "vue";
import Dropdown from "primevue/dropdown";

import { PropertyController } from "../PropertyController";
import { PropertySet } from "../PropertySet";
import { type ProfileID } from "../PropertyProfile";

const props = defineProps(["property"]);

const controller = inject("controller") as PropertyController<PropertySet | PropertySet[]>;
const categoryId = inject("categoryId") as string;
const profileId = inject("profileId") as ProfileID;

const value = ref(controller.getValue(profileId, categoryId, props.property.id));

let debounce: number | null = null;

const handleInput = (e: any) => {
    debounce = controller.setValue(profileId, debounce, categoryId, props.property.id, e.value);
};
</script>

<template>
    <div class="flex">
        <Dropdown
            v-model="value"
            @change="handleInput"
            :options="property.options"
            class="grow"
            placeholder="Select"
            filter
            :pt="{
                panel: {
                    class: 'w-0',
                },
            }"
        />
    </div>
</template>
