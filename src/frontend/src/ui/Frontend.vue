<script setup lang="ts">
import Panel from 'primevue/panel'
import TabView from "primevue/tabview";
import TabPanel from 'primevue/tabpanel';
import Toolbar from 'primevue/toolbar';
import Button from "primevue/button";
import Badge from "primevue/badge";
import ProgressBar from "primevue/progressbar";
import InputNumber from "primevue/inputnumber";
import SplitButton from "primevue/splitbutton";
import InputText from "primevue/inputtext";

const items = [
    {
        label: 'Update',
        icon: 'pi pi-refresh',
    },
    {
        label: 'Delete',
        icon: 'pi pi-times',
    },
    {
        label: 'Vue Website',
        icon: 'pi pi-external-link',
    },
    { label: 'Upload', icon: 'pi pi-upload' }
];
</script>

<template>
    <div class="r-centered-grid r-text">
        <div style="width: 800px;">
            <div>&nbsp;</div>
            <Panel header="Header">
                <p class="mt-0">
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
                    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </p>
            </Panel>

            <TabView>
                <TabPanel header="Header I">
                    <p>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
                        consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                    </p>
                </TabPanel>
                <TabPanel header="Header II">
                    <p>
                        Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim
                        ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Consectetur, adipisci velit, sed quia non numquam eius modi.
                    </p>
                </TabPanel>
                <TabPanel header="Header III">
                    <p>
                        At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui
                        officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus.
                    </p>
                </TabPanel>
            </TabView>
            <Toolbar>
                <template #start>
                    <Button label="New" icon="pi pi-plus" class="mr-2"/>
                    <Button label="Upload" icon="pi pi-upload" severity="success"/>
                    <i class="pi pi-bars p-toolbar-separator mr-2"/>
                    <SplitButton label="Save" icon="pi pi-check" :model="items" severity="warning"></SplitButton>
                </template>

                <template #end>
                    <Button icon="pi pi-search" class="mr-2"/>
                    <Button icon="pi pi-calendar" severity="success" class="mr-2"/>
                    <Button icon="pi pi-times" severity="danger"/>
                </template>
            </Toolbar>
            <div>
                <Badge value="2"></Badge>
                <Badge value="8" severity="success"></Badge>
                <Badge value="4" severity="info"></Badge>
                <Badge value="12" severity="warning"></Badge>
                <Badge value="3" severity="danger"></Badge>
            </div>
            <div class="card">
                <ProgressBar :value="50"></ProgressBar>
            </div>
            <div class="p-inputgroup w-full md:w-30rem">
                <span class="p-inputgroup-addon">
                    <i class="pi pi-clock"></i>
                </span>
                <span class="p-inputgroup-addon">
                    <i class="pi pi-star-fill"></i>
                </span>
                <InputNumber placeholder="Price"/>
                <span class="p-inputgroup-addon">$</span>
                <span class="p-inputgroup-addon">.00</span>
            </div>
            <div>
                <div class="p-inputgroup flex-1">
                    <Button icon="pi pi-check" severity="success"/>
                    <InputText placeholder="Vote"/>
                    <Button icon="pi pi-times" severity="danger"/>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
div {
    margin-bottom: 5px;
}
</style>
