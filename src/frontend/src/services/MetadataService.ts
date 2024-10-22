import { GetMetadataProfilesReply } from "@common/api/metadata/MetadataCommands";
import { MetadataProfileContainer } from "@common/data/entities/metadata/MetadataProfileContainer";
import { Service } from "@common/services/Service";
import { ColorTable } from "@common/ui/components/propertyeditor/utils/ColorTable";
import { deepClone, shortenDataStrings } from "@common/utils/ObjectUtils";

import { FrontendComponent } from "@/component/FrontendComponent";
import { FrontendServiceContext } from "@/services/FrontendServiceContext";

/**
 * Creates the metadata service.
 *
 * @param comp - The main component instance.
 *
 * @returns - The newly created service.
 */
export default function (comp: FrontendComponent): Service {
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

                    ColorTable.populateFromProfileContainerList(ctx.metadataStore.profiles);
                } else {
                    ctx.logger.error("Unable to retrieve the metadata profiles", "metadata", { reason: msg.message });
                }
            });
        },
        FrontendServiceContext
    );
}
