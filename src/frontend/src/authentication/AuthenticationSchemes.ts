import logging from "@common/core/logging/Logging";

import { AuthenticationScheme } from "@/authentication/AuthenticationScheme";
import { AuthenticationSchemesCatalog } from "@/authentication/AuthenticationSchemesCatalog";
import { FrontendComponent } from "@/component/FrontendComponent";

import { BasicAuthenticationScheme } from "@/authentication/schemes/BasicAuthenticationScheme";
import { HostAuthenticationScheme } from "@/authentication/schemes/HostAuthenticationScheme";

/**
 * Registers all available authentication schemes.
 *
 * When adding a new scheme, always register it here.
 */
export function registerAuthenticationSchemes(comp: FrontendComponent): void {
    function registerScheme(scheme: AuthenticationScheme): void {
        AuthenticationSchemesCatalog.registerItem(scheme.scheme, scheme);
    }

    // New schemes go here
    registerScheme(new BasicAuthenticationScheme(comp));
    registerScheme(new HostAuthenticationScheme(comp));

    // Print all available schemes for debugging purposes
    const names = Object.keys(AuthenticationSchemesCatalog.items);
    logging.debug(`Registered authentication schemes: ${names.join("; ")}`);
}
