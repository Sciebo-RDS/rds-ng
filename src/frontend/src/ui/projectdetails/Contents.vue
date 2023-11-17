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
} catch (e) {
    logging.error(e, "propertyeditor");
}
try {
    profiles.push(new PropertySet(testProfile, testValues));
} catch (e) {
    logging.warning(e, "propertyeditor");
}

const controller = reactive(new MetadataController(profiles));
</script>

<template>
    <div class="p-10 overflow-y-auto">
        <PropEditor :controller="controller" :logging="logging" />
    </div>
</template>

<style scoped lang="scss"></style>
