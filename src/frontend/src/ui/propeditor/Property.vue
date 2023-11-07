<script setup lang="ts">
import { propertyDataForms } from "@/ui/propeditor/PropertyProfile";

const props = defineProps(["property"]);
</script>

<template>
    <div class="grid grid-rows-1 grid-cols-4 gap-x-20">
        <div class="row-start-1 row-span-1">
            {{ props.property.name }}
            <div class="text-sm text-slate-600">
                {{ props.property.description }}
            </div>
        </div>
        <div class="row-span-1 col-span-3">
            <component
                :is="propertyDataForms[property.type]"
                class="w-full"
                :property="property"
            />
        </div>
    </div>
</template>
