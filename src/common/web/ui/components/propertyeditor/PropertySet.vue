<script setup lang="ts">
import Button from "primevue/button";
import Chip from "primevue/chip";
import Dialog from "primevue/dialog";
import OrderList from "primevue/orderlist";

import { computed, ref, type Ref } from "vue";

import { ProjectObjectStore } from "./ProjectObjectStore";
import PropertyOneCol from "./PropertyOneCol.vue";
import { ProfileLayoutClass } from "./PropertyProfile";
import { ColorTable } from "./utils/ColorTable";

const props = defineProps(["controller", "project", "exporters", "projectProfiles", "projectObjects", "sharedObjectStore"]);

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

const getLayout = () => {
    let layout = [];
    for (const profile of props.projectProfiles.list()) {
        for (const p of profile["layout"]) {
            const x = layout.find((xd) => p.id == xd.id);
            if (x !== undefined) {
                x["profiles"].push(profile["metadata"]["id"]);
                if (p.required) x["required"] = true;
            } else {
                p["profiles"] = [profile["metadata"]["id"]];
                layout.push(p);
            }
        }
    }
    return layout;
};

const layout = getLayout();

const propsToShow = ref(layout.filter((e: ProfileLayoutClass) => e.required || props.projectObjects.get(e.id) !== undefined));

const selectedProperties = ref([]) as Ref<ProfileLayoutClass[]>;
const unselectProperties = () => (selectedProperties.value = []);
const selectProperties = (selection: ProfileLayoutClass[]) => (selectedProperties.value = selection);

// TODO FIXME this
const hideProperty = (id: string) => {
    propsToShow.value = propsToShow.value.filter((e: ProfileLayoutClass) => e.id != id);
};

const showAddProperties = ref(false);
const hiddenPropertys = computed(() => layout.filter((e: ProfileLayoutClass) => !propsToShow.value.map((e: ProfileLayoutClass) => e.id).includes(e.id)));
</script>

<template>
    <!--     <Toolbar :pt="{ root: { class: '!py-2 border-0 border-y-4 rounded-none' } }">
        <template #start>
            <div class="text-xl font-bold truncate text-clip" :title="profile['metadata']['name'] + ' v' + profile['metadata']['version']">
                {{ `${profile["metadata"]["name"]} v${profile["metadata"]["version"]}` }}
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
    </Toolbar> -->
    <div class="w-full max-w-full">
        <PropertyOneCol
            v-for="(p, i) in propsToShow"
            :key="p.id"
            :index="i"
            class="my-5 w-full max-w-full"
            :propertyClass="p"
            :profileId="layout.filter((e) => e.id == p.id)[0].profiles"
            :projectObjects="projectObjects"
            :sharedObjectStore="sharedObjectStore as ProjectObjectStore"
            :projectProfiles="projectProfiles"
            :layoutProfiles="layout"
            @hide="(id) => hideProperty(id)"
        />
    </div>
    <Button v-if="hiddenPropertys.length !== 0" class="fixed bottom-10 right-10" icon="pi pi-plus" size="large" rounded @click="showAddProperties = true" />

    <Dialog
        v-model:visible="showAddProperties"
        modal
        :header="`Add Properties ${selectedProperties.length ? '(' + selectedProperties.length + ')' : ''} `"
        :pt="{ content: { class: 'h-full' } }"
        :style="{ width: '50vw', height: '80vh' }"
        @hide="selectedProperties = []"
    >
        <template #default class="h-full">
            <OrderList
                v-model="hiddenPropertys"
                @update:selection="(selection: ProfileLayoutClass[]) => selectProperties(selection)"
                dataKey="id"
                class="h-full"
                :pt="{ list: { class: 'min-h-full' } }"
                :stripedRows="true"
            >
                <template #item="slotProps">
                    <div class="flex flex-col">
                        <span class="font-semibold flex gap-4" :title="slotProps.item.label"
                            >{{ slotProps.item.label }}
                            <Chip
                                v-for="p in slotProps.item.profiles"
                                :label="p[0]"
                                size="small"
                                :style="`background-color: ${ColorTable.color(p[0])}`"
                                class="h-4 !rounded p-2.5 text-sm self-center bg-opacity-40"
                        /></span>
                        <span class="text-gray-500 ellipsis line-clamp-1" :title="slotProps.item.description">{{ slotProps.item.description }}</span>
                    </div>
                </template>
            </OrderList>
        </template>
        <template #footer>
            <div class="flex justify-end gap-2 mt-5">
                <Button
                    :disabled="!selectedProperties.length"
                    @click="
                        propsToShow.push(...selectedProperties);
                        unselectProperties();
                        showAddProperties = false;
                    "
                    >Add
                </Button>
                <Button
                    outlined
                    severity="secondary"
                    @click="
                        unselectProperties();
                        showAddProperties = false;
                    "
                    >Cancel
                </Button>
            </div>
        </template>
    </Dialog>
</template>

<style scoped lang="scss">
:deep(.p-orderlist-controls) {
    display: none;
}

:deep(.p-orderlist-item) {
    @apply border-l-2 border-solid border-transparent;
}

:deep(.p-highlight) {
    @apply bg-emerald-50  border-l-2 border-emerald-600 text-slate-700;
}
</style>
