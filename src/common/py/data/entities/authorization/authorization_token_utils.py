import time
import typing

from .authorization_token import AuthorizationTokenID, AuthorizationToken

# Avoid some cyclic dependencies
if typing.TYPE_CHECKING:
    from ..connector import ConnectorInstanceID
    from ..user import User


def get_host_authorization_token_id(user: "User") -> AuthorizationTokenID:
    """
    Retrieves the authorization token ID for the user host system.

    Args:
        user: The user.

    Returns:
        The authorization token ID.
    """
    return user.user_id, AuthorizationToken.TokenType.HOST


def get_connector_instance_authorization_token_id(
    user: "User", instance: "ConnectorInstanceID"
) -> AuthorizationTokenID:
    """
    Retrieves the authorization token ID for a connector instance.

    Args:
        user: The user.
        instance: The connector instance ID.

    Returns:
        The authorization token ID.
    """
    return user.user_id, f"{AuthorizationToken.TokenType.CONNECTOR}:{instance}"


def has_authorization_token_expired(token: AuthorizationToken) -> bool:
    """
    Checks whether an authorization token has expired and thus should be refreshed.

    Args:
        token: The authorization token.
    """
    return (
        time.time() >= token.expiration_timestamp
        if token.expiration_timestamp > 0
        else False
    )
