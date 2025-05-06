/**
 * Settings for authorization.
 *
 * @param strategy - The authorization strategy; if empty, none is used.
 * @param config - The authorization configuration.
 */
export interface AuthorizationSettings {
    strategy: string;
    config: Record<string, any>;
}
