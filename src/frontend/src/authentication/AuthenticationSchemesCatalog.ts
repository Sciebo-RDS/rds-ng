import { ItemsCatalog } from "@common/utils/ItemsCatalog";

import { AuthenticationScheme } from "@/authentication/AuthenticationScheme";

/**
 * Global catalog of all supported authentication schemes.
 */
@ItemsCatalog.define()
export class AuthenticationSchemesCatalog extends ItemsCatalog<AuthenticationScheme> {
}
