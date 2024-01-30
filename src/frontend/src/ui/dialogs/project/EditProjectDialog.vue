<script setup lang="ts">
import Checkbox from "primevue/checkbox";
import InputText from "primevue/inputtext";
import Panel from "primevue/panel";
import RadioButton from "primevue/radiobutton";
import Textarea from "primevue/textarea";
import { onMounted, ref, watch } from "vue";
import { string as ystring, array as yarray } from "yup";

import { ListResourcesReply } from "@common/api/resource/ResourceCommands";
import { type ConnectorInstanceID } from "@common/data/entities/connector/ConnectorInstance";
import { findConnectorInstanceByID } from "@common/data/entities/connector/ConnectorUtils";
import { resourcesListToTreeNodes } from "@common/data/entities/resource/ResourceUtils";
import { useExtendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";
import { useDirectives } from "@common/ui/Directives";

import MandatoryMark from "@common/ui/components/MandatoryMark.vue";
import ResourcesTreeSelect from "@common/ui/components/ResourcesTreeSelect.vue";
import ConnectorInstancesSelect from "@/ui/dialogs/project/ConnectorInstancesSelect.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { type UIOptions } from "@/data/entities/UIOptions";
import { useUserStore } from "@/data/stores/UserStore";
import { ListResourcesAction } from "@/ui/actions/resource/ListResourcesAction";
import { SnapInsCatalog } from "@/ui/snapins/SnapInsCatalog";

const { dialogData, acceptDialog, useValidator } = useExtendedDialogTools();
const { vFocus } = useDirectives();

const comp = FrontendComponent.inject();
const userStore = useUserStore();
const optSnapIns = SnapInsCatalog.allOptionals();
const uiOptions = ref<UIOptions>(dialogData.userData.options.ui);
const showDataPathSelector = dialogData.options["showDataPathSelector"];

const validator = useValidator({
        title: ystring().required().label("Title").default(dialogData.userData.title),
        description: ystring().label("Description").default(dialogData.userData.description),
        datapath: ystring().required().label("Data path").default(dialogData.userData.datapath),
        activeInstances: yarray().label("Active connections").default(dialogData.userData.options.active_connector_instances).test(
            "active-instances",
            "Select at least one connection to use",
            (value: ConnectorInstanceID[]) => {
                return dialogData.userData.options.use_all_connector_instances ||
                    (Array.isArray(value) && value.filter((instance) => !!findConnectorInstanceByID(userStore.userSettings.connector_instances, instance)).length > 0);
            }
        )
    }
);
const title = validator.defineComponentBinds("title");
const datapath = validator.defineComponentBinds("datapath");
const activeInstances = validator.defineComponentBinds("activeInstances");

const resourcesNodes = ref<Object[]>([]);
onMounted(() => {
    if (showDataPathSelector) {
        const action = new ListResourcesAction(comp, true);
        action.prepare("", true, false).done((reply: ListResourcesReply, success, msg) => {
            if (success) {
                resourcesNodes.value = resourcesListToTreeNodes(reply.resources);
            }
        });
        action.execute();
    }
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
        <Panel header="General" :pt="{ header: '!p-3' }">
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

        <Panel header="Data" :pt="{ header: '!p-3' }">
            <span class="r-form-field">
                <label>Data path <MandatoryMark /></label>
                <span v-if="showDataPathSelector" class="grid grid-flow-row">
                    <ResourcesTreeSelect
                        v-bind="datapath"
                        v-model="dialogData.userData.datapath"
                        :options="resourcesNodes"
                        placeholder="Select where the data of this project is stored"
                        loading
                        :class="{ 'p-invalid': validator.errors.datapath }"
                    />
                    <small><b>Important:</b> This path cannot be changed after the project has been created!</small>
                </span>
                <span v-else class="grid grid-flow-row">
                    <span class="flex border border-solid rounded p-2">
                        <span class="material-icons-outlined mi-folder opacity-75 pr-2" />
                        <span>{{ dialogData.userData.datapath }}</span>
                    </span>
                    <small><b>Note:</b> This path cannot be changed anymore after project creation.</small>
                </span>
            </span>
        </Panel>

        <Panel header="Features" :pt="{ header: '!p-3' }">
            <div v-for="snapIn of optSnapIns" :key="snapIn.snapInID" class="flex align-items-center pb-1">
                <Checkbox v-model="uiOptions.optional_snapins" :inputId="snapIn.snapInID" :value="snapIn.snapInID" />
                <label :for="snapIn.snapInID" class="pl-1.5">{{ snapIn.options.optional!.label }}</label>
            </div>
        </Panel>

        <Panel header="Connections" :pt="{ header: '!p-3' }">
            <div class="r-form-field">
                <div class="grid grid-flow-row">
                    <div>
                        <RadioButton v-model="dialogData.userData.options.use_all_connector_instances" inputId="useAllConnectorInstances" :value="true" @change="validator.validate()" />
                        <label for="useAllConnectorInstances">Use all available connections</label>
                    </div>

                    <div>
                        <RadioButton v-model="dialogData.userData.options.use_all_connector_instances" inputId="useSelectConnectorInstances" :value="false" @change="validator.validate()" />
                        <label for="useSelectConnectorInstances">Use only the following connections:</label>
                    </div>

                    <div class="border border-solid rounded p-2 ml-2 mr-2 mt-1" :class="{ 'r-border-error': validator.errors.activeInstances }">
                        <ConnectorInstancesSelect
                            v-bind="activeInstances"
                            v-model="dialogData.userData.options.active_connector_instances"
                            :disabled="dialogData.userData.options.use_all_connector_instances"
                            class="w-full h-44"
                        />
                    </div>
                </div>
            </div>
        </Panel>
    </form>
</template>

<style scoped lang="scss">

</style>
