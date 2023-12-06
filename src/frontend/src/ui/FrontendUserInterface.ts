import { type Component as VueComponent } from "vue";
import { type Router, type RouteRecordRaw } from "vue-router";

import { DataManagementPlanFeature } from "@common/features/DataManagementPlanFeature";
import { MetadataFeature } from "@common/features/MetadataFeature";
import { type ProjectFeaturePanelLoaders } from "@common/features/ProjectFeaturePanelLoader";
import { SummaryFeature } from "@common/features/SummaryFeature";
import { UserInterface } from "@common/ui/UserInterface";
import { View } from "@common/ui/views/View";

import { FrontendView } from "@/ui/views/frontend/FrontendView";

/**
 * Class for frontend-specific user interface handling.
 */
export class FrontendUserInterface extends UserInterface {
    private readonly _frontendView: FrontendView;

    /**
     * @param router - The Vue router.
     * @param appRoot - The root (main) application component.
     */
    public constructor(router: Router, appRoot: VueComponent) {
        super(router, appRoot);

        // We know in which order we placed the sub-views, so we can safely assign them to local variables
        this._frontendView = this.mainView.subViews[0]! as FrontendView;
    }

    public configureProjectFeaturePanels(): ProjectFeaturePanelLoaders | undefined {
        const panelLoaders: ProjectFeaturePanelLoaders = {};

        panelLoaders[MetadataFeature.FeatureID] = () => import("frontend/src/ui/content/features/MetadataPanel.vue");
        panelLoaders[DataManagementPlanFeature.FeatureID] = () => import("frontend/src/ui/content/features/DataManagementPlanPanel.vue");
        panelLoaders[SummaryFeature.FeatureID] = () => import("frontend/src/ui/content/features/SummaryPanel.vue");

        return panelLoaders;
    }

    protected configureMainRoute(): RouteRecordRaw | undefined {
        return {
            redirect: `/${FrontendView.rootPath}`
        } as RouteRecordRaw;
    }

    protected createSubViews(router: Router): View[] {
        return [new FrontendView(router)];
    }

    /**
     * The frontend view.
     */
    public get frontendView(): FrontendView {
        return this._frontendView!;
    }
}
