<script setup lang="ts">
import { ref, inject } from "vue";
import Calendar from "primevue/calendar";

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
        <Calendar
            @date-select="(date: Date) => controller.setValue(profileId, categoryId, props.property.id, date)"
            dateFormat="yy"
            v-model="value"
            class="w-full"
            view="year"
        />
    </div>
</template>
