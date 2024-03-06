import { useUrlSearchParams } from "@vueuse/core";
import { useAxios } from "@vueuse/integrations/useAxios";
import { type KeyLike } from "jose";
import * as jose from "jose";
import { unref } from "vue";

import { FrontendComponent } from "@/component/FrontendComponent";
import { type HostUserToken } from "@/integration/HostUserToken";
import { FrontendSettingIDs } from "@/settings/FrontendSettingIDs";

export function useHostIntegration(comp: FrontendComponent) {
    // TODO: Many fixed & magic things, variables etc.; improve later
    async function getHostPublicKey(): Promise<KeyLike> { // TODO: Single Host only; must be extended later
        return new Promise<KeyLike>(async (resolve, reject) => {
            const pubKeyURL = comp.data.config.value<string>(FrontendSettingIDs.PublicKeyURL);
            if (pubKeyURL == "") {
                reject("No public key URL has been configured");
                return;
            }

            useAxios(pubKeyURL).then(async (response) => {
                if (response.isFinished) {
                    const data = unref(response.data);
                    if (!data.hasOwnProperty("public-key")) {
                        reject("The configured host doesn't provide a public key");
                        return;
                    }
                    resolve(JSON.parse(data["public-key"]) as KeyLike);
                }
            });
        });
    }

    function getUserToken(): string | undefined {
        const queryParams = useUrlSearchParams("history");
        return queryParams.hasOwnProperty("user-token") ? queryParams["user-token"] : undefined;
    }

    async function extractUserToken(): Promise<HostUserToken> {
        return new Promise<HostUserToken>(async (resolve, reject) => {
            getHostPublicKey().then(async (pubKey) => {
                const userToken = getUserToken();
                if (!userToken) {
                    reject("No user token has been provided");
                    return;
                }

                try {
                    const key = await jose.importJWK(pubKey);
                    const { payload } = await jose.compactVerify(userToken, key);

                    const jwtData = JSON.parse(new TextDecoder().decode(payload));
                    if (!jwtData.hasOwnProperty("user-token")) {
                        reject("The provided JWT doesn't contain any user token");
                        return;
                    }

                    const tokenData = jwtData["user-token"];
                    resolve({
                        userID: tokenData["user-id"],
                        userName: tokenData["user-name"]
                    } as HostUserToken);
                } catch (exc) {
                    reject(`The provided JWT is invalid: ${String(exc)}`);
                }
            });
        });
    }

    return {
        getHostPublicKey,
        getUserToken,
        extractUserToken
    };
}
