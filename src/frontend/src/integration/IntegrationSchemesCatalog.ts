import { ItemsCatalog } from "@common/utils/ItemsCatalog";
import { type Constructable } from "@common/utils/Types";

import { IntegrationScheme } from "@/integration/IntegrationScheme";

/**
 * Global catalog of all supported integration schemes.
 */
@ItemsCatalog.define()
export class IntegrationSchemesCatalog extends ItemsCatalog<Constructable<IntegrationScheme>> {}
