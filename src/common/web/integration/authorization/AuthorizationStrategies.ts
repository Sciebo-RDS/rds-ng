import { WebComponent } from "../../component/WebComponent";
import logging from "../../core/logging/Logging";
import { type Constructable } from "../../utils/Types";
import { AuthorizationStrategiesCatalog } from "./AuthorizationStrategiesCatalog";
import { AuthorizationStrategy } from "./AuthorizationStrategy";
import { OAuth2Strategy } from "./OAuth2Strategy";

/**
 * Registers all available authorization strategies.
 *
 * When adding a new strategy, always register it here.
 */
export function registerAuthorizationStrategies(): void {
    interface ConstructableStrategy extends Constructable<AuthorizationStrategy> {
        Strategy: string;
    }

    function registerStrategy(strategy: ConstructableStrategy): void {
        AuthorizationStrategiesCatalog.registerItem(strategy.Strategy, strategy);
    }

    // New strategies go here
    registerStrategy(OAuth2Strategy);

    // Print all available strategies for debugging purposes
    const names = Object.keys(AuthorizationStrategiesCatalog.items);
    logging.debug(`Registered authorization strategies: ${names.join("; ")}`);
}

/**
 * Creates an authorization strategy using its global identifier.
 *
 * @param comp - The main component.
 * @param strategy - The strategy identifier.
 * @param config - The strategy configuration.
 */
export function createAuthorizationStrategy(comp: WebComponent, strategy: string, config: Record<string, any>): AuthorizationStrategy {
    const authStrategy = AuthorizationStrategiesCatalog.findItem(strategy);
    if (!authStrategy) {
        throw new Error(`The authorization strategy '${strategy}' couldn't be found`);
    }

    return new authStrategy(comp, config);
}
