import { ItemsCatalog } from "@common/utils/ItemsCatalog";

import { ConnectorCategory } from "./ConnectorCategory";

/**
 * Global catalog of all supported authentication schemes.
 */
@ItemsCatalog.define()
export class ConnectorCategoriesCatalog extends ItemsCatalog<ConnectorCategory> {}
