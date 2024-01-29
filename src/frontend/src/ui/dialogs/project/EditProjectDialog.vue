<script setup lang="ts">
import Checkbox from "primevue/checkbox";
import InputText from "primevue/inputtext";
import Panel from "primevue/panel";
import Textarea from "primevue/textarea";
import { TreeNode } from "primevue/treenode";
import TreeSelect from "primevue/treeselect";
import { onMounted, ref, watch } from "vue";
import { string as ystring, object as yobject } from "yup";

import { ListResourcesReply } from "@common/api/resource/ResourceCommands";
import { type Resource } from "@common/data/entities/resource/Resource";
import { resourcesListToTreeNodes } from "@common/data/entities/resource/ResourceUtils";
import { useExtendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";
import { useDirectives } from "@common/ui/Directives";
import MandatoryMark from "@common/ui/components/MandatoryMark.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { type UIOptions } from "@/data/entities/UIOptions";
import { ListResourcesAction } from "@/ui/actions/resource/ListResourcesAction";
import { SnapInsCatalog } from "@/ui/snapins/SnapInsCatalog";

const { dialogData, acceptDialog, useValidator } = useExtendedDialogTools();
const { vFocus } = useDirectives();

const comp = FrontendComponent.inject();
const optSnapIns = SnapInsCatalog.allOptionals();
const uiOptions = ref<UIOptions>(dialogData.userData.options.ui);

const validator = useValidator({
        title: ystring().required().label("Title").default(dialogData.userData.title),
        description: ystring().label("Description").default(dialogData.userData.description),
        datapath: yobject().required().label("Data path").test("datapath-test", "Data path is a required field", (value, ctx) => {
            return Object.entries(value).length > 0;
        })
    }
);
const title = validator.defineComponentBinds("title");
const datapath = validator.defineComponentBinds("datapath");

const resourcesNodes = ref<TreeNode[] | null>();
const selectedResource = ref<Resource>();
onMounted(() => {
    const action = new ListResourcesAction(comp, true);
    action.prepare("", true, false, true).done((reply: ListResourcesReply, success, msg) => {
        if (success) {
            resourcesNodes.value = resourcesListToTreeNodes(reply.resources);
        }
    });
    action.execute();
});

watch(selectedResource, (newResource) => {
    const data = Object.keys(newResource);
    dialogData.userData.datapath = data.length > 0 ? data[0] : "";
});

// Reflect selected features based on snap-ins with associated project features
watch(() => uiOptions.value.optional_snapins, (snapIns) => {
    dialogData.userData.options.optional_features = SnapInsCatalog.filter(
        (snapIn) => snapIns.includes(snapIn.snapInID) && !!snapIn.options.optional?.feature
    ).map(
        (snapIn) => snapIn.options.optional!.feature
    );
});
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

        <Panel header="Data" :pt="{ header: ' !p-3' }">
            <span class="r-form-field">
                <label>Data path <MandatoryMark /></label>
                <!-- TODO: Separate component -->
                <TreeSelect
                    v-bind="datapath"
                    v-model="selectedResource"
                    :options="resourcesNodes"
                    selection-mode="single"
                    placeholder="Select where the data of this project is stored"
                    :class="{ 'p-invalid': validator.errors.datapath }"
                    :pt="{
                        panel: 'r-z-index-toplevel'
                    }"
                >
                    <template #value="value">
                        <div v-if="value.value.length > 0" class="flex gap-2"><span class="material-icons-outlined mi-folder opacity-75" /> {{ value.value[0].data }}</div>
                        <div v-else>{{ value.placeholder }}</div>
                    </template>
                </TreeSelect>
                <small><b>Important:</b> This path cannot be changed after the project has been created!</small>
            </span>
        </Panel>

        <Panel header="Features" :pt="{ header: ' !p-3' }">
            <div v-for="snapIn of optSnapIns" :key="snapIn.snapInID" class="flex align-items-center pb-1">
                <Checkbox v-model="uiOptions.optional_snapins" :inputId="snapIn.snapInID" :value="snapIn.snapInID" />
                <label :for="snapIn.snapInID" class="pl-1.5">{{ snapIn.options.optional!.label }}</label>
            </div>
        </Panel>
    </form>
</template>

<style scoped lang="scss">

</style>
