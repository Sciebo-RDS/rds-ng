import { ItemsCatalog } from "../../utils/ItemsCatalog";
import { type Constructable } from "../../utils/Types";
import { AuthorizationStrategy } from "./AuthorizationStrategy";

/**
 * Global catalog of all supported authorization strategies.
 */
@ItemsCatalog.define()
export class AuthorizationStrategiesCatalog extends ItemsCatalog<Constructable<AuthorizationStrategy>> {}
