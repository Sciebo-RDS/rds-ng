from dataclasses import dataclass

from dataclasses_json import dataclass_json

from ...data.entities.authorization import AuthorizationToken


@dataclass_json
@dataclass(kw_only=True)
class AuthorizationRequestPayload:
    """
    The payload that is sent with authorization requests.

    Attributes:
        auth_id: The authorization ID.
        auth_type: The authorization type.
        auth_issuer: The entity that requires the authorization.
        auth_issuer_url: The URL of above entity.
        auth_bearer: The entity that will be authorized against.

        fingerprint: The user's fingerprint.
    """

    auth_id: str = ""
    auth_type: AuthorizationToken.TokenType = AuthorizationToken.TokenType.INVALID
    auth_issuer: str = ""
    auth_issuer_url: str = ""
    auth_bearer: str = ""

    fingerprint: str = ""
