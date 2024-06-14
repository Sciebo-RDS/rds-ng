import { FrontendComponent } from "@/component/FrontendComponent";
import { SetSessionValueCommand } from "@common/api/session/SessionCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to set a session value stored on the server.
 */
export class SetSessionValueAction extends FrontendCommandAction<SetSessionValueCommand, CommandComposer<SetSessionValueCommand>> {
    public constructor(comp: FrontendComponent, suppressDefaultNotifiers: boolean = true) {
        super(comp, suppressDefaultNotifiers);
    }

    public prepare(key: string, value: any): CommandComposer<SetSessionValueCommand> {
        super.prepareNotifiers();

        this._composer = SetSessionValueCommand.build(this.messageBuilder, key, value);
        return this._composer;
    }
}
