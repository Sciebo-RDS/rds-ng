import { useAxios } from "@vueuse/integrations/useAxios";
import { type KeyLike } from "jose";
import { unref } from "vue";

import { terminatePath } from "@common/utils/Paths";

import { FrontendComponent } from "@/component/FrontendComponent";
import { type HostAuthorization } from "@/integration/HostTypes";
import { HostIntegrationSettingIDs } from "@/settings/IntegrationSettingIDs";

/**
 * All known host API endpoints.
 */
const enum HostAPIEndpoints {
    PublicKey = "public-key",
    Authorization = "authorization",
}

/**
 * The host integration API.
 */
export class HostAPI {
    private readonly _apiURL: string;

    public constructor(comp: FrontendComponent) {
        this._apiURL = comp.data.config.value<string>(HostIntegrationSettingIDs.APIURL);
        if (this._apiURL == "") {
            throw new Error("No host API URL has been configured");
        }
        this._apiURL = terminatePath(this._apiURL);
    }

    public async getPublicKey(): Promise<KeyLike> {
        return this.getEndpointData<KeyLike>(HostAPIEndpoints.PublicKey, "public-key", true);
    }

    public async getAuthorization(): Promise<HostAuthorization> {
        return this.getEndpointData<HostAuthorization>(HostAPIEndpoints.Authorization, "authorization");
    }

    private resolveAPIEndpoint(endpoint: string): string {
        return new URL(endpoint, new URL(this._apiURL)).toString();
    }

    private async getEndpointData<DataType>(endpoint: string, dataName: string, decodeData: boolean = false): Promise<DataType> {
        return new Promise<DataType>(async (resolve, reject) => {
            const url = this.resolveAPIEndpoint(endpoint);
            useAxios(url).then(async (response) => {
                if (!response.isFinished) {
                    return;
                }

                const data = unref(response.data);
                if (!data.hasOwnProperty(dataName)) {
                    reject("The configured host doesn't provide the proper data");
                    return;
                }
                resolve(decodeData ? (JSON.parse(data[dataName]) as DataType) : (data[dataName] as DataType));
            });
        });
    }
}
