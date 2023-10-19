<script setup lang="ts">
import { ref } from "vue";
import { PropertyCategory } from "./PropertySet";
import StringForm from "@/ui/propeditor/propForms/StringForm.vue";
import NumberForm from "@/ui/propeditor/propForms/NumberForm.vue";

const props = defineProps(["category"]);

const forms = {
  string: StringForm,
  number: NumberForm,
};
</script>

<template>
  <div>
    <div class="text-2xl ma-2">
      {{ props.category.name }}
    </div>
    <component
      :is="forms[prop.type]"
      v-for="prop in props.category.properties"
      class="my-5 mx-2"
      :property="prop"
    />
  </div>
</template>
