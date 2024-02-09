import { Type } from "class-transformer";

import { type ConnectorInstanceID } from "../connector/ConnectorInstance";
import { type ProjectFeatureID } from "./features/ProjectFeature";

/**
 * Arbitrary UI options.
 */
export type UIOptions = Record<string, any>;

/**
 * Class holding all options of a **Project**.
 *
 * @param optional_features - A list of all user-enabled optional features.
 * @param use_all_connector_instances - Whether all available connector instances should be used.
 * @param active_connector_instances - List of connector instances to use for the project (if *use_all_connector_instances* is false).
 * @param ui - Arbitrary UI options.
 */
export class ProjectOptions {
    // @ts-ignore
    @Type(() => String)
    public readonly optional_features: ProjectFeatureID[];

    use_all_connector_instances: boolean;
    // @ts-ignore
    @Type(() => String)
    active_connector_instances: ConnectorInstanceID[];

    public readonly ui: UIOptions;

    public constructor(optionalFeatures: ProjectFeatureID[] = [], useAllConnectors: boolean = true, activeConnectorInstances: ConnectorInstanceID[] = [], uiOptions: UIOptions = {}) {
        this.optional_features = optionalFeatures;

        this.use_all_connector_instances = useAllConnectors;
        this.active_connector_instances = activeConnectorInstances;

        this.ui = uiOptions;
    }
}
