import { Application } from "./app/Application";

export const useCommon = () => {
    const app = Application.instance;
    return { app, };
};
