import { type RouteRecordRaw } from "vue-router";

import { ComponentType, ComponentUnit } from "@common/component/ComponentIDs";
import { WebComponent } from "@common/component/WebComponent";
import { UnitID } from "@common/utils/UnitID";

import { Routes } from "@/component/Routes";

import Frontend from "@/ui/Frontend.vue";

import LandingView from "@/ui/views/LandingView.vue";

/**
 * The main frontend component class.
 */
export class FrontendComponent extends WebComponent {
    public constructor(appElement: string = "#app") {
        super(import.meta.env, new UnitID(ComponentType.Web, ComponentUnit.Frontend), Frontend, appElement);
    }

    protected defineRoutes(): RouteRecordRaw[] | null {
        return [
            {
                path: '/',
                component: LandingView,
                name: Routes.Landing,
            },
        ];
    }
}
