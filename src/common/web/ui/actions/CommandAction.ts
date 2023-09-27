import { Command } from "../../core/messaging/Command";
import { CommandFailType } from "../../core/messaging/CommandReply";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { Action, ActionState } from "./Action";

/**
 * Actions specific to ``Command`.
 */
export abstract class CommandAction<CmdType extends Command, CompType extends CommandComposer<CmdType>> extends Action<CmdType, CompType> {
    protected preExecution(): void {
        this._composer!
            .done((cmd: Command, success: boolean, msg: string) => {
                this.setState(success ? ActionState.Done : ActionState.Failed, msg);
            })
            .failed((failType: CommandFailType, msg: string) => {
                this.setState(ActionState.Failed, msg);
            });

        super.preExecution();
    }
}
