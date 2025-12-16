from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(kw_only=True, frozen=True)
class TenantPublicConfiguration:
    """
    Public tenant configuration.
    """

    @dataclass_json
    @dataclass(kw_only=True, frozen=True)
    class Integration:
        """
        General integration settings.
        """

        @dataclass_json
        @dataclass(kw_only=True, frozen=True)
        class HostIntegration:
            @dataclass_json
            @dataclass(kw_only=True, frozen=True)
            class Endpoints:
                """
                Host endpoint settings.
                """

                entrypoint: str
                api: str

            """
            Host integration settings.
            """

            url: str
            endpoints: Endpoints

        scheme: str

        host_integration: HostIntegration

    @dataclass_json
    @dataclass(kw_only=True, frozen=True)
    class Authorization:
        """
        Authorization settings.
        """

        @dataclass_json
        @dataclass(kw_only=True, frozen=True)
        class OAuth2:
            """
            OAuth2 authorization settings.
            """

            client_id: str

        oauth2: OAuth2

    integration: Integration
    authorization: Authorization


@dataclass_json
@dataclass(kw_only=True, frozen=True)
class TenantPrivateConfiguration:
    """
    Private tenant configuration.
    """

    @dataclass_json
    @dataclass(kw_only=True, frozen=True)
    class Authorization:
        """
        Authorization settings.
        """

        @dataclass_json
        @dataclass(kw_only=True, frozen=True)
        class OAuth2:
            """
            OAuth2 authorization settings.
            """

            client_secret: str

        oauth2: OAuth2

    authorization: Authorization
