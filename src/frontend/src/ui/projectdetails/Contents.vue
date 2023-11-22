<script setup lang="ts">
import { reactive } from "vue";
import { MetadataController } from "@/ui/propeditor/PropertyController";
import { dataCite, testProfile, testValues } from "@/ui/propeditor/DummyData";
import { PropertySet } from "@/ui/propeditor/PropertySet";
import PropEditor from "@/ui/propeditor/PropEditor.vue";
import logging from "@common/core/logging/Logging";

// TODO have a closer look at Toasts

const profiles: PropertySet[] = [];
try {
    profiles.push(new PropertySet(dataCite));
} catch (e: any) {
    logging.error(e, "propertyeditor");
}
try {
    profiles.push(new PropertySet(testProfile, testValues));
} catch (e: any) {
    logging.error(e, "propertyeditor");
}

const controller: MetadataController = reactive(
    new MetadataController(profiles)
);

const handleMetadataUpdate: Function = (data: any) => {
    logging.debug(
        `Received update from PropertyEditor: ${JSON.stringify(data)}`,
        "ProjectDetails"
    );
};
</script>

<template>
    <div class="p-10 overflow-y-auto">
        <PropEditor
            @update="(data: any) => handleMetadataUpdate(data)"
            :controller="controller"
            :logging="logging"
        />
    </div>
</template>

<style scoped lang="scss"></style>
