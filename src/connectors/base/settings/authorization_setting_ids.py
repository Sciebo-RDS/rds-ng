from common.py.utils.config import SettingID


class AuthorizationSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for general authorization settings.

    Attributes:
        STRATEGY: The authorization strategy to use (value type: ``string``).
    """
    STRATEGY = SettingID("authorization", "strategy")


class OAuth2AuthorizationSettingIDs:
    # pylint: disable=too-few-public-methods
    """
    Identifiers for OAuth2 authorization settings.

    Attributes:
        SERVER_HOST: The OAuth2 host server (value type: ``string``).
        SERVER_AUTHORIZATION_ENDPOINT: The (relative) authorization endpoint (value type: ``string``).
        SERVER_TOKEN_ENDPOINT: The (relative) token endpoint (value type: ``string``).
        SERVER_SCOPE: The (optional) access scope (value type: ``string``).
        CLIENT_ID: The client ID (value type: ``string``).
        CLIENT_REDIRECT_URL: The redirection URL (value type: ``string``).
    """
    SERVER_HOST = SettingID("authorization.oauth2", "server.host")
    SERVER_AUTHORIZATION_ENDPOINT = SettingID(
        "authorization.oauth2", "server.authorization_endpoint"
    )
    SERVER_TOKEN_ENDPOINT = SettingID("authorization.oauth2", "server.token_endpoint")
    SERVER_SCOPE = SettingID("authorization.oauth2", "server.scope")

    CLIENT_ID = SettingID("authorization.oauth2", "client.id")
    CLIENT_REDIRECT_URL = SettingID("authorization.oauth2", "client.redirect_url")
