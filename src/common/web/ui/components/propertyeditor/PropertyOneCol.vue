<script setup lang="ts">
import { propertyDataForms } from "./PropertyProfile";

const props = defineProps(["property"]);
</script>

<template>
    <div class="lg:grid grid-rows-1 mt-5">
        <div class="row-start-1 row-span-1 font-semibold">
            {{ props.property.name }}
            <div class="py-1">
                <span class="grid grid-rows-1">
                    <span class="font-normal text-neutral-700">
                        {{ props.property.description }}
                    </span>
                </span>
            </div>
        </div>

        <div>
            <component :is="propertyDataForms[property.type]" class="w-full" :property="property" />
        </div>
    </div>
</template>
