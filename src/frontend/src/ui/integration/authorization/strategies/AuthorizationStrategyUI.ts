import type { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import type { Connector } from "@common/data/entities/connector/Connector";
import type { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";

/**
 * Dynamic strategy integration Vue component loader.
 */
export type AuthorizationStrategyUILoader = () => any;

/**
 * Options for strategy UI menu entries.
 */
export interface AuthorizationStrategyUIMenuEntry {
    label: string;
    icon?: string;

    command: (connector: Connector, instance: ConnectorInstance) => void;
}

/**
 * Options to initialize an authorization UI.
 */
export interface AuthorizationStrategyUIOptions {
    /** The general display name. */
    name: string;

    /** Integration options. */
    integration?: {
        /** The integration loader. */
        loader: AuthorizationStrategyUILoader;

        /** Whether the UI provides a menu entry. */
        providesMenuEntry: boolean;
    };
}

/**
 * The strategy UI represents how an authorization integrates itself into the existing UI.
 */
export abstract class AuthorizationStrategyUI {
    private readonly _strategy: string;
    private readonly _options: AuthorizationStrategyUIOptions;

    /**
     * @param strategy - The strategy identifier.
     * @param options - The strategy UI options.
     */
    protected constructor(strategy: string, options: AuthorizationStrategyUIOptions) {
        this._strategy = strategy;
        this._options = options;
    }

    /**
     * Gets a menu entry depending on its authorization state.
     *
     * @param authState - The current authorization state.
     */
    public getMenuEntry(authState: AuthorizationState): AuthorizationStrategyUIMenuEntry | undefined {
        return undefined;
    }

    /**
     * The strategy identifier.
     */
    public get strategy(): string {
        return this._strategy;
    }

    /**
     * The strategy UI options.
     */
    public get options(): AuthorizationStrategyUIOptions {
        return this._options;
    }

    /**
     * Whether this UI has an integration component.
     */
    public hasIntegration(): boolean {
        return !!this._options.integration;
    }
}
