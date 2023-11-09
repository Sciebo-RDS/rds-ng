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
            <div @click="showDescription = !showDescription">
                <i
                    class="pi"
                    :class="{
                        'pi-angle-right': !showDescription,
                        'pi-angle-down': showDescription,
                    }"
                    style="font-size: 0.7rem; color: 'var(--secondary-color)'"
                />
                <span
                    v-show="!showDescription"
                    style="font-size: 0.7rem; color: 'var(--secondary-color)'"
                >
                    Description
                </span>
                <span
                    class="grid grid-rows-1 transition-all duration-300 ease-out"
                    :style="
                        showDescription
                            ? 'grid-template-rows: 1fr'
                            : 'grid-template-rows: 0fr'
                    "
                >
                    <span class="text-sm ml-2 text-neutral-700 overflow-hidden">
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
