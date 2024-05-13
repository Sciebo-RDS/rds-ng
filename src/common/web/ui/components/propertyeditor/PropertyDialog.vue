<script setup lang="ts">
import { ref, inject, computed, watch } from "vue";

import Breadcrumb from "primevue/breadcrumb";
import Card from "primevue/card";
import { ProjectObject, type ProjectObjectStore } from "./ProjectObjectStore";
import PropertyOneCol from "./PropertyOneCol.vue";
import { PropertyDataType } from "./PropertyProfile";
import { propertyDataForms, type Property } from "./PropertyProfile";
import OverlayPanel from "primevue/overlaypanel";
import Chip from "primevue/chip";
import Skeleton from "primevue/skeleton";
import NewPropertyButton from "./NewPropertyButton.vue";
import LinkedItemButton from "./LinkedItemButton.vue";
import Button from "primevue/button";

const dialogRef = inject("dialogRef");

const id = dialogRef.value.data.id;

const projectObjects = dialogRef.value.data.projectObjectStore;
const projectProfiles = dialogRef.value.data.propertyProfileStore;
const profileId = dialogRef.value.data.profileId;
let object = ref(projectObjects.get(id));
const objectClass = projectProfiles.getClassById(profileId, object.value["type"]);

const displayableInputs = objectClass["input"] || [];

const addableTypes = objectClass["type"] || [];

const linkedObjects = computed(() => projectObjects.getLinkedObjects(object.value.id));

let path = [id];
let menuPath = ref();
updatePath(path.length - 1);

function updatePath(i: number) {
    path = path.slice(0, i + 1);
    menuPath.value = path.map((obj, i) => {
        return {
            label: obj,
            command: () => {
                updatePath(i);
                object.value = projectObjects.get(obj);
            }
        };
    });
}

const example = objectClass.example ? `<b>Example</b>: ${objectClass.example}` : null;

const op = ref();
const toggle = (event: Event) => {
    op.value.toggle(event);
};
const linkedItemActions = ref((id: string) => [
    {
        label: "Unlink",
        icon: "pi pi-minus",
        command: () => {
            console.log("Unlinking " + id);
            projectObjects.removeLink(object.value.id, id);
        }
    },
    {
        label: "Delete",
        icon: "pi pi-trash",
        command: () => {
            console.log("Deleting " + id);
            projectObjects.remove(id);
        }
    }
]);

const loadObject = (id: string) => {
    if (id === object.value.id) {
        return;
    }
    if (path.includes(id)) {
        const i = path.indexOf(id);
        updatePath(i);
        object.value = projectObjects.get(id);
        return;
    }
    path.push(id);
    updatePath(path.length - 1);
    object.value = projectObjects.get(id);
};
</script>

<template>
    <Card :pt="{ root: { class: 'shadow-none' }, body: { class: 'pl-1 p-0' } }">
        <template #header>
            <Breadcrumb
                :model="menuPath"
                :pt="{
                    root: { class: 'px-0 pt-0' },
                    menu: { class: ' flex flex-wrap' },
                    separator: { class: 'mb-2' },
                    label: { class: 'text-red-900 opacity-80 hover:opacity-100 cursor-pointer truncate mb-2' }
                }"
            />
        </template>
        <template #title>
            <div class="row-span-1 text-gray-800 justify-between flex items-center">
                <span :title="object.label">
                    <span class="text-xl"> {{ objectClass.label }}</span>
                    <Button unstyled @click="toggle">
                        <i v-if="objectClass.description" class="pi pi-question-circle mx-2" style="font-size: 1rem" />
                    </Button>
                    <OverlayPanel ref="op" class="max-w-lg">
                        {{ objectClass.description }}
                        <p :v-if="objectClass.example" class="mt-2" v-html="example"></p>
                    </OverlayPanel>
                </span>
                <!-- {{ object }} -->

                <span class="mr-auto ml-5 flex space-x-1">
                    <NewPropertyButton
                        v-for="t in addableTypes"
                        :key="t"
                        :type="t"
                        :parentId="object.id"
                        :profileId="profileId"
                        :projectObjects="projectObjects"
                        :projectProfiles="projectProfiles"
                        mode="dialog"
                        @loadObject="(id) => loadObject(id)"
                    />
                </span>

                <Chip label="RepoLabel" size="small" class="bg-[#83d5ff] h-4 !rounded px-2 py-3 text-sm bg-opacity-40" />
            </div>
        </template>
        <template #content>
            <div class="flex flex-row">
                <div class="grow">
                    <!-- <span class="bg-blue-100">
                        {{ object }}
                    </span>
                    {{ linkedObjects }} -->
                    <!--  Header Row -->

                    <!--                     {{ projectObjects.get(object.id) }} {{ projectObjects._objects.length }}

                    {{ objectClass }} -->

                    <!--  Linked Items Row -->
                    <div class="row-span-1 flex mb-3 flex-wrap">
                        <LinkedItemButton
                            v-for="i in linkedObjects"
                            :key="i"
                            class="m-1"
                            :linkedItemActions="linkedItemActions"
                            :item="i"
                            :profileId="profileId"
                            :projectObjects="projectObjects"
                            :projectProfiles="projectProfiles"
                            mode="dialog"
                            @loadObject="(id) => loadObject(id)"
                        />
                        <Skeleton v-if="linkedObjects?.length === 0 && addableTypes.length > 0" height="2rem" width="20rem" class="mb-2" />
                    </div>
                    <!-- Simple Input Row -->
                    <div class="space-y-3">
                        <div v-for="input in displayableInputs" class="row-span-1">
                            <span v-if="input.label !== objectClass.label">{{ input.label }}</span>
                            <component
                                :is="propertyDataForms[input['type'] as PropertyDataType]"
                                class="w-full"
                                :propertyObjectId="object['id']"
                                :projectObjects="projectObjects"
                                :inputId="input['id']"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </Card>
</template>
