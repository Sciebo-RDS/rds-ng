import { OAuth2Strategy } from "@common/integration/authorization/strategies/oauth2/OAuth2Strategy";

import { AuthorizationStrategyUIsCatalog } from "@/ui/integration/authorization/strategies/AuthorizationStrategyUIsCatalog";
import { OAuth2StrategyUI } from "@/ui/integration/authorization/strategies/oauth2/OAuth2StrategyUI";

/**
 * Registers all available authorization strategy UIs.
 *
 * When adding a new strategy, always register its UI here as well.
 */
export function registerAuthorizationStrategyUIs(): void {
    // New strategy UIs go here
    AuthorizationStrategyUIsCatalog.registerItem(OAuth2Strategy.Strategy, new OAuth2StrategyUI());
}
