<script setup lang="ts">
import { computed, inject, reactive, ref, type Ref } from "vue";

import Breadcrumb from "primevue/breadcrumb";
import Button from "primevue/button";
import Card from "primevue/card";
import type { MenuItem } from "primevue/menuitem";
import OverlayPanel from "primevue/overlaypanel";
import { History } from "./Breadcrumbs";
import LinkedItemButton from "./LinkedItemButton.vue";
import NewPropertyButton from "./NewPropertyButton.vue";
import { ProjectObjectStore, SharedObject } from "./ProjectObjectStore";
import { ProfileClass, PropertyDataType, propertyDataForms } from "./PropertyProfile";
import { PropertyProfileStore } from "./PropertyProfileStore";
import { calcObjLabel } from "./utils/ObjectUtils";

const dialogRef = inject("dialogRef") as any;
const {
    id,
    projectObjects,
    sharedObjectStore,
    projectProfiles
}: { id: string; projectObjects: ProjectObjectStore; sharedObjectStore: ProjectObjectStore; projectProfiles: PropertyProfileStore } = dialogRef.value.data;

// selected object
const object = ref(sharedObjectStore.get(id)!) as Ref<SharedObject>;
let objectClass = reactive(projectProfiles.getClassById(object.value["type"]!)!) as ProfileClass;

const displayableInputs = ref(objectClass["input"] || []);
const addableTypes = ref(objectClass["type"] || []);

const linkedObjects = computed(() => sharedObjectStore.getReferencedObjects(object.value.id));

// History for Breadcrumbs
const history = new History();
const menuPath = ref();

// Description Overlay
const op = ref();
const toggle = (event: Event) => {
    op.value.toggle(event);
};

function selectActiveObject(id: string) {
    object.value = sharedObjectStore.get(id)! as SharedObject;
    objectClass = projectProfiles.getClassById(object.value["type"]!)! as ProfileClass;
    addableTypes.value = objectClass["type"] || [];
    displayableInputs.value = objectClass["input"] || [];
    history.navigateTo(object.value);
    // TODO optimize by only updating necessary elements
    menuPath.value = history.list().map((item: SharedObject) => {
        const obj = sharedObjectStore.get(item.id) as SharedObject;

        return {
            label: `${projectProfiles.getClassLabelById(item.type!)}:  ${calcObjLabel(obj!, projectProfiles)}`,
            command: () => selectActiveObject(item.id)
        };
    });
}

selectActiveObject(id);
</script>

<template>
    <Card :pt="{ root: { class: 'shadow-none' }, body: { class: 'pl-1 p-0 overflow-hidden' } }">
        <template #header>
            <Breadcrumb
                :model="menuPath as MenuItem[]"
                class="max-w-full w-full grid grid-cols-1"
                :pt="{
                    root: { class: 'px-0 pt-0' },
                    menu: { class: ' flex flex-wrap ' },
                    separator: { class: 'mb-2' },
                    menuItem: { class: 'max-w-full' },
                    label: { class: 'text-red-900 opacity-80 hover:opacity-100 cursor-pointer truncate pb-2 ' }
                }"
            />
        </template>
        <template #title>
            <div class="row-span-1 text-gray-800 justify-between flex items-start">
                <span :title="objectClass.label" class="flex-none">
                    <span class="text-xl"> {{ objectClass.label }}</span>
                    <Button v-if="objectClass.description" unstyled @click="toggle">
                        <i class="pi pi-question-circle mx-2" style="font-size: 1rem" />
                    </Button>
                    <OverlayPanel ref="op" class="max-w-lg">
                        {{ objectClass.description }}
                        <span v-if="objectClass.example" v-html="`<br/>Example: ${objectClass.example}`" />
                    </OverlayPanel>
                </span>

                <span class="mr-auto ml-5 flex gap-1 flex-wrap">
                    <NewPropertyButton
                        v-for="t in addableTypes"
                        :key="t"
                        :type="t"
                        :parentId="object.id"
                        :projectObjects="projectObjects"
                        :sharedObjectStore="sharedObjectStore as ProjectObjectStore"
                        :projectProfiles="projectProfiles"
                        mode="dialog"
                        @loadObject="(id) => selectActiveObject(id)"
                    />
                </span>
            </div>
        </template>
        <template #content>
            <div class="flex flex-row">
                <div class="grow max-w-full space-y-4">
                    <!--  Linked Items Row -->

                    <div
                        v-if="addableTypes !== undefined && addableTypes.length > 0"
                        class="row-span-1 flex mt-3 p-2 flex-wrap gap-0.5 rounded-md"
                        style="
                            box-shadow:
                                0 0 #0000,
                                0 0 #0000,
                                0 1px 2px 0 rgba(18, 18, 23, 0.05);
                            transition:
                                background-color 0.2s,
                                color 0.2s,
                                border-color 0.2s,
                                box-shadow 0.2s,
                                outline-color 0.2s;
                            border: 1px dashed #b6bfca;
                        "
                    >
                        <LinkedItemButton
                            v-if="linkedObjects.length > 0"
                            v-for="i in linkedObjects"
                            :key="i"
                            class="m-1 max-w-full"
                            :item-id="i"
                            :parentId="object.id"
                            :projectObjects="projectObjects"
                            :sharedObjectStore="sharedObjectStore as ProjectObjectStore"
                            :projectProfiles="projectProfiles"
                            mode="dialog"
                            @loadObject="(id) => selectActiveObject(id)"
                        />
                        <span v-else class="text-gray-500 m-1 my-3 place-self-center align-middle inline-block"
                            >No
                            <span class="italic">
                                {{
                                    addableTypes
                                        .map((e) => projectProfiles.getClassLabelById(e))
                                        .join(", ")
                                        .replace(/, ([^,]*)$/, " or $1")
                                }}
                            </span>
                            linked</span
                        >
                    </div>
                    <!-- Simple Input Row -->
                    <div class="space-y-5">
                        <div v-for="input in displayableInputs" class="row-span-1 space-y-1">
                            <div v-if="input.label !== objectClass.label" class="font-bold mb-1 font">{{ input.label }}</div>
                            {{ input.description }}
                            <span v-if="input.example" v-html="`<br/>Example: ${input.example}`" />
                            <component
                                :is="propertyDataForms[input['type'] as PropertyDataType]"
                                class="w-full"
                                :propertyObjectId="object['id']"
                                :projectObjects="sharedObjectStore"
                                :sharedObjectStore="sharedObjectStore as ProjectObjectStore"
                                :inputId="input['id']"
                                :inputOptions="input['options'] ? input['options'] : []"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </Card>
</template>

<style scoped lang="scss">
:deep(.p-menuitem:last-child) {
    @apply font-bold;
}
</style>
