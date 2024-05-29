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

    public abstract requestAuthorization(): void;

    /**
     * The strategy identifier.
     */
    public get strategy(): string {
        return this._strategy;
    }
}
