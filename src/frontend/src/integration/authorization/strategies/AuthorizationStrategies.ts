import logging from "@common/core/logging/Logging";

import { FrontendComponent } from "@/component/FrontendComponent";
import { AuthorizationStrategy } from "@/integration/authorization/strategies/AuthorizationStrategy";
import { AuthorizationStrategiesCatalog } from "@/integration/authorization/strategies/AuthorizationStrategiesCatalog";
import { createOAuth2Strategy, OAuth2Strategy } from "@/integration/authorization/strategies/OAuth2Strategy";

/**
 * Registers all available authorization strategies.
 *
 * When adding a new strategy, always register it here.
 */
export function registerAuthorizationStrategies(): void {
    // New strategies go here
    AuthorizationStrategiesCatalog.registerItem(OAuth2Strategy.Strategy, createOAuth2Strategy);

    // Print all available strategies for debugging purposes
    const names = Object.keys(AuthorizationStrategiesCatalog.items);
    logging.debug(`Registered authorization strategies: ${names.join("; ")}`);
}

/**
 * Creates an authorization strategy using the specified identifier.
 *
 * @param comp - The global component.
 * @param strategy - The strategy identifier.
 * @param config - The host strategy configuration as an arbitrary record.
 */
export function createAuthorizationStrategy(comp: FrontendComponent, strategy: string, config: Record<string, any>): AuthorizationStrategy {
    if (!strategy) {
        throw new Error("No authorization strategy has been provided");
    }

    const strategyCreator = AuthorizationStrategiesCatalog.findItem(strategy);
    if (!strategyCreator) {
        throw new Error(`The authorization strategy '${strategy}' couldn't be found`);
    }

    return strategyCreator(comp, config);
}
