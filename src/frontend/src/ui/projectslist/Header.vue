<script setup lang="ts">
import Button from "primevue/button";
</script>

<template>
    <div class="grid grid-rows-2 grid-cols-[min-content_1fr_min-content] grid-flow-col gap-x-2 content-center items-center r-primary-bg r-primary-text">
        <div class="row-span-2">
            <a href="https://www.research-data-services.org" target="_blank">
                <img id="logo" src="@assets/img/rds-octopus-wh.svg" alt="RDS Logo" class="p-1.5" title="Visit the RDS website">
            </a>
        </div>
        <div class="font-bold pt-3">
            Donald T. Rump
        </div>
        <div class="italic pb-3">
            3 Projects
        </div>
        <div class="row-span-2 pr-2">
            <Button plain rounded aria-label="Settings" title="Settings">
                <template #icon>
                    <span class="material-icons-outlined mi-settings r-primary-text" style="font-size: 40px;"/>
                </template>
            </Button>
        </div>
    </div>
</template>

<style scoped lang="scss">
#logo {
    min-width: 5rem;
}
</style>
