<script setup lang="ts">
import { WebComponent } from "@common/component/WebComponent";

const comp = WebComponent.inject();

const appTitle = comp.data.title;
const appName = comp.data.name;
const appVersion = comp.data.version;
</script>

<template>
    <div class="grid grid-flow-row auto-rows-max justify-items-center">
        <div>
            <img src="@assets/img/rds_ng-octopus-blue.png" alt="RDS-NG Logo" class="logo mt-20">
        </div>
        <div>
            <h2 class="text-2xl font-extrabold text-slate-700">{{ appTitle }}</h2>
        </div>
        <div>
            <h3 class="text-1xl italic text-slate-700"><span class="font-bold">{{ appName }}</span> - <span class="text-slate-500">v{{ appVersion }}</span></h3>
        </div>
    </div>
</template>

<style scoped lang="scss">
.logo {
    width: 500px;
    height: auto;
}
</style>
