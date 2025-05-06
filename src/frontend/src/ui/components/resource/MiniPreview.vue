<script setup lang="ts">
import Skeleton from "primevue/skeleton";

const { loading, iconAlwaysVisible, icon, iconSize } = defineProps(["loading", "iconAlwaysVisible", "icon", "iconSize"]);
</script>

<template>
    <div class="r-centered-grid content-center max-w-inherit grid group place-items-center" :class="{ 'cursor-pointer': !loading }">
        <Skeleton v-if="loading" title="Loading file..." class="!w-[calc(12rem-0.5rem)] !h-[calc(12rem-0.5rem)]"></Skeleton>
        <div v-if="!loading" class="col-start-1 row-start-1 transition duration-200">
            <slot name="preview" />
        </div>
        <div
            v-if="!loading && icon"
            class="w-full h-full grid place-items-center col-start-1 row-start-1 group-hover:bg-black/[70%] transition duration-200 rounded"
        >
            <i
                class="pi"
                :class="[!iconAlwaysVisible ? 'group-[:not(:hover)]:hidden' : '', icon]"
                style="color: white"
                :style="{ 'font-size': +(iconSize || 1) + 'rem' }"
            ></i>
        </div>
    </div>
</template>
