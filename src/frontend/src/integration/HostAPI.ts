import { terminatePath } from "@common/utils/Paths";

import { FrontendComponent } from "@/component/FrontendComponent";
import { FrontendSettingIDs } from "@/settings/FrontendSettingIDs";

/**
 * All known host API endpoints.
 */
export const enum HostAPIEndpoints {
    PublicKey = "publickey",
    Resources = "resources",
}

/**
 * Formats a URL of the host API.
 *
 * @param comp - The frontend component.
 * @param endpoint - The target endpoint (may include query parameters).
 *
 * @returns - The URL as a string.
 */
export function resolveHostAPIEndpoint(comp: FrontendComponent, endpoint: string): string {
    let apiURL = comp.data.config.value<string>(FrontendSettingIDs.HostAPIURL);
    if (apiURL == "") {
        throw new Error("No host API URL has been configured");
    }
    apiURL = terminatePath(apiURL);
    return new URL(endpoint, new URL(apiURL)).toString();
}
