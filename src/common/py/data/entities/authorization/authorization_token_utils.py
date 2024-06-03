from .authorization_token import AuthorizationTokenID
from ..user import UserID


def combine_authorization_token_id(
    user_id: UserID, token_id: str
) -> AuthorizationTokenID:
    """
    Combines the keys of an authorization token ID (user ID + token ID) into a tuple.

    Args:
        user_id: The user ID.
        token_id: The token ID.

    Returns:
        The ID tuple.
    """
    return user_id, token_id
