import { Command } from "@common/core/messaging/Command";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { CommandAction } from "@common/ui/actions/CommandAction";

import { FrontendComponent } from "@/component/FrontendComponent";

/**
 * Command actions specific to the frontend.
 */
export abstract class FrontendCommandAction<CmdType extends Command, CompType extends CommandComposer<CmdType>> extends CommandAction<CmdType, CompType> {
    protected _component: FrontendComponent;

    /**
     * @param comp - The main frontend component.
     * @param suppressDefaultNotifiers - Suppress default notifiers.
     */
    public constructor(comp: FrontendComponent, suppressDefaultNotifiers: boolean = false) {
        super(comp.frontendService, suppressDefaultNotifiers);

        this._component = comp;
    }
}
