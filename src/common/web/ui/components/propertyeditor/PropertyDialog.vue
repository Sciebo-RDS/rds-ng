<script setup lang="ts">
import { computed, inject, reactive, ref } from "vue";

import Breadcrumb from "primevue/breadcrumb";
import Button from "primevue/button";
import Card from "primevue/card";
import type { MenuItem } from "primevue/menuitem";
import OverlayPanel from "primevue/overlaypanel";
import { History } from "./Breadcrumbs";
import LinkedItemButton from "./LinkedItemButton.vue";
import NewPropertyButton from "./NewPropertyButton.vue";
import { ProjectObjectStore } from "./ProjectObjectStore";
import { ProfileClass, PropertyDataType, propertyDataForms, type ProfileID } from "./PropertyProfile";
import { PropertyProfileStore } from "./PropertyProfileStore";

const dialogRef = inject("dialogRef") as any;
const { id, projectObjects, globalObjectStore, projectProfiles, profileId }: {id: string, projectObjects: ProjectObjectStore, globalObjectStore: ProjectObjectStore, projectProfiles: PropertyProfileStore, profileId: ProfileID}  = dialogRef.value.data;

const object = ref(globalObjectStore.get(id)!);
let objectClass = reactive(projectProfiles.getClassById(profileId, object.value["type"]!)!) as ProfileClass;
const displayableInputs = ref(objectClass["input"] || []);
const addableTypes = ref(objectClass["type"] || []);

const linkedObjects = computed(() => globalObjectStore.getLinkedObjects(object.value.id));

const history = new History();
const menuPath = ref();

const op = ref();
const toggle = (event: Event) => {
    op.value.toggle(event);
};

function selectActiveObject(id: string) {
    object.value = globalObjectStore.get(id)!;
    objectClass = projectProfiles.getClassById(profileId, object.value["type"]!)! as ProfileClass;
    addableTypes.value = objectClass["type"] || [];
    displayableInputs.value = objectClass["input"] || [];
    history.navigateTo(object.value);
    // TODO optimize by only updating necessary elements
    menuPath.value = history.list().map((item) => {
        const obj = globalObjectStore.get(item.id);
        
        return {
            label: `${projectProfiles.getClassLabelById(item.type!)}:  ${obj.instanceLabel(projectProfiles)}`,
            command: () => selectActiveObject(item.id)
        };
    });
}

selectActiveObject(id);
</script>

<template>
    <Card :pt="{ root: { class: 'shadow-none' }, body: { class: 'pl-1 p-0' } }">
        <template #header>
            <Breadcrumb
                :model="menuPath as MenuItem[]"
                :pt="{
                    root: { class: 'px-0 pt-0' },
                    menu: { class: ' flex flex-wrap' },
                    separator: { class: 'mb-2' },
                    label: { class: 'text-red-900 opacity-80 hover:opacity-100 cursor-pointer truncate pb-2' }
                }"
            />
        </template>
        <template #title>
            <div class="row-span-1 text-gray-800 justify-between flex items-center">
                <span :title="objectClass.label">
                    <span class="text-xl"> {{ objectClass.label }}</span>
                    <Button v-if="objectClass.description" unstyled @click="toggle">
                        <i class="pi pi-question-circle mx-2" style="font-size: 1rem" />
                    </Button>
                    <OverlayPanel ref="op" class="max-w-lg">
                        {{ objectClass.description }}
                    </OverlayPanel>
                </span>

                <span class="mr-auto ml-5 flex space-x-1">
                    <NewPropertyButton
                        v-for="t in addableTypes"
                        :key="t"
                        :type="t"
                        :parentId="object.id"
                        :profileId="profileId"
                        :projectObjects="projectObjects"
                        :globalObjectStore="globalObjectStore as ProjectObjectStore"
                        :projectProfiles="projectProfiles"
                        mode="dialog"
                        @loadObject="(id) => selectActiveObject(id)"
                    />
                </span>
            </div>
        </template>
        <template #content>
            <div class="flex flex-row">
                <div class="grow max-w-full">
                    <!--  Linked Items Row -->
                    <div class="row-span-1 flex my-3 flex-wrap gap-2">
                        <LinkedItemButton
                            v-for="i in linkedObjects"
                            :key="i"
                            class="m-1 max-w-full"
                            :item-id="i"
                            :parentId="object.id"
                            :profileId="profileId"
                            :projectObjects="projectObjects"
                            :globalObjectStore="globalObjectStore as ProjectObjectStore"
                            :projectProfiles="projectProfiles"
                            mode="dialog"
                            @loadObject="(id) => selectActiveObject(id)"
                        />
                    </div>
                    <!-- Simple Input Row -->
                    <div class="space-y-3">
                        <div v-for="input in displayableInputs" class="row-span-1">
                            <div v-if="input.label !== objectClass.label" class="font-bold">{{ input.label }}</div>
                            {{ input.description }} 
                            <span v-if="input.example" class="mt-2" v-html="`<b>Example</b>: ${input.example}`"/>
                            <component
                                :is="propertyDataForms[input['type'] as PropertyDataType]"
                                class="w-full"
                                :propertyObjectId="object['id']"
                                :projectObjects="globalObjectStore"
                                :globalObjectStore="globalObjectStore as ProjectObjectStore"
                                :inputId="input['id']"
                                :profileId="profileId"
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
