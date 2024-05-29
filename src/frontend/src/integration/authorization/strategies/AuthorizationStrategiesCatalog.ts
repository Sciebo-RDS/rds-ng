import { FrontendComponent } from "@/component/FrontendComponent";
import { AuthorizationStrategy } from "@/integration/authorization/strategies/AuthorizationStrategy";
import { ItemsCatalog } from "@common/utils/ItemsCatalog";

export type AuthorizationStrategyCreator = (comp: FrontendComponent, config: Record<string, any>) => AuthorizationStrategy;

/**
 * Global catalog of creator functions for all known authorization strategies.
 */
@ItemsCatalog.define()
export class AuthorizationStrategiesCatalog extends ItemsCatalog<AuthorizationStrategyCreator> {}
