<script setup lang="ts">
import { ref, provide, inject, useAttrs } from "vue";
import Button from "primevue/button";
import Card from "primevue/card";
import Dropdown from "primevue/dropdown";
import Fieldset from "primevue/fieldset";
import Accordion from "primevue/accordion";
import AccordionTab from "primevue/accordiontab";

import { type Property as PropertyType } from "./PropertyProfile";
import { PropertyController } from "./PropertyController";
import PropertyOneCol from "./PropertyOneCol.vue";
import { PropertySet } from "./PropertySet";

const props = defineProps(["category", "profileId", "project", "index"]);

const controller = inject("controller") as PropertyController<PropertySet | PropertySet[]>;
const attrs = useAttrs();

provide("categoryId", props.category.id);
provide("profileId", props.profileId);

const showPropertySelector = ref(false);
const selectedProperties = ref<PropertyType>();

const propsToShow = !Object.prototype.hasOwnProperty.call(attrs, "defaultSet")
    ? ref<PropertyType[]>(
          props.category.properties.filter((p: PropertyType) => controller.getValue(props.profileId, props.category.id, p.id) != undefined || p.showAlways)
      )
    : ref<PropertyType[]>(props.category.properties);

const propsToSelect = ref(props.category.properties.filter((p: PropertyType) => !propsToShow.value.includes(p)));

function updatePropsToShow(e: any) {
    propsToShow.value = [...propsToShow.value, props.category.properties.filter((p: PropertyType) => p.name === e.value)[0] as PropertyType];
    propsToSelect.value = propsToSelect.value.filter((p: PropertyType) => !propsToShow.value.includes(p));
    showPropertySelector.value = false;
}

const header = `${props.index + 1}. ${props.category.name}`;
</script>

<template>
    <Accordion v-if="!Object.prototype.hasOwnProperty.call(attrs, 'defaultSet')" class="w-full">
        <AccordionTab :pt="{ header: { class: ['border-indigo-200', { 'border-t': index !== 0 }] }, headerAction: { class: 'pb-0 pt-5' } }">
            <template #header>
                <span class="flex align-items-center w-full !text-gray-800 truncate text-ellipsis mr-2" :title="header">
                    {{ header }}
                </span>
            </template>
            <Card
                class="drop-shadow-none"
                :pt="{ root: { class: '!shadow-none' }, content: { class: '!p-0' }, title: { class: '!text-xl' }, body: { class: '!p-0' } }"
            >
                <template #content>
                    <div class="text-neutral-700">{{ props.category.description }}</div>
                    <div class="divide-y">
                        <PropertyOneCol v-for="prop in propsToShow" :property="prop" class="mt-2 pt-5" />
                    </div>
                    <!-- Should have its own component -->
                    <div v-show="!showPropertySelector && !!propsToSelect.length" class="flex justify-end">
                        <Button label="Add Property" outlined size="small" icon="pi pi-plus" @click="showPropertySelector = true" severity="contrast" />
                    </div>

                    <Fieldset v-show="showPropertySelector" legend="Add Property">
                        <div class="flex">
                            <Dropdown
                                v-model="selectedProperties"
                                @change="updatePropsToShow"
                                :options="propsToSelect"
                                optionLabel="name"
                                optionValue="name"
                                class="grow"
                                placeholder="Select a property to add"
                                filter
                                :pt="{
                                    panel: {
                                        class: 'w-0'
                                    }
                                }"
                            >
                                <template #option="slotprops">
                                    <div class="font-semibold">
                                        {{ slotprops.option.name }}
                                    </div>
                                    <div class="text-gray-400 ml-3 ellipsis">
                                        {{ slotprops.option.description }}
                                    </div>
                                </template>
                            </Dropdown>
                        </div>
                    </Fieldset>
                </template>
                <!-- /Should have its own component -->
            </Card>
        </AccordionTab>
    </Accordion>

    <!--
    Should have it's own component
 -->
    <div v-else class="m-5">
        <div class="divide-y">
            <PropertyOneCol v-for="prop in propsToShow" :property="prop" class="[&:not(:first-child)]:mt-2 [&:not(:first-child)]:pt-5" />
        </div>
        <!-- Should have its own component -->
        <div v-show="!showPropertySelector && !!propsToSelect.length" class="flex justify-end">
            <Button label="Add Property" text size="small" icon="pi pi-plus" @click="showPropertySelector = true" />
        </div>

        <Fieldset v-show="showPropertySelector" legend="Add Property">
            <div class="flex">
                <Dropdown
                    v-model="selectedProperties"
                    @change="updatePropsToShow"
                    :options="propsToSelect"
                    optionLabel="name"
                    optionValue="name"
                    class="grow"
                    placeholder="Select a property to add"
                    filter
                    :pt="{
                        panel: {
                            class: 'w-0'
                        }
                    }"
                >
                    <template #option="slotprops">
                        <div class="font-semibold">
                            {{ slotprops.option.name }}
                        </div>
                        <div class="text-gray-400 ml-3 ellipsis">
                            {{ slotprops.option.description }}
                        </div>
                    </template>
                </Dropdown>
            </div>
        </Fieldset>
    </div>
</template>
