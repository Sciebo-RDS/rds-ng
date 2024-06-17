import { FrontendComponent } from "@/component/FrontendComponent";
import { GetSessionValueCommand } from "@common/api/session/SessionCommands";
import { CommandComposer } from "@common/core/messaging/composers/CommandComposer";

import { FrontendCommandAction } from "@/ui/actions/FrontendCommandAction";

/**
 * Action to get a session value stored on the server.
 */
export class GetSessionValueAction extends FrontendCommandAction<GetSessionValueCommand, CommandComposer<GetSessionValueCommand>> {
    public constructor(comp: FrontendComponent, suppressDefaultNotifiers: boolean = true) {
        super(comp, suppressDefaultNotifiers);
    }

    public prepare(key: string): CommandComposer<GetSessionValueCommand> {
        super.prepareNotifiers();

        this._composer = GetSessionValueCommand.build(this.messageBuilder, key);
        return this._composer;
    }
}
