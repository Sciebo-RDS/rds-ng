<script setup lang="ts">
import { WebComponent } from "../../../../component/WebComponent";

const comp = WebComponent.injectComponent();

const appTitle = comp.data.title;
const appName = comp.data.name;
const appVersion = comp.data.version;
</script>

<template>
    <div>
        <img src="../../../../../assets/img/rds_ng-octopus-blue.png" alt="Logo" class="logo" />
    </div>
    <div>
        <h2 class="text-2xl font-extrabold">
            {{ appTitle }} <span class="r-text-light text-lg font-bold">v{{ appVersion }}</span>
        </h2>
    </div>
    <div>&nbsp;</div>
</template>

<style scoped lang="scss">
.logo {
    width: 400px;
    height: auto;
}
</style>
