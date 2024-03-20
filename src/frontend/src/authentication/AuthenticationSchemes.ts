import logging from "@common/core/logging/Logging";
import { type Constructable } from "@common/utils/Types";

import { AuthenticationScheme } from "@/authentication/AuthenticationScheme";
import { AuthenticationSchemesCatalog } from "@/authentication/AuthenticationSchemesCatalog";

import { BasicAuthenticationScheme } from "@/authentication/schemes/BasicAuthenticationScheme";
import { HostAuthenticationScheme } from "@/authentication/schemes/HostAuthenticationScheme";

/**
 * Registers all available authentication schemes.
 *
 * When adding a new scheme, always register it here.
 */
export function registerAuthenticationSchemes(): void {
    interface ConstructableScheme extends Constructable<AuthenticationScheme> {
        Scheme: string;
    }

    function registerScheme(scheme: ConstructableScheme): void {
        AuthenticationSchemesCatalog.registerItem(scheme.Scheme, scheme);
    }

    // New schemes go here
    registerScheme(BasicAuthenticationScheme);
    registerScheme(HostAuthenticationScheme);

    // Print all available schemes for debugging purposes
    const names = Object.keys(AuthenticationSchemesCatalog.items);
    logging.debug(`Registered authentication schemes: ${names.join("; ")}`);
}
