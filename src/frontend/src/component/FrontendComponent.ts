import { ComponentType, ComponentUnit } from "@common/component/ComponentIDs";
import { WebComponent } from "@common/component/WebComponent";
import { UnitID } from "@common/utils/UnitID";

import App from "@/component/App.vue";

/**
 * The main frontend component class.
 */
export class FrontendComponent extends WebComponent {
    public constructor(appElement: string = "#app") {
        super(import.meta.env, new UnitID(ComponentType.Web, ComponentUnit.Frontend), App, appElement);
    }
}
