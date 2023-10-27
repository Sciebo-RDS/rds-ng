<script setup lang="ts">
import { ref } from "vue";
import StringForm from "@/ui/propeditor/propForms/StringForm.vue";
import NumberForm from "@/ui/propeditor/propForms/NumberForm.vue";
import TextAreaForm from "@/ui/propeditor/propForms/TextAreaForm.vue";
import MultiSelectForm from "@/ui/propeditor/propForms/MultiSelectForm.vue";

const props = defineProps(["property", "category_name", "controller"]);

const forms = {
    string: StringForm,
    number: NumberForm,
    textarea: TextAreaForm,
    multiselect: MultiSelectForm,
};
</script>

<template>
    <div class="grid grid-rows-1 grid-cols-4 gap-x-20">
        <div class="row-start-1 row-span-1">
            {{ props.property.name }}
            <div class="text-sm text-slate-600">
                {{ props.property.description }}
            </div>
        </div>
        <div class="row-span-1 col-span-3">
            <component
                :is="forms[property.type]"
                class="w-full"
                :property="property"
                :category_name="props.category_name"
                :controller="props.controller"
            />
        </div>
    </div>
</template>
