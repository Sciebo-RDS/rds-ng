import { Command } from "@common/core/messaging/Command";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";
import { CommandAction } from "@common/ui/actions/CommandAction";

import { FrontendComponent } from "@/component/FrontendComponent";
import { FrontendSettingIDs } from "@/settings/FrontendSettingIDs";

/**
 * Command actions specific to the frontend.
 */
export abstract class FrontendCommandAction<CmdType extends Command, CompType extends CommandComposer<CmdType>> extends CommandAction<CmdType, CompType> {
    protected _component: FrontendComponent;

    protected _regularTimeout: number;

    public constructor(comp: FrontendComponent) {
        super(comp.frontendService);

        this._component = comp;

        this._regularTimeout = comp.data.config.value(FrontendSettingIDs.RegularCommandTimeout);
    }
}
