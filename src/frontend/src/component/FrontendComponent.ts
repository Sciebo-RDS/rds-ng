import { type RouteRecordRaw } from "vue-router";

import { ComponentType, ComponentUnit } from "@common/component/ComponentIDs";
import { WebComponent } from "@common/component/WebComponent";
import { UnitID } from "@common/utils/UnitID";

import Frontend from "@/ui/Frontend.vue";

/**
 * The main frontend component class.
 */
export class FrontendComponent extends WebComponent {
    public constructor(appElement: string = "#app") {
        super(import.meta.env, new UnitID(ComponentType.Web, ComponentUnit.Frontend), Frontend, appElement);
    }

    protected configureRoutes(): RouteRecordRaw[] {
        return [];
    }
}
