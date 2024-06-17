import { WebComponent } from "../../../component/WebComponent";
import logging from "../../../core/logging/Logging";
import { Service } from "../../../services/Service";
import { AuthorizationStrategiesCatalog } from "./AuthorizationStrategiesCatalog";
import { AuthorizationStrategy } from "./AuthorizationStrategy";
import { createOAuth2Strategy, OAuth2Strategy } from "./oauth2/OAuth2Strategy";

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
 * @param svc - The service to use for message sending.
 * @param strategy - The strategy identifier.
 * @param config - The host strategy configuration as an arbitrary record.
 *
 * @returns - The newly created strategy.
 */
export function createAuthorizationStrategy(comp: WebComponent, svc: Service, strategy: string, config: Record<string, any>): AuthorizationStrategy {
    if (!strategy) {
        throw new Error("No authorization strategy has been provided");
    }

    const strategyCreator = AuthorizationStrategiesCatalog.findItem(strategy);
    if (!strategyCreator) {
        throw new Error(`The authorization strategy '${strategy}' couldn't be found`);
    }

    return strategyCreator(comp, svc, config);
}
