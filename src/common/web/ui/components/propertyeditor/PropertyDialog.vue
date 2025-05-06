<script setup lang="ts">
import { computed, type ComputedRef, inject, reactive, ref, type Ref } from "vue";

import Breadcrumb from "primevue/breadcrumb";
import Button from "primevue/button";
import Card from "primevue/card";
import Menu from "primevue/menu";
import type { MenuItem } from "primevue/menuitem";
import ScrollPanel from "primevue/scrollpanel";
import SplitButton from "primevue/splitbutton";

import Fieldset from "primevue/fieldset";

import { WebComponent } from "../../../component/WebComponent";
import { History } from "./Breadcrumbs";
import EntityColumnHeader from "./EntityColumn/EntityColumnHeader.vue";
import EntityColumnInputs from "./EntityColumn/EntityColumnInputs.vue";
import EntityColumnLinkedItems from "./EntityColumn/EntityColumnLinkedItems.vue";
import { PropertyObjectStore, SharedPropertyObject } from "./PropertyObjectStore";
import { ProfileClass, ProfileClassRef } from "./PropertyProfile";
import { PropertyProfileStore } from "./PropertyProfileStore";
import { calcObjLabel } from "./utils/ObjectUtils";
import { linkableObjects, linkedItemActions } from "./utils/PropertyEditorUtils";

const dialogRef = inject("dialogRef") as any;
const {
    id,
    propertyObjects,
    sharedPropertyObjectStore,
    projectProfiles
}: { id: string; propertyObjects: PropertyObjectStore; sharedPropertyObjectStore: PropertyObjectStore; projectProfiles: PropertyProfileStore } =
    dialogRef.value.data;

// selected object
const propertyObject = ref(sharedPropertyObjectStore.get(id)!) as Ref<SharedPropertyObject>;
let propertyClass = reactive(projectProfiles.getClassById(propertyObject.value.getType())!) as ProfileClass;
const referencedObjects = computed(() => propertyObject.value.getReferences().map((e) => sharedPropertyObjectStore.get(e))) as ComputedRef<
    SharedPropertyObject[]
>;

const displayableInputs = ref(propertyClass.getInputs());
const addableTypes = ref(propertyClass.getRefTypes()) as Ref<ProfileClassRef[]>;

const addableExlineTypes = computed(() => addableTypes.value.filter((t) => !t.isInline()));
const addableInlineTypes = computed(() => addableTypes.value.filter((t) => t.isInline()));

// History for Breadcrumbs
const history = new History();
const menuPath = ref();

function selectActiveObject(id: string) {
    propertyObject.value = sharedPropertyObjectStore.get(id) as SharedPropertyObject;
    propertyClass = projectProfiles.getClassById(propertyObject.value.getType())! as ProfileClass;
    addableTypes.value = propertyClass.getRefTypes();
    displayableInputs.value = propertyClass.getInputs();
    history.navigateTo(propertyObject.value);
    // TODO optimize by only updating necessary elements
    menuPath.value = history.list().map((item: SharedPropertyObject) => {
        const obj = sharedPropertyObjectStore.get(item.getId()) as SharedPropertyObject;

        return {
            label: `${projectProfiles.getClassLabelById(item.getType())}:  ${calcObjLabel(obj!, projectProfiles)}`,
            command: () => selectActiveObject(item.getId())
        };
    });
}

selectActiveObject(id);

const comp = WebComponent.instance;

const inlineMenuRef = ref({}) as Ref<{ [key: string]: any }>;

const itemActions = (property: SharedPropertyObject) =>
    linkedItemActions(
        comp,
        propertyObjects,
        sharedPropertyObjectStore,
        propertyObject.value.getId(),
        property.getId(),
        projectProfiles.getClassById(property.getType())?.getDisplayLabel()!
    );

const linkableByClass = (classId: string) => {
    return linkableObjects(propertyObjects, sharedPropertyObjectStore, projectProfiles, propertyObject.value.getId(), classId).length
        ? linkableObjects(propertyObjects, sharedPropertyObjectStore, projectProfiles, propertyObject.value.getId(), classId).sort((a: any, b: any) =>
              a.label > b.label ? 1 : b.label > a.label ? -1 : 0
          )
        : [
              {
                  label: `No linkable ${projectProfiles.getClassById(classId)?.getDisplayLabel()}(s) available`,
                  disabled: true
              }
          ];
};

function createObject(type: string) {
    const newObject = new SharedPropertyObject(type);

    sharedPropertyObjectStore.add(newObject);
    sharedPropertyObjectStore.addRef(propertyObject.value.getId(), newObject.getId());
}
</script>

