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
                class="py-1 rounded-md cursor-pointer"
            >
                <span class="grid grid-rows-1">
                    <span
                        class="text-sm text-neutral-700 flex"
                        :class="showDescription ? '' : 'truncate'"
                    >
                        <span
                            class="material-icons-outlined"
                            style="font-size: 1.3rem"
                            >{{
                                showDescription
                                    ? "arrow_drop_down"
                                    : "arrow_right"
                            }}</span
                        >
                        <span class="m-w-0 text-ellipsis overflow-hidden">
                            {{ props.property.description }}
                        </span>
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
