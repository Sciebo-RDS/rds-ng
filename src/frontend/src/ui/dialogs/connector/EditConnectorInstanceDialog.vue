<script setup lang="ts">
import InputText from "primevue/inputtext";
import Panel from "primevue/panel";
import Textarea from "primevue/textarea";
import { string as ystring } from "yup";

import { useExtendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";
import { useDirectives } from "@common/ui/Directives";
import MandatoryMark from "@common/ui/components/MandatoryMark.vue";

const { dialogData, acceptDialog, useValidator } = useExtendedDialogTools();
const { vFocus } = useDirectives();

const validator = useValidator({
        name: ystring().trim().required().label("Name").default(dialogData.userData.name),
        description: ystring().label("Description").default(dialogData.userData.description)
    }
);
const name = validator.defineComponentBinds("name");
</script>

<template>
    <form @submit.prevent="acceptDialog" class="r-form">
        <Panel header="General" :pt="{ header: ' !p-3' }">
            <span class="r-form-field">
                <label>Name <MandatoryMark /></label>
                <InputText name="name" v-bind="name" v-model="dialogData.userData.name" placeholder="Name" :class="{ 'p-invalid': validator.errors.name }" v-focus />
                <small>The name of the connection.</small>
            </span>

            <span class="r-form-field">
                <label>Description</label>
                <Textarea name="description" v-model.trim="dialogData.userData.description" placeholder="Description" rows="3" />
                <small>An (optional) connection description.</small>
            </span>
        </Panel>
    </form>
</template>

<style scoped lang="scss">

</style>
