<script setup lang="ts">
import { reactive } from "vue";

import { Project } from "@common/data/entities/project/Project";
import { MetadataController } from "@common/ui/components/propertyeditor/PropertyController";
import { testProfile, testValues } from "@common/ui/components/propertyeditor/DummyData";
import { dataCite } from "@common/ui/components/propertyeditor/profiles/datacite";
import { osf } from "@common/ui/components/propertyeditor/profiles/osf";
import { PropertySet, type PersistedPropertySet } from "@common/ui/components/propertyeditor/PropertySet";
import PropertyEditor from "@common/ui/components/propertyeditor/PropertyEditor.vue";
import logging from "@common/core/logging/Logging";
const props = defineProps({
    project: {
        type: Project,
        required: true,
    },
});

/* Testdata */
const baseSet = new PropertySet(dataCite);
console.log(baseSet);
const mergeSet = [new PropertySet(osf)];
console.log(mergeSet);

const profiles: PropertySet[] = [];

try {
    profiles.push(new PropertySet(testProfile, testValues));
} catch (e: any) {
    logging.error(e, "propertyeditor");
}
/* Testdata */

const controller = reactive(new MetadataController(profiles, baseSet, mergeSet));

const handleMetadataUpdate: Function = (data: PersistedPropertySet) => {
    logging.debug(`Received update from PropertyEditor: ${JSON.stringify(data)}`, "ProjectDetails");
};
</script>

<template>
    <div><PropertyEditor @update="(data: PersistedPropertySet) => handleMetadataUpdate(data)" :controller="controller" :logging="logging" twoCol /></div>
</template>

<style scoped lang="scss"></style>
