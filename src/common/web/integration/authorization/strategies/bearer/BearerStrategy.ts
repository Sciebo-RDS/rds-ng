import { WebComponent } from "../../../../component/WebComponent";
import { Service } from "../../../../services/Service";
import { bearerTokenDialog } from "../../../../ui/dialogs/authorization/BearerTokenDialog";
import { RedirectionTarget } from "../../../../utils/HTMLUtils";
import { AuthorizationRequest } from "../../AuthorizationRequest";
import { AuthorizationExecutionType, AuthorizationStrategy } from "../AuthorizationStrategy";
import { type BearerAuthorizationRequestData, type BearerStrategyConfiguration } from "./BearerTypes";

/**
 * Bearer authorization strategy.
 */
export class BearerStrategy extends AuthorizationStrategy {
    public static readonly Strategy = "bearer";

    private readonly _config: BearerStrategyConfiguration;

    public constructor(comp: WebComponent, svc: Service, config: BearerStrategyConfiguration) {
        super(comp, svc, BearerStrategy.Strategy, RedirectionTarget.Current);

        this._config = config;
    }

    protected initiateRequest(authRequest: AuthorizationRequest): void {
        bearerTokenDialog(this._component, this._config)
            .then((data) => {
                authRequest.extendedData = { bearer_token: data.bearerToken } as BearerAuthorizationRequestData;

                // We execute the request immediately
                this.executeAuthorizationRequest(authRequest, AuthorizationExecutionType.Direct)
                    .then(() => {})
                    .catch((error) => {});
            })
            .catch((_) => {
                // This will simply re-fetch all authorizations, just in case
                this.handleRequestCompletion();
            });
    }

    protected getRequestData(authRequest: AuthorizationRequest): any {
        return authRequest.extendedData as BearerAuthorizationRequestData;
    }
}

/**
 * Creates a new Bearer strategy instance, automatically configuring it.
 *
 * @param comp - The main component.
 * @param svc - The service to use for message sending.
 * @param config - The strategy configuration.
 *
 * @returns - The newly created strategy.
 */
export function createBearerStrategy(comp: WebComponent, svc: Service, config: Record<string, any>): BearerStrategy {
    const bearerConfig = config as BearerStrategyConfiguration;

    // Set defaults for non-critical settings
    if (!bearerConfig.bearer_label) {
        bearerConfig.bearer_label = "Bearer token";
    }

    return new BearerStrategy(comp, svc, bearerConfig);
}
