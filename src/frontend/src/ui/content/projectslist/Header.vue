<script setup lang="ts">
import { storeToRefs } from "pinia";
import Button from "primevue/button";
import { unref } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { useUserStore } from "@/data/stores/UserStore";
import { EditUserSettingsAction } from "@/ui/actions/user/EditUserSettingsAction";

const comp = FrontendComponent.inject();
const userStore = useUserStore();
const { userSettings } = storeToRefs(userStore);

function showUserSettings() {
    const action = new EditUserSettingsAction(comp);
    action.showUserSettingsDialog(unref(userSettings.value)).then((data) => {
        action.prepare(data.userSettings);
        action.execute();
    });
}
</script>

<template>
    <div class="grid grid-rows-2 grid-cols-[min-content_1fr_min-content] grid-flow-col gap-x-2 content-center items-center r-primary-bg r-primary-text">
        <div class="row-span-2">
            <a href="https://www.research-data-services.org" target="_blank">
                <img id="logo" src="@assets/img/rds-octopus-wh.svg" alt="RDS Logo" class="p-1.5" title="Visit the RDS website">
            </a>
        </div>
        <div class="font-bold self-center pt-3">
            Donald T. Rump
        </div>
        <div class="italic self-center pb-3">
            X Projects
        </div>
        <div class="row-span-2 pr-2">
            <Button plain rounded aria-label="Settings" title="Settings" @click="showUserSettings">
                <template #icon>
                    <span class="material-icons-outlined mi-settings r-primary-text" style="font-size: 40px;" />
                </template>
            </Button>
        </div>
    </div>
</template>

<style scoped lang="scss">
#logo {
    min-width: 5rem;
}
</style>
