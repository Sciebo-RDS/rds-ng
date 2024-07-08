import typing

from common.py.integration.authorization.strategies import OAuth2StrategyConfiguration
from common.py.utils.config import Configuration


def get_oauth2_strategy_configuration(
    config: Configuration,
) -> typing.Dict[str, typing.Any]:
    from .....settings import OAuth2AuthorizationSettingIDs

    return OAuth2StrategyConfiguration(
        server=OAuth2StrategyConfiguration.Server(
            host=config.value(OAuth2AuthorizationSettingIDs.SERVER_HOST),
            authorization_endpoint=config.value(
                OAuth2AuthorizationSettingIDs.SERVER_AUTHORIZATION_ENDPOINT
            ),
            token_endpoint=config.value(
                OAuth2AuthorizationSettingIDs.SERVER_TOKEN_ENDPOINT
            ),
            scope=config.value(OAuth2AuthorizationSettingIDs.SERVER_SCOPE),
        ),
        client=OAuth2StrategyConfiguration.Client(
            client_id=config.value(OAuth2AuthorizationSettingIDs.CLIENT_ID),
            redirect_url=config.value(
                OAuth2AuthorizationSettingIDs.CLIENT_REDIRECT_URL
            ),
        ),
    ).to_dict()
