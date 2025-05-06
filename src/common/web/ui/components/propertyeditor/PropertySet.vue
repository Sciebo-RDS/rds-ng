<script setup lang="ts">
import { computed, ref } from "vue";

import Button from "primevue/button";

import { PropertyObjectStore } from "./PropertyObjectStore";
import { type ProfileID, ProfileLayoutClass } from "./PropertyProfile";
import { calculateLayout as makeLayout } from "./utils/PropertyEditorUtils";

import AddPropertiesDialog from "./AddPropertiesDialog.vue";
import PropertyEditorSearchBar from "./PropertyEditorSearchBar.vue";
import PropertyRow from "./PropertyRow.vue";

const props = defineProps(["project", "projectProfiles", "propertyObjects", "sharedPropertyObjectStore"]);

var layout = makeLayout(props.projectProfiles);

const profileFilter = ref<ProfileID[]>([]);
const requiredOnly = ref(false);
const searchString = ref("");

// TODO Comment and maybe refactor to have dynamic filters
const propsToShow = computed(() =>
    layout
        .filter((e: ProfileLayoutClass) => e.required || (requiredOnly.value ? false : props.propertyObjects.get(e.id) !== undefined))
        .filter(
            (e: ProfileLayoutClass) =>
                profileFilter.value.length === 0 || e.profiles.some((p: ProfileID) => profileFilter.value.map((i) => i[0]).includes(p[0]))
        )
        .filter(
            (e: ProfileLayoutClass) =>
                // search in label
                e.getDisplayLabel().toLowerCase().includes(searchString.value.toLowerCase()) ||
                // search in description
                e.description?.toLowerCase().includes(searchString.value.toLowerCase()) ||
                // search in simple property objects
                !Object.values(props.propertyObjects.get(e.id).getValues()).findIndex((v: string) =>
                    v.toLowerCase().includes(searchString.value.toLowerCase())
                ) ||
                // search in referenced property objects
                      // implement search function on objects? this seems buggy
                      props.propertyObjects
                    .getReferencedObjects(e.id)
                    .map((o: String) => props.sharedPropertyObjectStore.get(o).getValues())
                          .map((e: {}) => Object.values(e))
                    .flat()
                          .findIndex((v: string) => v.toLowerCase().includes(searchString.value.toLowerCase())) >= 0
        )
        .sort((a: ProfileLayoutClass, b: ProfileLayoutClass) => -a.profiles!.length - -b.profiles!.length)
);

const showAddProperties = ref(false);
const hiddenProperties = computed(() =>
    layout.filter((e: ProfileLayoutClass) => !propsToShow.value.map((e: ProfileLayoutClass) => e.getId()).includes(e.getId()))
);
</script>

<template>
    <div class="w-full max-w-full">
        <PropertyEditorSearchBar
            v-model:all-count="layout.filter((e: ProfileLayoutClass) => e.isRequired() || props.propertyObjects.get(e.id) !== undefined).length"
            v-model:search-string="searchString"
            v-model:profile-filter="profileFilter"
            v-model:required-only="requiredOnly"
            v-model:matches-count="propsToShow.length"
            :projectProfiles="projectProfiles"
            :propertyObjects="propertyObjects"
        />
        <PropertyRow
            v-for="(p, i) in propsToShow"
            :key="p.getId()"
            :index="i"
            class="my-5 w-full max-w-full"
            :propertyClass="p"
            :propertyObjects="propertyObjects"
            :sharedPropertyObjectStore="sharedPropertyObjectStore as PropertyObjectStore"
            :projectProfiles="projectProfiles"
            :layoutProfiles="layout"
        />

    <Button
            v-if="hiddenProperties.length !== 0"
        class="fixed bottom-10 right-10"
        icon="material-icons-outlined mi-add"
        size="large"
        rounded
        severity="primary"
        @click="showAddProperties = true"
        v-tooltip="{ value: 'Add more properties' }"
    />

        <AddPropertiesDialog
        v-model:visible="showAddProperties"
            @add-properties="(selectedProperties: ProfileLayoutClass[]) => propsToShow.push(...selectedProperties)"
            :hiddenProperties="hiddenProperties"
        />
            </div>
</template>

<style scoped lang="scss">
:deep(.p-orderlist-controls) {
    display: none;
}

:deep(.p-orderlist-item) {
    @apply border-l-2 border-solid border-transparent;
}

:deep(.p-orderlist-item.p-highlight) {
    @apply bg-emerald-50  border-l-2 border-emerald-600 text-slate-700;
}
</style>
