import { AuthorizationStrategiesCatalog } from "../../../integration/authorization/strategies/AuthorizationStrategiesCatalog";
import { OAuth2Strategy, type OAuth2StrategyConfiguration } from "../../../integration/authorization/strategies/oauth2/OAuth2Strategy";
import { Connector, type ConnectorID } from "./Connector";
import { ConnectorInstance, type ConnectorInstanceID } from "./ConnectorInstance";

/**
 * Searches for a connector by its ID within a list of connectors.
 *
 * @param connectors - The list of connectors.
 * @param connectorID - The connector to search for.
 *
 * @returns - The found connector or **undefined** otherwise.
 */
export function findConnectorByID(connectors: Connector[], connectorID: ConnectorID): Connector | undefined {
    return connectors.find((con) => con.connector_id == connectorID);
}

/**
 * Searches for a connector instance by its ID within a list of connector instances.
 *
 * @param connectorInstances - The list of connector instances.
 * @param instanceID - The connector instance to search for.
 *
 * @returns - The found connector instance or **undefined** otherwise.
 */
export function findConnectorInstanceByID(connectorInstances: ConnectorInstance[], instanceID: ConnectorInstanceID): ConnectorInstance | undefined {
    return connectorInstances.find((inst) => inst.instance_id == instanceID);
}

/**
 * Checks whether a connector requires authorization (and whether that authorization strategy is available).
 *
 * @param connector - The connector.
 */
export function connectorRequiresAuthorization(connector: Connector): boolean {
    const strategy = connector.authorization.strategy;
    return strategy != "" && AuthorizationStrategiesCatalog.findItem(strategy) != undefined;
}

/**
 * Creates a strategy configuration from the authorization settings of a connector.
 *
 * @param connector - The connector.
 *
 * @returns - The strategy configuration.
 */
export function getStrategyConfigurationFromConnector(connector: Connector): Record<string, any> {
    switch (connector.authorization.strategy) {
        case OAuth2Strategy.Strategy:
            // For OAuth2, the stored configuration matches the proper structure already
            const config = connector.authorization.config as OAuth2StrategyConfiguration;
            config.client.embedded = false;
            return config;

        default:
            return {};
    }
}
