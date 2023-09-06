import { ItemsCatalog } from "../../utils/ItemsCatalog";
import { type ConstructableMessage } from "./Message";

/**
 * Global catalog of all registered message types.
 *
 * This is a globally accessible list of all message types, associated with their respective message names.
 * It's mainly used to create proper message objects from incoming network messages.
 */

@ItemsCatalog.define()
export class MessageTypesCatalog extends ItemsCatalog<ConstructableMessage> {
}
