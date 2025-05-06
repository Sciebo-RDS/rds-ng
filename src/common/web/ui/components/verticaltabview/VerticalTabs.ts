import { type VueComponent } from "../../../component/WebComponent";

/**
 * The definition of a tab for the vertical tabs component.
 */
export interface VerticalTabDefinition {
    title: string;
    component: VueComponent;

    icon?: string;
}
