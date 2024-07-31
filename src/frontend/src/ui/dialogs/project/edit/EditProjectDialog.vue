<script setup lang="ts">
import Checkbox from "primevue/checkbox";
import Fieldset from "primevue/fieldset";
import InputSwitch from "primevue/inputswitch";
import InputText from "primevue/inputtext";
import Stepper from "primevue/stepper";
import StepperPanel from "primevue/stepperpanel";
import Textarea from "primevue/textarea";
import { computed, onMounted, ref, unref, watch } from "vue";
import { string as ystring } from "yup";

import { ListResourcesReply } from "@common/api/resource/ResourceCommands";
import { resourcesListToTreeNodes } from "@common/data/entities/resource/ResourceUtils";
import { useExtendedDialogTools } from "@common/ui/dialogs/ExtendedDialogTools";
import { useDirectives } from "@common/ui/Directives";

import MandatoryMark from "@common/ui/components/misc/MandatoryMark.vue";
import ResourcesTreeSelect from "@common/ui/components/resource/ResourcesTreeSelect.vue";
import StepperIconHeader from "@common/ui/components/stepper/StepperIconHeader.vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { type UIOptions } from "@/data/entities/ui/UIOptions";
import { ListResourcesAction } from "@/ui/actions/resource/ListResourcesAction";
import { SnapInsCatalog } from "@/ui/snapins/SnapInsCatalog";

import ConnectorInstancesSelect from "@/ui/dialogs/project/edit/ConnectorInstancesSelect.vue";
import EditProjectDialogFooter from "@/ui/dialogs/project/edit/EditProjectDialogFooter.vue";

const { dialogData, acceptDialog, useValidator } = useExtendedDialogTools();
const { vFocus } = useDirectives();

const comp = FrontendComponent.inject();
const optSnapIns = SnapInsCatalog.allOptionals();
const uiOptions = ref<UIOptions>(dialogData.userData.options.ui);
const showDataPathSelector = dialogData.options["showDataPathSelector"];
const newProject = dialogData.userData.newProject;

const stepIndices = {
    main: 0,
    features: 1,
    connections: 2
};
const lastStepIndex = Object.entries(stepIndices).length - 1;
const activeStep = ref(0);

const validator = useValidator({
    title: ystring().trim().required().label("Title").default(dialogData.userData.title),
    description: ystring().label("Description").default(dialogData.userData.description),
    datapath: ystring().trim().required().label("Data path").default(dialogData.userData.datapath)
});
const title = validator.defineComponentBinds("title");
const datapath = validator.defineComponentBinds("datapath");

const resourcesNodes = ref<Object[]>([]);
const resourcesError = ref("");
onMounted(() => {
    if (showDataPathSelector) {
        const action = new ListResourcesAction(comp, true);
        action
            .prepare("", true, false)
            .done((reply: ListResourcesReply, success, msg) => {
                if (success) {
                    resourcesNodes.value = resourcesListToTreeNodes(reply.resources, true);
                }
            })
            .failed((_, msg) => {
                resourcesError.value = "Unable to load resources";
            });
        action.execute();
    }
});

// Reflect selected features based on snap-ins with associated project features
watch(
    () => uiOptions.value.optional_snapins,
    (snapIns) => {
        dialogData.userData.options.optional_features = SnapInsCatalog.filter(
            (snapIn) => snapIns.includes(snapIn.snapInID) && !!snapIn.options.optional?.feature
        ).map((snapIn) => snapIn.options.optional!.feature);
    }
);

const prevCallback = computed(() => {
    if (unref(activeStep) == stepIndices.main) {
        return undefined;
    } else {
        return onPrevStep;
    }
});
const nextCallback = computed(() => {
    if (unref(activeStep) >= lastStepIndex) {
        return acceptDialog;
    } else {
        validator.validate();

        // Verify each step to prevent advancing to the next one
        if (unref(activeStep) == stepIndices.main) {
            if ("title" in validator.errors || "datapath" in validator.errors) {
                return undefined;
            }
        }

        return onNextStep;
    }
});
const nextName = computed(() => {
    if (unref(activeStep) >= lastStepIndex) {
        return newProject ? "Create" : "Save";
    } else {
        return undefined;
    }
});

function onClickStep(event: Event, callback: (event: Event) => void) {
    validator.validate();
    callback(event);
}

function onPrevStep() {
    validator.validate();
    activeStep.value -= 1;
}

function onNextStep() {
    validator.validate();
    activeStep.value += 1;
}
</script>

