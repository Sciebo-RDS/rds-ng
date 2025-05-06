<script setup>
import Button from "primevue/button";
import ConfirmDialog from "primevue/confirmdialog";
</script>

<template>
    <ConfirmDialog group="messagedlg">
        <template #container="{ message, acceptCallback }">
            <div class="flex flex-col items-center p-5 rounded">
                <div class="rounded-full flex justify-center items-center h-[5rem] w-[5rem] -mt-[3.75rem]" :class="message.background">
                    <span class="!text-5xl text-white" :class="message.icon" />
                </div>

                <span class="self-start font-bold text-2xl block mb-2 mt-4">{{ message.header }}</span>
                <p class="self-start mb-0">{{ message.message }}</p>

                <div class="flex self-end gap-2 mt-6">
                    <Button label="OK" outlined @click="acceptCallback" />
                </div>
            </div>
        </template>
    </ConfirmDialog>
</template>

<style scoped lang="scss"></style>
