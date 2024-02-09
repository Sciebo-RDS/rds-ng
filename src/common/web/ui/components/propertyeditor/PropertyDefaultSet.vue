<script setup lang="ts">
import { ref, computed } from "vue";
import Button from "primevue/button";
import Menu from "primevue/menu";
import Toolbar from "primevue/toolbar";

import { ExportersCatalog } from "@common/ui/components/propertyeditor/exporters/ExportersCatalog";
import PropertyCategory from "./PropertyCategory.vue";

const props = defineProps(["controller", "project", "exporters"]);

const menu = ref();
const items = computed(() => {
    const downloadItems = ExportersCatalog.byID(props.exporters).map((e) => {
        return {
            label: e.options.menuItem.label,
            icon: e.options.menuItem.icon,
            command: () => {
                e.options.menuItem.command(props.controller, props.project?.title);
            },
        };
    });
    return !!downloadItems.length
        ? [
              {
                  label: "Download",
                  items: downloadItems,
              },
          ]
        : [];
});

const toggle = (event) => {
    menu.value.toggle(event);
};

let defaultCategories = props.controller.getDefaultCategories();
let defaultProfile = props.controller.getDefaultProfile();
</script>

<template>
    <PropertyCategory
        v-for="[i, category] of defaultCategories.entries()"
        :project="project"
        :category="category"
        :profileId="defaultProfile"
        :index="i"
        class="mt-5"
        defaultSet
    />
</template>