<template>
    <form @submit.prevent="!newProject ? acceptDialog : undefined" :class="[{ 'h-[calc(100%-4rem)]': newProject }, 'r-form']">
        <Stepper v-model:activeStep="activeStep" :linear="newProject" :pt="{ panelContainer: newProject ? 'h-full' : '' }">
            <StepperPanel header="Main settings" :pt="{ root: 'h-full', separator: !newProject ? 'r-border-bg' : '' }">
                <template #header="{ index, clickCallback }">
                    <StepperIconHeader
                        :active="newProject ? index <= activeStep : index == activeStep"
                        :click-callback="(event: Event) => onClickStep(event, clickCallback)"
                        icon="mi-edit"
                    />
                </template>

                <template #content>
                    <div class="mb-2">
                        Set your main project settings, like its title, here. Note that the data path cannot be changed once the project has been created.
                    </div>

                    <Fieldset legend="General">
                        <span class="r-form-field">
                            <label>Title <MandatoryMark /></label>
                            <InputText
                                name="title"
                                v-bind="title"
                                v-model="dialogData.userData.title"
                                placeholder="Title"
                                :class="{ 'p-invalid': validator.errors.title }"
                                v-focus
                            />
                            <small>The title of the project.</small>
                        </span>

                        <span class="r-form-field mt-5">
                            <label>Description</label>
                            <Textarea name="description" v-model="dialogData.userData.description" placeholder="Description" rows="3" />
                            <small>An (optional) project description.</small>
                        </span>
                    </Fieldset>

                    <Fieldset legend="Data" class="h-fit">
                        <span class="r-form-field">
                            <label>Data path <MandatoryMark /></label>
                            <span v-if="showDataPathSelector" class="grid grid-flow-row">
                                <ResourcesTreeSelect
                                    v-bind="datapath"
                                    v-model="dialogData.userData.datapath"
                                    :options="resourcesNodes"
                                    :loading-error="resourcesError"
                                    placeholder="Select where the data of this project is stored"
                                    loading
                                    :class="{ 'p-invalid': validator.errors.datapath }"
                                />
                                <small class="pt-1"><b>Important:</b> This path cannot be changed after the project has been created!</small>
                            </span>
                            <span v-else class="grid grid-flow-row">
                                <span class="flex border border-solid rounded p-2">
                                    <span class="material-icons-outlined mi-folder opacity-75 pr-2" />
                                    <span>{{ dialogData.userData.datapath }}</span>
                                </span>
                                <small class="pt-1"><b>Note:</b> This path cannot be changed anymore after project creation.</small>
                            </span>
                        </span>
                    </Fieldset>
                </template>
            </StepperPanel>

            <StepperPanel header="Features" :pt="{ root: 'h-full', separator: !newProject ? 'r-border-bg' : '' }">
                <template #header="{ index, clickCallback }">
                    <StepperIconHeader
                        :active="newProject ? index <= activeStep : index == activeStep"
                        :click-callback="(event: Event) => onClickStep(event, clickCallback)"
                        icon="mi-checklist"
                    />
                </template>

                <template #content>
                    <div class="mb-2">
                        Select the features you want to use in this project. You can always turn additional features on or existing ones off later.
                    </div>

                    <Fieldset legend="Features">
                        <div v-for="snapIn of optSnapIns" :key="snapIn.snapInID" class="flex align-items-center pb-1">
                            <Checkbox v-model="uiOptions.optional_snapins" :inputId="snapIn.snapInID" :value="snapIn.snapInID" class="self-center" />
                            <label :for="snapIn.snapInID" class="pl-1.5">{{ snapIn.options.optional!.label }}</label>
                        </div>
                    </Fieldset>
                </template>
            </StepperPanel>

            <StepperPanel header="Connections" :pt="{ root: 'h-full', separator: !newProject ? 'r-border-bg' : '' }">
                <template #header="{ index, clickCallback }">
                    <StepperIconHeader
                        :active="newProject ? index <= activeStep : index == activeStep"
                        :click-callback="(event: Event) => onClickStep(event, clickCallback)"
                        icon="mi-hub"
                    />
                </template>

                <template #content>
                    <div class="mb-2">
                        Here you can select which connections - all or only specific ones - to make available for publishing or exporting your project. You can
                        always change this selection later.
                    </div>

                    <Fieldset legend="Connections">
                        <div class="r-form-field">
                            <div class="grid grid-flow-row">
                                <div class="flex align-items-center">
                                    <InputSwitch
                                        v-model="dialogData.userData.options.use_all_connector_instances"
                                        inputId="useSelectConnectorInstances"
                                        :true-value="false"
                                        :false-value="true"
                                        @change="validator.validate()"
                                        class="self-center"
                                    />
                                    <label for="useSelectConnectorInstances" class="pl-1.5">Use only the following connections:</label>
                                </div>

                                <div class="!h-full border border-solid rounded p-1 ml-3.5 mr-3.5 mt-1.5">
                                    <ConnectorInstancesSelect
                                        v-model="dialogData.userData.options.active_connector_instances"
                                        :disabled="dialogData.userData.options.use_all_connector_instances"
                                        class="w-full h-full"
                                    />
                                </div>
                            </div>
                        </div>
                    </Fieldset>
                </template>
            </StepperPanel>
        </Stepper>
    </form>

    <EditProjectDialogFooter
        v-if="newProject"
        :prev-callback="prevCallback"
        :next-callback="nextCallback"
        :next-name="nextName"
        :next-icon="activeStep >= lastStepIndex ? 'mi-done' : undefined"
        :next-icon-position="activeStep >= lastStepIndex ? 'left' : undefined"
        class="mt-auto"
    />
</template>

<style scoped lang="scss">
.fixed-border-color {
    background-color: var(--r-border-color);
}
</style>
