import { WebComponent } from "../../../component/WebComponent";
import { Service } from "../../../services/Service";
import { ItemsCatalog } from "../../../utils/ItemsCatalog";
import { AuthorizationStrategy } from "./AuthorizationStrategy";

export type AuthorizationStrategyCreator = (comp: WebComponent, svc: Service, config: Record<string, any>) => AuthorizationStrategy;

/**
 * Global catalog of creator functions for all known authorization strategies.
 */
@ItemsCatalog.define()
export class AuthorizationStrategiesCatalog extends ItemsCatalog<AuthorizationStrategyCreator> {}
