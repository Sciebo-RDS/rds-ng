<script setup lang="ts">
import { defineProps, ref } from "vue";

import { propertyDataForms } from "@/ui/propeditor/PropertyProfile";

const props = defineProps(["property"]);

const showDescription = ref(false);
</script>

<template>
    <div class="grid grid-rows-1 grid-cols-4 gap-x-10">
        <div class="row-start-1 row-span-1">
            {{ props.property.name }}
            <div
                @click="showDescription = !showDescription"
                class="p-1 rounded-md cursor-pointer"
                :class="!showDescription ? 'hover:bg-sky-50' : ''"
                style="
                    transition: background-color 0.2s, color 0.2s,
                        border-color 0.2s, box-shadow 0.2s;
                "
            >
                <span
                    class="grid grid-rows-1 transition-all duration-500 ease-out"
                >
                    <span
                        class="text-sm text-neutral-700"
                        :class="
                            showDescription
                                ? 'whitespace-normal'
                                : 'whitespace-nowrap truncate'
                        "
                    >
                        {{ props.property.description }}
                    </span>
                </span>
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
