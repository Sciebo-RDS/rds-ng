import { useUrlSearchParams } from "@vueuse/core";
import { useAxios } from "@vueuse/integrations/useAxios";
import { plainToInstance } from "class-transformer";
import { type KeyLike } from "jose";
import * as jose from "jose";
import { unref } from "vue";

import { ResourcesList } from "@common/data/entities/resource/ResourcesList";

import { FrontendComponent } from "@/component/FrontendComponent";
import { HostAPIEndpoints, resolveHostAPIEndpoint } from "@/integration/HostAPI";
import { type HostUserToken } from "@/integration/HostUserToken";

export function useHostIntegration(comp: FrontendComponent) {
    // TODO: Many fixed & magic things, variables etc.; improve later
    async function getHostPublicKey(): Promise<KeyLike> { // TODO: Single Host only; must be extended later
        return new Promise<KeyLike>(async (resolve, reject) => {
            const pubKeyURL = resolveHostAPIEndpoint(comp, HostAPIEndpoints.PublicKey);
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

    // TODO: Temporary only
    async function getResourcesList(systemID: string): Promise<ResourcesList> {
        return new Promise<ResourcesList>(async (resolve, reject) => {
            const resourcesURL = resolveHostAPIEndpoint(comp, `${HostAPIEndpoints.Resources}?uid=${systemID}`);
            useAxios(resourcesURL).then(async (response) => {
                if (response.isFinished) {
                    const data = unref(response.data);
                    if (!data.hasOwnProperty("resources")) {
                        reject("The configured host doesn't provide a resources list");
                        return;
                    }
                    const resourcesData = JSON.parse(data["resources"] as string);
                    resolve(plainToInstance(ResourcesList, resourcesData) as ResourcesList);
                }
            });
        });
    }

    function getUserToken(): string | undefined {
        const queryParams = useUrlSearchParams("history");
        return queryParams.hasOwnProperty("user-token") ? queryParams["user-token"] as string : undefined;
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
                        systemID: tokenData["system-id"],
                        userName: tokenData["user-name"]
                    } as HostUserToken);
                } catch (exc) {
                    console.trace();
                    reject(`The provided JWT is invalid: ${String(exc)}`);
                }
            });
        });
    }

    return {
        getHostPublicKey,
        getUserToken,
        getResourcesList,
        extractUserToken
    };
}
