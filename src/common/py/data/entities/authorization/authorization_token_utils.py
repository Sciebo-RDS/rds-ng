from .authorization_token import AuthorizationTokenID
from ..connector import ConnectorInstanceID
from ..user import User


def get_host_authorization_token_id(user: User) -> AuthorizationTokenID:
    """
    Retrieves the authorization token ID for the user host system.

    Args:
        user: The user.

    Returns:
        The authorization token ID.
    """
    return user.user_id, "host"


def get_connector_instance_authorization_token_id(
    user: User, instance: ConnectorInstanceID
) -> AuthorizationTokenID:
    """
    Retrieves the authorization token ID for a connector instance.

    Args:
        user: The user.
        instance: The connector instance ID.

    Returns:
        The authorization token ID.
    """
    return user.user_id, f"connector:{instance}"
