<script setup lang="ts">
import { ref } from "vue";
import { propertyDataForms, type Property } from "./PropertyProfile";
import OverlayPanel from "primevue/overlaypanel";
import Chip from "primevue/chip";

const props = defineProps(["property"]);
const property = props.property as Property;

const op = ref();
const toggle = (event: Event) => {
    op.value.toggle(event);
};

let example: string;
/* const example = "<p class='mt-2'><b>Example</b>: this is an example<p>"; */
</script>

<template>
    <div class="lg:grid grid-rows-1 mt-5">
        <div class="row-start-1 row-span-1 text-gray-800 justify-between flex">
            <span :title="props.property.name">
                {{ props.property.name }}
                <i v-if="props.property.description" class="pi pi-question-circle mx-2" style="font-size: 1rem" @click="toggle"></i>
                <OverlayPanel ref="op" class="max-w-lg">
                    {{ props.property.description }}
                    <span v-if="example !== undefined" :v-html="example"></span>
                </OverlayPanel>
            </span>

            <Chip label="$RepoLabel" size="small" class="bg-[#ffdc83] h-4 !rounded px-2 py-3 text-sm bg-opacity-70" />
        </div>
        <div class="py-2">
            <span class="grid grid-rows-1">
                <span class="font-normal text-neutral-700"> </span>
            </span>
        </div>

        <div>
            <component :is="propertyDataForms[property.type]" class="w-full" :property="property" />
        </div>
    </div>
</template>