<template>
    <ScrollPanel class="h-full pr-5">
        <Card :pt="{ root: 'shadow-none', body: 'pl-1 p-0 overflow-hidden' }">
            <template #header>
                <Breadcrumb
                    :model="menuPath as MenuItem[]"
                    class="max-w-full w-full grid grid-cols-1"
                    :pt="{
                        root: { class: 'px-0 pt-0' },
                        list: { class: ' flex flex-wrap ' },
                        separator: { class: 'mb-2' },
                        item: { class: 'max-w-full breadcrumbs-item' },
                        itemLabel: { class: 'text-red-900 opacity-80 hover:opacity-100 cursor-pointer truncate pb-2' }
                    }"
                />
            </template>
            <template #title>
                <!--  Header Row -->

                <EntityColumnHeader
                    :addableTypes="addableTypes"
                    :propertyClass="propertyClass"
                    :propertyObject="propertyObject"
                    :propertyObjects="propertyObjects"
                    :sharedPropertyObjectStore="sharedPropertyObjectStore"
                    :projectProfiles="projectProfiles"
                    :isDialog="true"
                    @loadObject="(id) => selectActiveObject(id)"
                />
            </template>
            <template #content>
                <div class="flex flex-row">
                    <div class="grow max-w-full space-y-4">
                        <!--  Linked Items Row -->

                        <EntityColumnLinkedItems
                            v-if="!!addableExlineTypes.length"
                            :propertyObjects="propertyObjects"
                            :propertyClass="propertyObject"
                            :sharedPropertyObjectStore="sharedPropertyObjectStore"
                            :projectProfiles="projectProfiles"
                            :addableTypes="addableExlineTypes"
                            :propertyObject="propertyObject"
                            :isDialog="true"
                            @loadObject="(id) => selectActiveObject(id)"
                        />
                        <!-- Simple Input Row -->
                        <EntityColumnInputs
                            v-if="displayableInputs.length > 0"
                            :displayableInputs="displayableInputs"
                            :propertyObject="propertyObject"
                            :propertyObjects="sharedPropertyObjectStore"
                            :propertyClass="propertyClass"
                            :isDialog="true"
                        />

                        <Fieldset
                            v-for="t in addableInlineTypes"
                            class="rounded-md"
                            :class="{ 'border-0': referencedObjects.filter((e) => e.getType() === t.getClassId()).length === 0 }"
                            :pt="{ content: 'p-0' }"
                        >
                            <template #legend>
                                <SplitButton
                                    @click="() => createObject(t.getClassId())"
                                    class="p-0"
                                    icon="pi pi-plus"
                                    dropdownIcon="pi pi-link"
                                    severity="primary"
                                    outlined
                                    :label="projectProfiles.getClassById(t.getClassId())!.getDisplayLabel()"
                                    :title="projectProfiles.getClassById(t.getClassId())!.getDescription()"
                                    :disabled="
                                        !t.allowsMultiple() && referencedObjects.filter((e: SharedPropertyObject) => e.getType() === t.getClassId()).length > 0
                                    "
                                    :model="linkableByClass(t.getClassId())"
                                />
                            </template>
                            <div class="space-y">
                                <div
                                    v-for="[i, refObject] of referencedObjects.filter((e: SharedPropertyObject) => e.getType() === t.getClassId()).entries()"
                                    class="row-span-1 last-fieldset-round [&:not(:first-child)]:mt-5"
                                >
                                    <Fieldset class="bg-sky-50 rounded-none border-y p-2 legend-right">
                                        <template #legend class="m-0 p-0">
                                            <div class="flex items-center space-x-3">
                                                <span>
                                                    <Button
                                                        class="[&:not(:hover)]:bg-white"
                                                        type="button"
                                                        icon="pi pi-ellipsis-v"
                                                        @click.stop="(event) => inlineMenuRef[refObject.getId()].toggle(event)"
                                                        aria-haspopup="true"
                                                        aria-controls="overlay_menu"
                                                        outlined
                                                        size="small"
                                                    />
                                                    <Menu
                                                        :ref="
                                                            (el) => {
                                                                inlineMenuRef[refObject.getId()] = el;
                                                            }
                                                        "
                                                        id="overlay_menu"
                                                        :model="itemActions(refObject)"
                                                        :popup="true"
                                                    />
                                                </span>
                                            </div>
                                        </template>
                                        <EntityColumnInputs
                                            v-if="!!projectProfiles.getClassById(t.getClassId())?.getInputs().length"
                                            class="mt-2"
                                            :displayableInputs="projectProfiles.getClassById(t.getClassId())?.getInputs()"
                                            :propertyObject="refObject"
                                            :propertyObjects="sharedPropertyObjectStore"
                                            :propertyClass="propertyClass"
                                            :isDialog="true"
                                        />
                                    </Fieldset>
                                </div>
                            </div>
                        </Fieldset>
                    </div>
                </div>
            </template>
        </Card>
    </ScrollPanel>
</template>

<style scoped lang="scss">
:deep(.breadcrumbs-item:last-child) {
    @apply font-bold;
}

:deep(.p-fieldset-legend) {
    @apply p-0 ml-[-1px];
}

:deep(.legend-right > .p-fieldset-legend) {
    @apply ml-auto m-0 p-0 rounded bg-transparent;
}

.last-fieldset-round:last-child > .p-fieldset {
    @apply rounded-b-md mb-0;
}
</style>
