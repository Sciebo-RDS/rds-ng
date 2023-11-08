<script setup lang="ts">
import { reactive } from "vue";
import { MetadataController } from "@/ui/propeditor/PropertyController";
import { testProfile, testValues } from "@/ui/propeditor/DummyData";
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
    <div class="p-10 overflow-y-auto">
        <PropEditor :controller="controller" />
    </div>
</template>

<style scoped lang="scss"></style>
