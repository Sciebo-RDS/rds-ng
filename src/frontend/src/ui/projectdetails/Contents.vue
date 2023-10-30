<script setup lang="ts">
import { reactive } from "vue";
import TabMenu from "primevue/tabmenu";
import { MetadataController } from "@/ui/propeditor/PropertyController";
import {
    PropertyProfile,
    testProfile,
    testValues,
} from "@/ui/propeditor/PropertyProfile";
import { PropertySet } from "@/ui/propeditor/PropertySet";
import PropEditor from "@/ui/propeditor/PropEditor.vue";

const controller = reactive(
    new MetadataController(
        testProfile,
        new PropertySet(["Test Profile", "1.1.1"], testValues)
    )
);
</script>

<template>
    <div class="m-10">
        <PropEditor :controller="controller" />
    </div>
</template>

<style scoped lang="scss"></style>
