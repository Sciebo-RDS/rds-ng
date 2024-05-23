<script setup lang="ts">
import { ref, inject, computed, reactive } from "vue";

import Breadcrumb from "primevue/breadcrumb";
import Card from "primevue/card";
import { ProjectObject, type ProjectObjectStore } from "./ProjectObjectStore";
import { PropertyDataType } from "./PropertyProfile";
import { propertyDataForms, type Property } from "./PropertyProfile";
import OverlayPanel from "primevue/overlaypanel";
import Chip from "primevue/chip";
import NewPropertyButton from "./NewPropertyButton.vue";
import LinkedItemButton from "./LinkedItemButton.vue";
import { History } from "./Breadcrumbs";
import { injectTemplate } from "./utils/Templates";
import Button from "primevue/button";
import { type MenuItem } from "primevue/menuitem";

const dialogRef = inject("dialogRef") as any;

const dialogProps = new Proxy(dialogRef.value.options.props, {});

const id = dialogRef.value.data.id;

const projectObjects = dialogRef.value.data.projectObjectStore;
const projectProfiles = dialogRef.value.data.propertyProfileStore;
const profileId = dialogRef.value.data.profileId;
const object = ref(projectObjects.get(id));
let objectClass = reactive(projectProfiles.getClassById(profileId, object.value["type"]));
let displayableInputs = objectClass["input"] || [];
let addableTypes = objectClass["type"] || [];

const linkedObjects = computed(() => projectObjects.getLinkedObjects(object.value.id));

const history = new History();

var menuPath = ref();

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

function selectActiveObject(id: string) {
    object.value = projectObjects.get(id);
    objectClass = projectProfiles.getClassById(profileId, object.value["type"]);
    addableTypes = objectClass["type"] || [];
    displayableInputs = objectClass["input"] || [];
    history.navigateTo(object.value);
    console.log(history.list());
    // TODO optimize by only updating necessary elements
    menuPath.value = history.list().map((item) => {
        const cb: Function = () => {
            selectActiveObject(item.id);
        };
        const objectClass = projectProfiles.getClassById(item.profile, item.type);
        const injectedLabel = injectTemplate(objectClass.labelTemplate, projectObjects.get(item.id));
        const label = `${objectClass.label}: ${injectedLabel}`;
        return {
            label: label,
            command: cb
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
                        v-if="linkedObjects?.length !== 0"
                        :key="t"
                        :type="t"
                        :parentId="object.id"
                        :profileId="profileId"
                        :projectObjects="projectObjects"
                        :projectProfiles="projectProfiles"
                        mode="dialog"
                        @loadObject="(id) => selectActiveObject(id)"
                    />
                </span>

                <Chip label="RepoLabel" size="small" class="bg-[#83d5ff] h-4 !rounded px-2 py-3 text-sm bg-opacity-40" />
            </div>
        </template>
        <template #content>
            <div class="flex flex-row">
                <div class="grow max-w-full">
                    <!-- <span class="bg-blue-100">
                        {{ object }}
                    </span>
                    {{ linkedObjects }} -->
                    <!--  Header Row -->

                    <!--                     {{ projectObjects.get(object.id) }} {{ projectObjects._objects.length }}

                    {{ objectClass }} -->

                    <!--  Linked Items Row -->
                    <div v-if="addableTypes.length > 0" class="row-span-1 flex mb-5 flex-wrap space-x-1">
                        <LinkedItemButton
                            v-for="i in linkedObjects"
                            v-if="linkedObjects?.length !== 0"
                            :key="i"
                            class="m-1 max-w-full"
                            :linkedItemActions="linkedItemActions"
                            :item="i"
                            :profileId="profileId"
                            :projectObjects="projectObjects"
                            :projectProfiles="projectProfiles"
                            mode="dialog"
                            @loadObject="(id) => selectActiveObject(id)"
                        />
                        <NewPropertyButton
                            v-for="t in addableTypes"
                            v-else
                            :key="t"
                            :type="t"
                            :parentId="object.id"
                            :profileId="profileId"
                            :projectObjects="projectObjects"
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

<style scoped lang="scss">
:deep(.p-menuitem:last-child) {
    @apply font-bold;
}
</style>
