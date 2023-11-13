<script setup lang="ts">
import { reactive } from "vue";
import { MetadataController } from "@/ui/propeditor/PropertyController";
import { dataCite, testValues } from "@/ui/propeditor/DummyData";
import { PropertySet } from "@/ui/propeditor/PropertySet";
import PropEditor from "@/ui/propeditor/PropEditor.vue";

// TODO make sure Values and Profile match
const controller = reactive(
    new MetadataController(
        dataCite,
        new PropertySet(["DataCite", "4.4"], undefined)
    )
);
</script>

<template>
    <div class="p-10 overflow-y-auto">
        <PropEditor :controller="controller" />
    </div>
</template>

<style scoped lang="scss"></style>
