<script setup lang="ts">
import Textarea from "primevue/textarea";
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
    <div>
        <Textarea
            @update:modelValue="(value) => projectObjects.update(profileId || [], inputId, propertyObjectId, value)"
            v-model="value[inputId]"
            autoResize
            class="w-full"
        />
    </div>
</template>
