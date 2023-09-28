<script setup lang="ts">
import { WebComponent } from "../../../../component/WebComponent";

const comp = WebComponent.injectComponent();

const appTitle = comp.data.title;
const appName = comp.data.name;
const appVersion = comp.data.version;
</script>

<template>
    <div>
        <img src="../../../../../assets/img/rds_ng-octopus-blue.png" alt="RDS-NG Logo" class="logo">
    </div>
    <div>
        <h2 class="text-2xl font-extrabold">{{ appTitle }}</h2>
    </div>
    <div>
        <h3 class="text-1xl italic"><span class="font-bold">{{ appName }}</span> - <span class="r-text-light">v{{ appVersion }}</span></h3>
    </div>
    <div>&nbsp;</div>
</template>

<style scoped lang="scss">
.logo {
    width: 500px;
    height: auto;
}
</style>
