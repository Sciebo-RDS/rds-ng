import { GetUserSettingsReply, SetUserSettingsReply } from "@common/api/user/UserCommands";
import { UserSettingsChangedEvent } from "@common/api/user/UserEvents";
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
export default function (comp: WebComponent): Service {
    return comp.createService(
        "User service",
        (svc: Service) => {
            svc.messageHandler(GetUserSettingsReply, (msg: GetUserSettingsReply, ctx: FrontendServiceContext) => {
                if (msg.success) {
                    ctx.logger.debug("Retrieved user settings", "user", { settings: JSON.stringify(msg.settings) });

                    // @ts-ignore
                    ctx.userStore.userSettings = msg.settings;
                } else {
                    ctx.logger.error("Unable to retrieve the user settings", "user", { reason: msg.message });
                }
            });

            svc.messageHandler(SetUserSettingsReply, (msg: SetUserSettingsReply, ctx: FrontendServiceContext) => {
                if (msg.success) {
                    ctx.logger.debug("Updated the user settings", "user", { settings: JSON.stringify(msg.settings) });

                    // @ts-ignore
                    ctx.userStore.userSettings = msg.settings;
                } else {
                    ctx.logger.error("Unable to update the user settings", "user", { reason: msg.message });
                }
            });

            svc.messageHandler(UserSettingsChangedEvent, (msg: UserSettingsChangedEvent, ctx: FrontendServiceContext) => {
                ctx.logger.debug("User settings update received", "user", { settings: JSON.stringify(msg.settings) });

                // @ts-ignore
                ctx.userStore.userSettings = msg.settings;
            });
        },
        FrontendServiceContext,
    );
}
