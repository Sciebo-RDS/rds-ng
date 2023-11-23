<script setup lang="ts">
import { ref } from "vue";

import { propertyDataForms } from "@/ui/propeditor/PropertyProfile";

const props = defineProps(["property"]);

const showDescription = ref(false);

let overflows = ref(false);

const vTestOverflow = {
    mounted: (el) => {
        if (el.offsetWidth < el.scrollWidth) {
            overflows.value = true;
        }
    },
};
</script>

<template>
    <div class="lg:grid grid-rows-1 xl:grid-cols-4 gap-10 my-5">
        <div class="row-start-1 row-span-1 xl:col-span-2 2xl:col-span-1">
            {{ props.property.name }}
            <div
                @click="overflows ? (showDescription = !showDescription) : null"
                class="py-1 cursor-default"
            >
                <span class="grid grid-rows-1">
                    <span
                        class="text-sm text-neutral-700 flex overflow-clip"
                        :class="showDescription ? '' : 'truncate'"
                        v-testOverflow
                    >
                        <span
                            class="material-icons-outlined ff-alignment-fix"
                            style="font-size: 1.3rem"
                            :style="overflows ? '' : 'opacity: 0'"
                            >{{
                                showDescription
                                    ? "arrow_drop_down"
                                    : "arrow_right"
                            }}</span
                        >
                        <span
                            class="text-ellipsis"
                            :class="{
                                'overflow-hidden':
                                    overflows && !showDescription,
                                'cursor-pointer': overflows,
                                'cursor-text': !overflows,
                            }"
                        >
                            {{ props.property.description }}
                        </span>
                    </span>
                </span>
            </div>
        </div>
        <div class="row-span-1 xl:col-span-2 2xl:col-span-3 col-span-2">
            <component
                :is="propertyDataForms[property.type]"
                class="w-full"
                :property="property"
            />
        </div>
    </div>
</template>

<style scoped>
/* fixes icon alignment in Firefox */
@-moz-document url-prefix() {
    .ff-alignment-fix {
        line-height: 1rem;
    }
}
</style>
