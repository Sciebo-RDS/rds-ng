<script setup lang="ts">
import { computed, watch, type PropType, type Ref } from "vue";
import { boolean } from "yup";

import { LayoutPropertyObject, PropertyObject, PropertyObjectStore } from "./PropertyObjectStore";
import { ProfileClass, ProfileLayoutClass, type ProfileID } from "./PropertyProfile";
import { PropertyProfileStore } from "./PropertyProfileStore";

import EntityColumn from "./EntityColumn/EntityColumn.vue";
import IndexColumn from "./IndexColumn.vue";

const { index, propertyClass, propertyObjects, projectProfiles, sharedPropertyObjectStore, layoutProfiles, showProfileTags } = defineProps({
    index: {
        type: Number,
        required: true
    },
    propertyClass: {
        type: Object as PropType<ProfileClass & { profiles: ProfileID[] }>,
        required: true
    },
    propertyObjects: {
        type: Object as PropType<PropertyObjectStore>,
        required: true
    },
    projectProfiles: {
        type: PropertyProfileStore,
        required: true
    },
    sharedPropertyObjectStore: {
        type: Object as PropType<PropertyObjectStore>,
        required: true
    },
    layoutProfiles: {
        type: Object as PropType<Array<ProfileLayoutClass>>,
        required: true
    },
    showProfileTags: {
        type: boolean,
        default: true
    }
});
propertyObjects.add(new LayoutPropertyObject(propertyClass.getId()));

watch(
    () => propertyObjects.get(propertyClass.getId()),
    (obj) => {
        if (!obj) propertyObjects.add(new LayoutPropertyObject(propertyClass.getId()));
    }
);

const propertyObject = computed(
    () => propertyObjects.get(propertyClass.getId()) || propertyObjects.add(new LayoutPropertyObject(propertyClass.getId()))
) as Ref<PropertyObject>;

const profiles = computed(() => {
    const profileIDs = layoutProfiles?.find((e) => e.id == propertyObject.value.getId())!.getProfiles() as ProfileID[];
    const filteredProfileIDs: ProfileID[] = [];

    profileIDs.forEach((id) => {
        if (!filteredProfileIDs.find((e) => e[0] == id[0])) {
            filteredProfileIDs.push(id);
        }
    });
    return filteredProfileIDs;
});

const removeFromLayout = (pId: string) => {
    propertyObjects.remove(pId);
};
</script>

<template>
    <div class="flex flex-row px-2 pl-0 rounded group max-w-full w-full">
        <!-- IndexColumn holds the index number and the remove button for the property, if it is not required. -->
        <IndexColumn class="grid w-16 justify-center shrink-0" @remove="(pId) => removeFromLayout(pId)" :propertyClass="propertyClass" :index="index + 1" />

        <!-- EntityColumn holds the main content of the property, including the property name, description, and linked items. -->
        <EntityColumn
            :propertyClass="propertyClass"
            :profiles="profiles"
            :projectProfiles="projectProfiles"
            :sharedPropertyObjectStore="sharedPropertyObjectStore"
            :propertyObjects="propertyObjects"
            :propertyObject="propertyObject"
            :isDialog="false"
            :show-profile-tag="showProfileTags"
        />
    </div>
</template>
