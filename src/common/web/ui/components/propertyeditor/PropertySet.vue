<script setup lang="ts">
import { ref, computed } from "vue";
import Button from "primevue/button";
import Menu from "primevue/menu";
import Toolbar from "primevue/toolbar";

import { ExportersCatalog } from "./exporters/ExportersCatalog";
import PropertyCategory from "./PropertyCategory.vue";

const props = defineProps(["controller", "profileId", "project", "exporters"]);

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

const toggle = (event: Event) => {
    menu.value.toggle(event);
};
</script>

<template>
    <Toolbar :pt="{ root: { class: '!py-2 !bg-gray-100' } }">
        <template #start>
            <div class="text-xl grow font-bold">
                {{ `${profileId["name"]} v${profileId["version"]}` }}
            </div>
        </template>
        <template #center class="flex grow"> </template>
        <template #end>
            <Button
                text
                :disabled="!items.length"
                iconPos="right"
                size="small"
                type="button"
                icon="pi pi-ellipsis-v"
                @click="toggle"
                aria-haspopup="true"
                aria-controls="overlay_menu"
            />
            <Menu ref="menu" id="overlay_menu" :model="items" :popup="true" />
        </template>
    </Toolbar>

    <PropertyCategory
        v-for="[i, category] of props.controller.getCategoryById(profileId).entries()"
        :project="project"
        :category="category"
        :profileId="profileId"
        :index="i"
        class="mt-5"
    />
</template>
