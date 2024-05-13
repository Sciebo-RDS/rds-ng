<script setup lang="ts">
import { inject, computed, ref, watch } from "vue";
import InputText from "primevue/inputtext";

import { PropertyController } from "../PropertyController";
import { PropertySet } from "../PropertySet";

import type { NestedView } from "@common/ui/views/NestedView";
import type { ProjectObjectStore } from "../ProjectObjectStore";

const props = defineProps(["propertyObjectId", "inputId", "profileId", "projectObjects"]);

//const value = computed(() => props.projectObjects.get(props.propertyObjectId).value);
const value = ref("");
let mV = "";

watch(
    () => props.propertyObjectId,
    (newValue) => {
        mV = "";
        value.value = "";
    }
);
</script>

<template>
    <div>
        <InputText
            type="text"
            :modelValue="mV"
            :v-model="value"
            class="w-full"
            @input="(e) => projectObjects.update(profileId, inputId, 'string', propertyObjectId, e.target.value)"
        />
    </div>
</template>
