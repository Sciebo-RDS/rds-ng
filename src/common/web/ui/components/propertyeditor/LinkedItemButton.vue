<script setup lang="ts">
import Button from "primevue/button";
import OverlayPanel from "primevue/overlaypanel";
import SplitButton from "primevue/splitbutton";
import { useDialog } from "primevue/usedialog";
import { computed, ref } from "vue";
import PropertyDialog from "./PropertyDialog.vue";
import { calculateClassColor } from "./utils/Colors";
import { injectTemplate } from "./utils/Templates";

const dialog = useDialog();
const props = defineProps(["linkedItemActions", "item", "projectObjects", "globalObjectStore", "profileId", "projectProfiles", "mode"]);

let object = props.projectObjects.get(props.item) || props.globalObjectStore.get(props.item);
var bgColor, borderColor, injectedLabel, objectClass;
if (object !== undefined) {
    var { bgColor, borderColor } = calculateClassColor(props.projectProfiles, props.profileId, object.type, 99, 10);
    var objectClass = props.projectProfiles.getClassById(props.profileId, object["type"]);
    injectedLabel = computed(() => injectTemplate(objectClass.labelTemplate, props.globalObjectStore.get(object.id)));
} else {
    bgColor = "#eee";
    borderColor = "#ee0000";
    injectedLabel = computed(() => `[${props.item.slice(0, 6)}]`);
}
const linkedItemActions = object
    ? props.linkedItemActions(object.id, injectedLabel)
    : [
          {
              label: "Remove all References to undefined Item",
              icon: "pi pi-trash",
              command: () => {
                  props.globalObjectStore.remove(props.item, props.item);
                  props.projectObjects.remove(props.item, props.item);
              }
          }
      ];
const emit = defineEmits(["loadObject"]);

function handleClick() {
    if (object["id"] === undefined) {
        return;
    }
    if (props.mode == "dialog") {
        emit("loadObject", object["id"]);
    } else {
        dialog.open(PropertyDialog, {
            props: {
                header: "Edit Property",
                style: {
                    width: "50vw",
                    height: "80vh"
                },
                breakpoints: {
                    "960px": "75vw",
                    "640px": "90vw"
                },
                modal: true
            },
            data: {
                id: object["id"],
                projectObjectStore: props.projectObjects,
                globalObjectStore: props.globalObjectStore,
                propertyProfileStore: props.projectProfiles,
                profileId: props.profileId
            }
        });
    }
}

const op = ref();
const toggle = (event: Event) => {
    op.value.toggle(event);
};
</script>

<template>
    <SplitButton
        v-if="object !== undefined"
        menuButtonIcon="pi pi-ellipsis-v"
        :model="linkedItemActions"
        menuitemicon="pi pi-link"
        @click="
            () => {
                object === undefined ? null : handleClick();
            }
        "
        :style="`--p-color: ${bgColor}; --p-border-color: ${borderColor};`"
    >
        <span class="text-lg mx-2 truncate"> {{ objectClass.label }}: {{ injectedLabel }} </span>
    </SplitButton>
    <Button
        v-else
        menuButtonIcon="pi pi-ellipsis-v"
        :model="linkedItemActions"
        menuitemicon="pi pi-link"
        :style="`background-color: ${bgColor}; border-color: ${borderColor}; height: 2rem`"
        class="text-gray-600"
        @click="toggle"
    >
        <i class="pi pi-exclamation-circle mx-1" style="color: #ee0000" />
        <span class="text-lg mx-2 truncate"> {{ "broken link" }}: {{ injectedLabel }} </span>
    </Button>

    <OverlayPanel ref="op" class="border-red-400">
        <div class="m-2 gap-3 w-25rem">
            <div>
                <span class="font-medium text-900 block mb-2">The referenced object is missing.</span>
            </div>
            <div>Do you want to remove all references to the missing object?</div>
            <div class="min-w-full flex justify-end mt-5 space-x-2">
                <Button text class="min-w-fit" size="small" @click="toggle"> cancel </Button>
                <Button
                    class="min-w-fit"
                    size="small"
                    severity="danger"
                    icon="pi pi-trash"
                    @click="
                        () => {
                            props.globalObjectStore.remove(props.item, props.item);
                            props.projectObjects.remove(props.item, props.item);
                        }
                    "
                >
                    Remove
                </Button>
            </div>
        </div>
    </OverlayPanel>
</template>

<style scoped lang="scss">
.p-splitbutton {
    @apply h-8 text-gray-600 border border-[var(--p-border-color)];
}
:deep(.p-splitbutton-defaultbutton) {
    @apply bg-[var(--p-color)] bg-opacity-30 border-0 px-2 text-inherit;
}

:deep(.p-splitbutton-menubutton) {
    @apply bg-[var(--p-color)] bg-opacity-50 border-0 border-l border-[var(--p-border-color)] text-inherit;
}
</style>
