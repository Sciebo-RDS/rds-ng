import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";

import { FrontendComponent } from "@/component/FrontendComponent";

/**
 * Base class for all authorization strategies.
 */
export abstract class AuthorizationStrategy {
    protected readonly _component: FrontendComponent;

    private readonly _strategy: string;

    protected constructor(comp: FrontendComponent, strategy: string) {
        this._component = comp;

        this._strategy = strategy;
    }

    /**
     * Requests user authorization.
     *
     * @param authState - The current authorization state.
     */
    public abstract requestAuthorization(authState: AuthorizationState): void;

    /**
     * The strategy identifier.
     */
    public get strategy(): string {
        return this._strategy;
    }
}
