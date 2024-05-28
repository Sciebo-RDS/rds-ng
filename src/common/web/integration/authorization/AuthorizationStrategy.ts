import { WebComponent } from "../../component/WebComponent";

/**
 * Base class for all authorization strategies.
 */
export abstract class AuthorizationStrategy {
    protected readonly _component: WebComponent;

    private readonly _strategy: string;

    protected constructor(comp: WebComponent, strategy: string) {
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
