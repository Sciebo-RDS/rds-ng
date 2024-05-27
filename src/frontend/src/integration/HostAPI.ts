import { useAxios } from "@vueuse/integrations/useAxios";
import { type KeyLike } from "jose";
import { unref } from "vue";

import { terminatePath } from "@common/utils/Paths";

import { FrontendComponent } from "@/component/FrontendComponent";
import { FrontendSettingIDs } from "@/settings/FrontendSettingIDs";

/**
 * All known host API endpoints.
 */
const enum HostAPIEndpoints {
    PublicKey = "public-key",
}

/**
 * The host integration API.
 */
export class HostAPI {
    private readonly _apiURL: string;

    public constructor(comp: FrontendComponent) {
        this._apiURL = comp.data.config.value<string>(FrontendSettingIDs.HostAPIURL);
        if (this._apiURL == "") {
            throw new Error("No host API URL has been configured");
        }
        this._apiURL = terminatePath(this._apiURL);
    }

    public async getPublicKey(): Promise<KeyLike> {
        const PubKeyDataName = "public-key";

        // TODO: Single Host only; extend later
        return new Promise<KeyLike>(async (resolve, reject) => {
            const pubKeyURL = this.resolveAPIEndpoint(HostAPIEndpoints.PublicKey);
            useAxios(pubKeyURL).then(async (response) => {
                if (!response.isFinished) {
                    return;
                }

                const data = unref(response.data);
                if (!data.hasOwnProperty(PubKeyDataName)) {
                    reject("The configured host doesn't provide a public key");
                    return;
                }
                resolve(JSON.parse(data[PubKeyDataName]) as KeyLike);
            });
        });
    }

    private resolveAPIEndpoint(endpoint: string): string {
        return new URL(endpoint, new URL(this._apiURL)).toString();
    }
}
