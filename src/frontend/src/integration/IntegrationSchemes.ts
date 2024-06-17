import logging from "@common/core/logging/Logging";
import { type Constructable } from "@common/utils/Types";

import { IntegrationScheme } from "@/integration/IntegrationScheme";
import { IntegrationSchemesCatalog } from "@/integration/IntegrationSchemesCatalog";

import { BasicIntegrationScheme } from "@/integration/schemes/BasicIntegrationScheme";
import { HostIntegrationScheme } from "@/integration/schemes/HostIntegrationScheme";

/**
 * Registers all available integration schemes.
 *
 * When adding a new scheme, always register it here.
 */
export function registerIntegrationSchemes(): void {
    interface ConstructableScheme extends Constructable<IntegrationScheme> {
        Scheme: string;
    }

    function registerScheme(scheme: ConstructableScheme): void {
        IntegrationSchemesCatalog.registerItem(scheme.Scheme, scheme);
    }

    // New schemes go here
    registerScheme(BasicIntegrationScheme);
    registerScheme(HostIntegrationScheme);

    // Print all available schemes for debugging purposes
    const names = Object.keys(IntegrationSchemesCatalog.items);
    logging.debug(`Registered integration schemes: ${names.join("; ")}`);
}
