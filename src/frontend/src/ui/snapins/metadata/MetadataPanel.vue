<script setup lang="ts">
import { reactive } from "vue";

import { Project } from "@common/data/entities/project/Project";
import { MetadataController } from "@common/ui/components/propertyeditor/PropertyController";
import { testProfile, testValues } from "@common/ui/components/propertyeditor/DummyData";
import { dataCite } from "@common/ui/components/propertyeditor/profiles/datacite";
import { osf } from "@common/ui/components/propertyeditor/profiles/osf";
import { PropertySet, type PersistedPropertySet, PersistedSet } from "@common/ui/components/propertyeditor/PropertySet";
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

/*
 deserialize PersistedSet -> e.g. testvalues = { profile_id = {PersistedSet}.profile_id, {PersistedSet}.categories}
 */

try {
    profiles.push(new PropertySet(testProfile, testValues));
} catch (e: any) {
    logging.error(e, "propertyeditor");
}
/* Testdata */

const controller = reactive(new MetadataController(profiles, baseSet, mergeSet)) as MetadataController;

const handleMetadataUpdate: Function = (data: PersistedSet) => {
    logging.debug(`Received update from PropertyEditor: ${JSON.stringify(data)}`, "ProjectDetails");
};
</script>

<template>
    <div><PropertyEditor @update="(data: PersistedSet) => handleMetadataUpdate(data)" :controller="controller" :logging="logging" twoCol /></div>
</template>

<style scoped lang="scss"></style>
