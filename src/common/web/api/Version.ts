import { SemVer } from "semver";

export const API_PROTOCOL_VERSION: SemVer = new SemVer("3.0.0");

/**
 * Compatibility degrees.
 */
export const enum ProtocolCompatibility {
    Compatible,
    MaybeCompatible,
    NotCompatible
}

/**
 * Checks if the given protocol version is compatible with the current one.
 *
 * @param version - The protocol version to check.
 */
export function checkProtocolCompatibility(version: SemVer): ProtocolCompatibility {
    if (version.major != API_PROTOCOL_VERSION.major) {
        return ProtocolCompatibility.NotCompatible;
    } else if (version.minor != API_PROTOCOL_VERSION.minor) {
        return ProtocolCompatibility.MaybeCompatible;
    }

    return ProtocolCompatibility.Compatible;
}
