import { GetUserConfigurationReply, SetUserConfigurationReply } from "@common/api/user/UserCommands";
import { UserConfigurationEvent } from "@common/api/user/UserEvents";
import { WebComponent } from "@common/component/WebComponent";
import { Service } from "@common/services/Service";

import { FrontendServiceContext } from "@/services/FrontendServiceContext";

/**
 * Creates the user service.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function(comp: WebComponent): Service {
    return comp.createService(
        "User service",
        (svc: Service) => {
            svc.messageHandler(GetUserConfigurationReply, (msg: GetUserConfigurationReply, ctx: FrontendServiceContext) => {
                if (msg.success) {
                    ctx.logger.debug("Retrieved user configuration", "user", { configuration: JSON.stringify(msg.configuration) });

                    // @ts-ignore
                    ctx.userStore.configuration = msg.configuration;
                } else {
                    ctx.logger.error("Unable to retrieve the user configuration", "user", { reason: msg.message });
                }
            });

            svc.messageHandler(SetUserConfigurationReply, (msg: SetUserConfigurationReply, ctx: FrontendServiceContext) => {
                if (msg.success) {
                    ctx.logger.debug("Updated the user configuration", "user");
                } else {
                    ctx.logger.error("Unable to update the user configuration", "user", { reason: msg.message });
                }
            });

            svc.messageHandler(UserConfigurationEvent, (msg: UserConfigurationEvent, ctx: FrontendServiceContext) => {
                ctx.logger.debug("User configuration update received", "user", { configuration: JSON.stringify(msg.configuration) });

                // @ts-ignore
                ctx.userStore.configuration = msg.configuration;
            });
        },
        FrontendServiceContext
    );
}
