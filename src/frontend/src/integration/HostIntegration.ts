import { useUrlSearchParams } from "@vueuse/core";
import { useAxios } from "@vueuse/integrations/useAxios";
import * as jose from "jose";
import { unref, watch } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { type HostUserToken } from "@/integration/HostUserToken";
import { FrontendSettingIDs } from "@/settings/FrontendSettingIDs";

export function useHostIntegration(comp: FrontendComponent) {
    function getUserToken(): Promise<HostUserToken> {
        // TODO: Many fixed & magic things, variables etc.; improve later
        return new Promise<HostUserToken>((resolve, reject) => {
            const pubKeyURL = comp.data.config.value<string>(FrontendSettingIDs.PublicKeyURL);
            if (pubKeyURL == "") {
                reject("No public key URL has been configured");
                return;
            }

            const { data, isFinished } = useAxios(pubKeyURL);
            watch(isFinished, async (finished) => {
                if (finished) {
                    if (!unref(data).hasOwnProperty("public-key")) {
                        reject("Couldn't retrieve the public key of the host system");
                        return;
                    }
                    const key = JSON.parse(unref(data)["public-key"]);

                    const queryParams = useUrlSearchParams("history");
                    if (!queryParams.hasOwnProperty("user-token")) {
                        reject("User token not provided");
                        return;
                    }

                    try {
                        const pubKey = await jose.importJWK(key);
                        const { payload } = await jose.compactVerify(queryParams["user-token"] as string, pubKey);

                        const jwtData = JSON.parse(new TextDecoder().decode(payload));
                        if (!jwtData.hasOwnProperty("user-token")) {
                            reject("The provided JWT doesn't contain any user token");
                            return;
                        }
                        resolve({
                            UserID: jwtData["user-token"]["user-id"],
                            UserName: jwtData["user-token"]["user-name"]
                        } as HostUserToken);
                    } catch (exc) {
                        reject(`The provided JWT is invalid: ${String(exc)}`);
                    }
                }
            });
        });
    }

    return {
        getUserToken
    };
}
