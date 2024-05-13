<script setup lang="ts">
import { ref, computed, provide, reactive, unref } from "vue";
import Button from "primevue/button";
import Menu from "primevue/menu";
import Fieldset from "primevue/fieldset";
import Toolbar from "primevue/toolbar";
import ContextMenu from "primevue/contextmenu";
import Dropdown from "primevue/dropdown";
import Listbox from "primevue/listbox";

import { ExportersCatalog } from "./exporters/ExportersCatalog";
import PropertyCategory from "./PropertyCategory.vue";
import PropertyOneCol from "./PropertyOneCol.vue";
import { ProjectObject, ProjectObjectStore } from "./ProjectObjectStore";

const props = defineProps(["controller", "profile", "project", "exporters", "projectProfiles", "projectObjects"]);
provide("profileId", props.profile["metadata"]["id"]);

/* const menu = ref();
const items = computed(() => {
    const downloadItems = ExportersCatalog.byID(props.exporters).map((e) => {
        return {
            label: e.options.menuItem.label,
            icon: e.options.menuItem.icon,
            command: () => {
                e.options.menuItem.command(props.controller, props.project?.title);
            }
        };
    });
    return !!downloadItems.length
        ? [
              {
                  label: "Download",
                  items: downloadItems
              }
          ]
        : [];
});

const toggle = (event: Event) => {
    menu.value.toggle(event);
};*/

const menu = ref();
const items = ref([
    {
        label: "info",
        icon: "pi pi-info-circle",
        command: () => {
            console.log(selected);
        }
    }
]);

let selected = ref();
const onRightClick = (event, p) => {
    selected = p;

    menu.value.show(event);
};

var propsToShow = ref(props.profile["layout"].filter((e) => e.required || props.projectObjects.get(e.id) !== undefined));
const selectedProperty = ref();

// TODO FIXME this
const hideProperty = (id: string) => {
    propsToShow.value = propsToShow.value.filter((e) => e.id != id);
};

const showAddProperties = ref(false);
const hiddenPropertys = computed(() => props.profile["layout"].filter((e) => !propsToShow.value.map((e) => e.id).includes(e.id)));
</script>

<template>
    <Toolbar :pt="{ root: { class: '!py-2 border-0 border-y-4 rounded-none' } }">
        <template #start>
            <div class="text-xl font-bold truncate text-clip" :title="profile['metadata']['name'] + ' v' + profile['metadata']['version']">
                {{ `${profile["metadata"]["name"]} v${profile["metadata"]["version"]}` }}
            </div>
        </template>
        <template #center class="flex grow"> </template>
        <template #end>
            <!-- <Button
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
            <Menu ref="menu" id="overlay_menu" :model="items" :popup="true" />-->
        </template>
    </Toolbar>

    <PropertyOneCol
        v-for="p in propsToShow"
        class="mt-2 mb-4"
        :propertyClass="p"
        :profileId="props.profile['metadata']['id']"
        :projectObjects="projectObjects"
        :projectProfiles="projectProfiles"
        @contextmenu="onRightClick($event, p)"
        @hide="
            (id) => {
                hideProperty(id);
            }
        "
    />
    <ContextMenu ref="menu" :model="items" />

    <Button v-show="hiddenPropertys.length > 0" v-if="!showAddProperties" outlined class="my-5 ml-auto block" @click="showAddProperties = true"
        >Add Property</Button
    >
    <Fieldset v-else legend="Add Property" class="mb-10">
        <div class="flex">
            <Listbox
                v-model="selectedProperty"
                :options="hiddenPropertys"
                filter
                optionLabel="label"
                class="w-full md:w-14rem border-0"
                listStyle="max-height:250px; min-height:250px; overflow-y: scroll; background-color: #f9f9f9; margin-top: 10px"
            >
                <template #option="{ option }">
                    <div class="flex flex-col">
                        <span class="font-semibold" :title="option.label">{{ option.label }}</span>
                        <span class="text-gray-400 ml-3 ellipsis line-clamp-1" :title="option.description">{{ option.description }}</span>
                    </div>
                </template>
            </Listbox>
        </div>
        <div class="flex justify-end gap-2 mt-5">
            <Button
                :disabled="!selectedProperty"
                @click="
                    propsToShow.push(selectedProperty);
                    selectedProperty = null;
                    showAddProperties = false;
                "
                >Add</Button
            >
            <Button
                outlined
                severity="secondary"
                @click="
                    selectedProperty = null;
                    showAddProperties = false;
                "
                >Cancel</Button
            >
        </div>
    </Fieldset>
</template>
