<script setup lang="ts">
import Chips from "primevue/chips";
import { computed, type PropType } from "vue";

import { ProjectObjectStore } from "../ProjectObjectStore";
import { type ProfileID } from "../PropertyProfile";

const props = defineProps({
    propertyObjectId: { type: String, required: true },
    inputId: { type: String, required: true },
    profileId: { type: Object as PropType<ProfileID[]>, required: false },
    projectObjects: { type: ProjectObjectStore, required: true }
});

const value = computed(() => props.projectObjects.get(props.propertyObjectId)?.value as Record<string, any>);
</script>

<template>
    <Chips
        @update:modelValue="(value) => projectObjects.update(profileId || [], inputId, propertyObjectId, value)"
        v-model="value[inputId]"
        separator=","
        class="inline"
        :addOnBlur="true"
        placeholder="Separate by comma"
    />
</template>
