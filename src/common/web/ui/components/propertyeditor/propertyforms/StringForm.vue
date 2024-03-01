<script setup lang="ts">
import { inject, computed } from "vue";
import InputText from "primevue/inputtext";

import { PropertyController } from "../PropertyController";
import { PropertySet } from "../PropertySet";
import { type ProfileID } from "../PropertyProfile";
import type { NestedView } from "@common/ui/views/NestedView";

const props = defineProps(["property"]);

const controller = inject("controller") as PropertyController<PropertySet | PropertySet[]>;
const categoryId = inject("categoryId") as string;
const profileId = inject("profileId") as ProfileID;

const value = computed(() => controller.getValue(profileId, categoryId, props.property.id));

const handleInput = (e: any) => {
    controller.setValue(profileId, categoryId, props.property.id, e.target.value);
};
</script>

<template>
    <div>
        <InputText type="text" @input="handleInput" :modelValue="value" class="w-full" />
    </div>
</template>
