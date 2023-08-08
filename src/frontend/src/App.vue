<script setup lang="ts">
import Button from "primevue/button"
import { useCommon } from "@common/common";

const { app, } = useCommon();
</script>

<template>
    <header>
        <img alt="Vue logo" class="logo" src="@assets/img/rds-octopus-bl.svg" width="250" height="250"/>
    </header>
    <Button label="Submit" class="bg-red-500 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded" unstyled/>
    <h1 class="text-3xl font-bold underline bg-amber-200">
        Hello world!
    </h1>
</template>
