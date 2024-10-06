<script setup lang="ts">
import Calendar from "primevue/calendar";
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
        <Calendar
            @date-select="(date: Date) => projectObjects.update(profileId || [], inputId, propertyObjectId, date)"
            dateFormat="dd/mm/yy"
            v-model="value[inputId]"
            class="w-full"
        />
    </div>
</template>
