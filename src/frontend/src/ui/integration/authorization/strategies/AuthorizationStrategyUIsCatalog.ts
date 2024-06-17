import { ItemsCatalog } from "@common/utils/ItemsCatalog";

import { AuthorizationStrategyUI } from "@/ui/integration/authorization/strategies/AuthorizationStrategyUI";

/**
 * Global catalog of all registered strategy UIs.
 */
@ItemsCatalog.define()
export class AuthorizationStrategyUIsCatalog extends ItemsCatalog<AuthorizationStrategyUI> {}
