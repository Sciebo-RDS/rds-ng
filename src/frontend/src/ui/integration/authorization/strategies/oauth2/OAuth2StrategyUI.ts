import { AuthorizationState } from "@common/data/entities/authorization/AuthorizationState";
import { Connector } from "@common/data/entities/connector/Connector";
import { ConnectorInstance } from "@common/data/entities/connector/ConnectorInstance";
import { OAuth2Strategy } from "@common/integration/authorization/strategies/oauth2/OAuth2Strategy";

import { AuthorizationStrategyUI, type AuthorizationStrategyUIMenuEntry } from "@/ui/integration/authorization/strategies/AuthorizationStrategyUI";
import { requestConnectorInstanceAuthorization, revokeConnectorInstanceAuthorization } from "@common/integration/authorization/AuthorizationUtils";

export class OAuth2StrategyUI extends AuthorizationStrategyUI {
    public constructor() {
        super(OAuth2Strategy.Strategy, {
            name: "OAuth2",
            integration: {
                loader: () => import("./OAuth2StrategyUI.vue"),
                providesMenuEntry: true,
            },
        });
    }

    public getMenuEntry(authState: AuthorizationState): AuthorizationStrategyUIMenuEntry | undefined {
        switch (authState) {
            case AuthorizationState.Authorized:
                return {
                    label: "Disconnect",
                    icon: "material-icons-outlined mi-link-off",

                    command: (connector: Connector, instance: ConnectorInstance) =>
                        revokeConnectorInstanceAuthorization(OAuth2Strategy.Strategy, connector, instance),
                } as AuthorizationStrategyUIMenuEntry;

            case AuthorizationState.NotAuthorized:
                return {
                    label: "Connect",
                    icon: "material-icons-outlined mi-link",

                    command: (connector: Connector, instance: ConnectorInstance) =>
                        requestConnectorInstanceAuthorization(OAuth2Strategy.Strategy, connector, instance),
                } as AuthorizationStrategyUIMenuEntry;

            default:
                return undefined;
        }
    }
}
