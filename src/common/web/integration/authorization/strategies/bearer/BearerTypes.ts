/**
 * The Bearer strategy configuration.
 */
export interface BearerStrategyConfiguration {
    bearer_label: string;

    help_link: string;
}

/**
 * Bearer authorization request data.
 */
export interface BearerAuthorizationRequestData {
    bearer_token: string;
}
