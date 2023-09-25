import { Channel } from "../core/messaging/Channel";
import { Command } from "../core/messaging/Command";
import { CommandReply } from "../core/messaging/CommandReply";
import { CommandComposer } from "../core/messaging/composers/CommandComposer";
import { CommandReplyComposer } from "../core/messaging/composers/CommandReplyComposer";
import { EventComposer } from "../core/messaging/composers/EventComposer";
import { MessageBuilder } from "../core/messaging/composers/MessageBuilder";
import { MessageComposer } from "../core/messaging/composers/MessageComposer";
import { Event } from "../core/messaging/Event";
import { Message } from "../core/messaging/Message";
import { networkStore } from "../data/stores/NetworkStore";
import { Service } from "../services/Service";

/**
 * Base class for UI controllers.
 *
 * Due to the nature of Vue, these controllers are generally rather simple and mostly deal with emitting messages based on user interaction.
 */
export class Controller {
    private readonly _service: Service;
    private readonly _serverChannel: Channel;

    /**
     * @param service - The service to use for message emission.
     */
    public constructor(service: Service) {
        const nwStore = networkStore();

        this._service = service;
        this._serverChannel = nwStore.serverChannel;
    }

    protected emitMessage<CompType extends MessageComposer<Message>, ExtType extends Function>(composer: CompType, extender: ExtType | null): void {
        if (extender) {
            extender(composer);
        }

        composer.emit(this._serverChannel);
    }

    protected get messageBuilder(): MessageBuilder {
        return this._service.messageBuilder;
    }
}

export type CommandComposerExtender<CmdType extends Command> = (composer: CommandComposer<CmdType>) => void;
export type CommandReplyComposerExtender<ReplyType extends CommandReply> = (composer: CommandReplyComposer<ReplyType>) => void;
export type EventExtender<EventType extends Event> = (composer: EventComposer<EventType>) => void;
