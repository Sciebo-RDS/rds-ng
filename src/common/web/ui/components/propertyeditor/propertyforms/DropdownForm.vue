<script setup lang="ts">
import { ref, inject } from "vue";
import Dropdown from "primevue/dropdown";

import { PropertyController } from "@common/ui/components/propertyeditor/PropertyController";
import { PropertySet } from "@common/ui/types/PropertySet";

const props = defineProps(["property"]);

const controller: PropertyController<PropertySet | PropertySet[]> = inject("controller");
const categoryId = inject("categoryId");
const profileId = inject("profileId");

const value = controller.getValue(profileId, categoryId, props.property.id);

let debounce: number | null = null;

const handleInput = (e: string) => {
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
