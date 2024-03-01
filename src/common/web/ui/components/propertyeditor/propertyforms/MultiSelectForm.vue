<script setup lang="ts">
import { ref, inject } from "vue";
import MultiSelect from "primevue/multiselect";

import { PropertyController } from "../PropertyController";
import { PropertySet } from "../PropertySet";
import { type ProfileID } from "../PropertyProfile";

const props = defineProps(["property"]);

const controller = inject("controller") as PropertyController<PropertySet | PropertySet[]>;
const categoryId = inject("categoryId") as string;
const profileId = inject("profileId") as ProfileID;

const value = ref(controller.getValue(profileId, categoryId, props.property.id));
</script>

<template>
    <div>
        <MultiSelect
            @change="(e: any) => controller.setValue(profileId, categoryId, props.property.id, e.value)"
            v-model="value"
            :options="property.options"
            class="w-full relative"
        />
    </div>
</template>
