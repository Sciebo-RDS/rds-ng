import { GetMetadataProfilesReply } from "@common/api/metadata/MetadataCommands";
import { WebComponent } from "@common/component/WebComponent";
import { MetadataProfileContainer } from "@common/data/entities/metadata/MetadataProfileContainer";
import { Service } from "@common/services/Service";

import { FrontendServiceContext } from "@/services/FrontendServiceContext";
import { deepClone, shortenDataStrings } from "@common/utils/ObjectUtils";

/**
 * Creates the metadata service.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: WebComponent): Service {
    function printableProfile(profile: MetadataProfileContainer): string {
        let obj = deepClone<MetadataProfileContainer>(profile);
        return JSON.stringify(shortenDataStrings(obj));
    }

    return comp.createService(
        "Metadata service",
        (svc: Service) => {
            svc.messageHandler(GetMetadataProfilesReply, (msg: GetMetadataProfilesReply, ctx: FrontendServiceContext) => {
                if (msg.success) {
                    ctx.logger.debug("Retrieved metadata profiles", "metadata", { profiles: msg.profiles.map(printableProfile) });

                    // @ts-ignore
                    ctx.metadataStore.profiles = msg.profiles;
                } else {
                    ctx.logger.error("Unable to retrieve the metadata profiles", "metadata", { reason: msg.message });
                }
            });
        },
        FrontendServiceContext
    );
}
