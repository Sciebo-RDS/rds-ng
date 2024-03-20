import { ItemsCatalog } from "@common/utils/ItemsCatalog";
import { type Constructable } from "@common/utils/Types";

import { AuthenticationScheme } from "@/authentication/AuthenticationScheme";

/**
 * Global catalog of all supported authentication schemes.
 */
@ItemsCatalog.define()
export class AuthenticationSchemesCatalog extends ItemsCatalog<Constructable<AuthenticationScheme>> {
}
