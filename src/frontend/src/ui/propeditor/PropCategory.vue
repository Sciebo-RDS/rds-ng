<script setup lang="ts">
import { ref, computed, watch } from "vue";
import Button from "primevue/button";

import Dropdown from "primevue/dropdown";
import Fieldset from "primevue/fieldset";

import { Property as PropertyType } from "./PropertySet";
import Property from "@/ui/propeditor/Property.vue";

const props = defineProps(["category"]);
const showPropertySelector = ref(false);
var selectedProperties = ref<PropertyType>();

var propsToShow = ref<PropertyType[]>(
  props.category.properties.filter((p: PropertyType) => p.required)
);

var propsToSelect = ref(
  props.category.properties.filter((p: PropertyType) => !p.required)
);

watch(selectedProperties, (newSP) => {
  propsToShow.value = [
    ...propsToShow.value,
    props.category.properties.filter(
      (p: PropertyType) => p.name === newSP
    )[0] as PropertyType,
  ];
  propsToSelect.value = propsToSelect.value.filter(
    (p: PropertyType) => !propsToShow.value.includes(p)
  );
  showPropertySelector.value = false;
});
</script>

<template>
  <div>
    <div class="text-2xl ma-2">
      {{ props.category.name }}
    </div>
    <Property v-for="prop in propsToShow" class="my-10 mx-2" :property="prop" />

    <!-- Should have its own component -->
    <div v-show="!showPropertySelector" class="flex justify-end">
      <Button
        label="Add Property"
        text
        size="small"
        icon="pi pi-plus"
        @click="showPropertySelector = true"
        :disabled="!propsToSelect.length"
      />
    </div>

    <Fieldset v-show="showPropertySelector" legend="Add Property">
      <div class="flex">
        <Dropdown
          v-model="selectedProperties"
          :options="propsToSelect"
          optionLabel="name"
          optionValue="name"
          class="grow"
          placeholder="Select a property to add"
        />
      </div>
    </Fieldset>
    <!-- /Should have its own component -->
  </div>
</template>
