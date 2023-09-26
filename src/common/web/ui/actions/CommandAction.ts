import { Command } from "../../core/messaging/Command";
import { CommandComposer } from "../../core/messaging/composers/CommandComposer";
import { Action } from "./Action";

export type CommandActionCallback<CmdType extends Command> = (composer: CommandComposer<CmdType>) => void;

/**
 * Command actions.
 */
export class CommandAction<CmdType extends Command> extends Action<CmdType, CommandComposer<CmdType>> {
}
