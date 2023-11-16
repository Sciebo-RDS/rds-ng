<script setup lang="ts">
import { reactive } from "vue";
import { MetadataController } from "@/ui/propeditor/PropertyController";
import { dataCite, testProfile, testValues } from "@/ui/propeditor/DummyData";
import { PropertySet } from "@/ui/propeditor/PropertySet";
import PropEditor from "@/ui/propeditor/PropEditor.vue";

const datacite = new PropertySet(dataCite, undefined);
const testprofile = new PropertySet(testProfile, testValues);

// TODO make sure Values and Profile match
const controller = reactive(new MetadataController([datacite, testprofile]));
</script>

<template>
    <div class="p-10 overflow-y-auto">
        <PropEditor :controller="controller" />
    </div>
</template>

<style scoped lang="scss"></style>
