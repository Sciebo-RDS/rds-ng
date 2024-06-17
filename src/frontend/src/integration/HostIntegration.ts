import { type KeyLike } from "jose";
import * as jose from "jose";

import { FrontendComponent } from "@/component/FrontendComponent";
import { type HostAuthorization, type HostResources, type HostUserToken, hostUserTokenFromData } from "@/integration/HostTypes";
import { HostAPI } from "@/integration/HostAPI";

import { getURLQueryParam } from "@common/utils/URLUtils";

export function useHostIntegration(comp: FrontendComponent) {
    const api = new HostAPI(comp);

    async function getHostUserToken(): Promise<HostUserToken> {
        return new Promise<HostUserToken>(async (resolve, reject) => {
            const UserTokenDataName = "user-token";

            api.getPublicKey().then(async (pubKey: KeyLike) => {
                const userToken = getURLQueryParam(UserTokenDataName);
                if (!userToken) {
                    reject("No user token has been provided");
                    return;
                }

                try {
                    const key = await jose.importJWK(pubKey);
                    const { payload } = await jose.compactVerify(userToken, key);

                    const jwtData = JSON.parse(new TextDecoder().decode(payload));
                    if (!jwtData.hasOwnProperty(UserTokenDataName)) {
                        reject("The provided JWT doesn't contain any user token");
                        return;
                    }
                    resolve(hostUserTokenFromData(jwtData[UserTokenDataName]));
                } catch (exc) {
                    reject(`The provided JWT is invalid: ${String(exc)}`);
                }
            });
        });
    }

    async function getHostAuthorization(): Promise<HostAuthorization> {
        return api.getAuthorization();
    }

    async function getHostResources(): Promise<HostResources> {
        return api.getResources();
    }

    return {
        getHostUserToken,
        getHostAuthorization,
        getHostResources,
    };
}
