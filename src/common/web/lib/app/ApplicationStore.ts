import { defineStore } from "pinia";
import { Application } from "./Application";

export const useApplicationStore = defineStore("ApplicationStore", () => {
    const app: Application | null = null;

    const test = "HELLO???";

    return { app, test };
});
