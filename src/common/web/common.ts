import { Component } from "./component/Component";

/**
 * Composable for easy access of commonly used global instances.
 */
export const useCommon = () => {
    const app = Component.instance;
    return { app, };
};
