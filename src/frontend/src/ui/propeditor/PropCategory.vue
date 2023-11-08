<script setup lang="ts">
import { ref, provide, inject } from "vue";
import Button from "primevue/button";

import Dropdown from "primevue/dropdown";
import Fieldset from "primevue/fieldset";

import { Property as PropertyType } from "./PropertyProfile";
import Property from "@/ui/propeditor/Property.vue";

const props = defineProps(["category"]);

const controller = inject("controller");

provide("categoryId", props.category.id);

const showPropertySelector = ref(false);
var selectedProperties = ref<PropertyType>();

var propsToShow = ref<PropertyType[]>(
    props.category.properties.filter(
        (p: PropertyType) =>
            controller.getValue(props.category.id, p.id) != undefined ||
            p.showAlways
    )
);

var propsToSelect = ref(
    props.category.properties.filter(
        (p: PropertyType) => !propsToShow.value.includes(p)
    )
);

function updatePropsToShow(e: Event) {
    propsToShow.value = [
        ...propsToShow.value,
        props.category.properties.filter(
            (p: PropertyType) => p.name === e.value
        )[0] as PropertyType,
    ];
    propsToSelect.value = propsToSelect.value.filter(
        (p: PropertyType) => !propsToShow.value.includes(p)
    );
    showPropertySelector.value = false;
}
</script>

<template>
    <div>
        <div class="text-2xl">
            {{ props.category.name }}
        </div>
        <div class="text-slate-600 mt-3 mb-5">
            {{ props.category.description }}
        </div>
        <Property
            v-for="prop in propsToShow"
            class="my-10 mx-2"
            :property="prop"
        />

        <!-- Should have its own component -->
        <div v-show="!showPropertySelector" class="flex justify-end">
            <Button
                label="Add Property"
                text
                size="small"
                icon="pi pi-plus"
                @click="showPropertySelector = true"
                :disabled="!propsToSelect.length"
            />
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
                    :pt="{
                        panel: {
                            class: 'w-0',
                        } /* HACK This fixes overflow, there is probably a better way*/,
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
        <!-- /Should have its own component -->
    </div>
</template>
