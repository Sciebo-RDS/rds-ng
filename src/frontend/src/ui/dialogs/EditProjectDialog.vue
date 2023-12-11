<script setup lang="ts">
import Checkbox from "primevue/checkbox";
import InputText from "primevue/inputtext";
import Panel from "primevue/panel";
import Textarea from "primevue/textarea";
import { string as ystring } from "yup";

import { FrontendComponent } from "@/component/FrontendComponent";
import { SnapInFlags } from "@/ui/snapins/SnapIn";

import { SnapInsCatalog } from "@/ui/snapins/SnapInsCatalog";
import { extendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";
import { useDirectives } from "@common/ui/Directives";

import MandatoryMark from "@common/ui/forms/MandatoryMark.vue";

const { dialogData, acceptDialog, useValidator } = extendedDialogTools();
const { vFocus } = useDirectives();

const comp = FrontendComponent.inject();
const optSnapIns = SnapInsCatalog.filter(SnapInFlags.Optional);

const validator = useValidator({
        title: ystring().required().label("Title").default(dialogData.userData.title),
        description: ystring().label("Description").default(dialogData.userData.description)
    }
);
const title = validator.defineComponentBinds("title");
</script>

<template>
    <form @submit.prevent="acceptDialog" class="r-form">
        <Panel header="General" :pt="{ header: ' !p-3' }">
            <span class="r-form-field">
                <label>Title <MandatoryMark /></label>
                <InputText name="title" v-bind="title" v-model="dialogData.userData.title" placeholder="Title" :class="{ 'p-invalid': validator.errors.title }" v-focus />
                <small>The title of the project.</small>
            </span>

            <span class="r-form-field">
                <label>Description</label>
                <Textarea name="description" v-model="dialogData.userData.description" placeholder="Description" rows="3" />
                <small>An (optional) project description.</small>
            </span>
        </Panel>

        <Panel header="Features" :pt="{ header: ' !p-3' }">
            <div v-for="snapIn of optSnapIns" :key="snapIn.snapInID" class="flex align-items-center pb-1">
                <Checkbox v-model="dialogData.userData.optionalSnapIns" :inputId="snapIn.snapInID" :value="snapIn.snapInID" />
                <label :for="snapIn.snapInID" class="pl-1.5">{{ snapIn.optionName }}</label>
            </div>
        </Panel>
    </form>
</template>

<style scoped lang="scss">
</style>
