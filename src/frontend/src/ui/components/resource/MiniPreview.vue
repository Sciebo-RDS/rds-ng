<script setup lang="ts">
import Skeleton from "primevue/skeleton";

const { loading, overlayIcon, hoverIcon } = defineProps(["loading", "overlayIcon", "hoverIcon"]);
</script>

<template>
    <div class="r-centered-grid content-center max-w-inherit grid group flex place-items-center">
        <Skeleton v-if="loading" title="Loading file..." class="!w-[calc(12rem-0.5rem)] !h-[calc(12rem-0.5rem)]"></Skeleton>
        <div v-if="!loading" class="col-start-1 row-start-1 transition duration-200 cursor-pointer">
            <slot name="preview" />
        </div>
        <div v-if="!loading && overlayIcon" class="w-full h-full grid place-items-center col-start-1 row-start-1 group-hover:hidden">
            <i class="pi" :class="overlayIcon" style="color: white"></i>
        </div>
        <div
            v-if="!loading && hoverIcon"
            class="w-full h-full grid place-items-center col-start-1 row-start-1 opacity-0 bg-black/50 group-hover:opacity-100 rounded transition duration-200"
            :class="!!overlayIcon ? 'transition-none' : ''"
        >
            <i class="pi" :class="hoverIcon" style="color: white"></i>
        </div>
    </div>
</template>
