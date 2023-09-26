import { FrontendComponent } from "@/component/FrontendComponent";
import { MessageComposer } from "@common/core/messaging/composers/MessageComposer";
import { Message } from "@common/core/messaging/Message";
import { Action } from "@common/ui/actions/Action";

/**
 * A more specialized ``Action`` for the frontend.
 */
export abstract class FrontendAction<MsgType extends Message, CompType extends MessageComposer<MsgType>> extends Action<MsgType, CompType> {
    protected readonly _component: FrontendComponent;

    protected constructor(comp: FrontendComponent) {
        super(comp.frontendService);

        this._component = comp;
    }
}
