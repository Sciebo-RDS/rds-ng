<script setup lang="ts">
import Button from "primevue/button";
import Chip from "primevue/chip";
import Dialog from "primevue/dialog";
import FloatLabel from "primevue/floatlabel";
import InputText from "primevue/inputtext";
import OrderList from "primevue/orderlist";

import { computed, ref, type Ref } from "vue";
import { useColorsStore } from "../../../data/stores/ColorsStore";

import { ProjectObjectStore } from "./ProjectObjectStore";
import PropertyOneCol from "./PropertyOneCol.vue";
import { ProfileLayoutClass, PropertyProfile } from "./PropertyProfile";

const props = defineProps(["controller", "project", "projectProfiles", "projectObjects", "sharedObjectStore"]);
const colorsStore = useColorsStore();

const getLayout = () => {
    let layout: ProfileLayoutClass[] = [];
    for (const profile of props.projectProfiles.list() as PropertyProfile[]) {

        for (const p of profile.getLayout()) {
            const x: ProfileLayoutClass | undefined = layout.find((xd: ProfileLayoutClass) => p.id == xd.id);
            if (x !== undefined) {
                x.addProfile(profile.getId());
                if (p.required) x["required"] = true;
            } else {
                p["profiles"] = [profile.getId()];
                layout.push(p);
            }
        }
    }
    return layout;
};

const layout = getLayout();

const propsToShow = ref<ProfileLayoutClass[]>(
    layout
        .filter((e: ProfileLayoutClass) => e.required || props.projectObjects.get(e.id) !== undefined)
        .sort((a: ProfileLayoutClass, b: ProfileLayoutClass) => -a.profiles!.length - -b.profiles!.length)
);

const selectedProperties = ref([]) as Ref<ProfileLayoutClass[]>;
const unselectProperties = () => (selectedProperties.value = []);
const selectProperties = (selection: ProfileLayoutClass[]) => (selectedProperties.value = selection);

// TODO FIXME this
const hideProperty = (id: string) => {
    propsToShow.value = propsToShow.value.filter((e: ProfileLayoutClass) => e.id != id);
};

const showAddProperties = ref(false);
const hiddenPropertys = computed(() => layout.filter((e: ProfileLayoutClass) => !propsToShow.value.map((e: ProfileLayoutClass) => e.id).includes(e.id)));

const filteredProperties = computed(() =>
    hiddenPropertys.value.filter(
        (e: ProfileLayoutClass) =>
            e.label.toLowerCase().includes(searchString.value.toLowerCase()) || e.description?.toLowerCase().includes(searchString.value.toLowerCase())
    )
);

const searchString = ref("");
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
        header="Add Properties"
        :pt="{ content: { class: 'h-full' } }"
        :style="{ width: '50vw', height: '80vh' }"
        @after-hide="
            unselectProperties();
            searchString = '';
        "
    >
        <template #default>
            <div class="h-full flex-col flex space-y-4">
                <FloatLabel>
                    <InputText type="text" v-model="searchString" id="searchString" class="w-full" />
                    <label for="searchString">Search...</label>
                </FloatLabel>
                <OrderList
                    v-model="filteredProperties"
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
                                    :style="`background-color: ${colorsStore.color(p[0])}`"
                                    class="h-4 !rounded p-2.5 text-sm self-center bg-opacity-40"
                            /></span>
                            <span class="text-gray-500 ellipsis line-clamp-1" :title="slotProps.item.description">{{ slotProps.item.description }}</span>
                        </div>
                    </template>
                </OrderList>
            </div>
        </template>
        <template #footer>
            <div class="flex justify-end gap-2 mt-5">
                <Button
                    :disabled="!selectedProperties.length"
                    @click="
                        propsToShow.push(...selectedProperties);
                        unselectProperties();
                        searchString = '';
                        showAddProperties = false;
                    "
                    >Add {{ selectedProperties.length ? "(" + selectedProperties.length + ")" : "" }}
                </Button>
                <Button
                    outlined
                    severity="secondary"
                    @click="
                        unselectProperties();
                        searchString = '';
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
