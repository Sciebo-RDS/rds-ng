/**
 * The Basic strategy configuration.
 */
export interface BasicStrategyConfiguration {
    user_id_label: string;
    user_password_label: string;

    help_link: string;
}

/**
 * Basic authorization request data.
 */
export interface BasicAuthorizationRequestData {
    user_id: string;
    user_password: string;
}
