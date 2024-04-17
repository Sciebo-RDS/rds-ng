<script setup lang="ts">
import { ref } from "vue";

import Breadcrumb from "primevue/breadcrumb";

let path = ["propery", "sub property", "sub sub property"];
let menuPath = ref();
updatePath(path.length - 1);

function updatePath(i: number) {
    path = path.slice(0, i + 1);
    menuPath.value = path.map((obj, i) => {
        return {
            label: obj,
            command: () => {
                updatePath(i);
            }
        };
    });
}
</script>

<template>
    <div>
        <Breadcrumb :model="menuPath" :pt="{ root: { class: '' }, label: { class: 'text-red-900 opacity-80 hover:opacity-100 capitalize' } }" />
    </div>
</template>
