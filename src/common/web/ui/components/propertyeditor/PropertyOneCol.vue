<script setup lang="ts">
import { propertyDataForms, type Property } from "./PropertyProfile";

const props = defineProps(["property"]);
const property = props.property as Property;
</script>

<template>
    <div class="lg:grid grid-rows-1 mt-5">
        <div class="row-start-1 row-span-1 font-semibold text-ellipsis truncate" :title="props.property.name">
            {{ props.property.name }}
        </div>
        <div class="py-2">
            <span class="grid grid-rows-1">
                <span class="font-normal text-neutral-700">
                    {{ props.property.description }}
                </span>
            </span>
        </div>

        <div>
            <component :is="propertyDataForms[property.type]" class="w-full" :property="property" />
        </div>
    </div>
</template>
