from common.py.utils.config import Configuration

from .. import AuthorizationStrategyConfiguration


def get_oauth2_strategy_configuration(
    config: Configuration,
) -> AuthorizationStrategyConfiguration:
    from common.py.integration.authorization.strategies.oauth2 import (
        OAuth2StrategyPublicConfiguration,
        OAuth2StrategyPrivateConfiguration,
    )

    from common.py.utils import RedirectionTarget
    from .....settings import OAuth2AuthorizationSettingIDs

    return AuthorizationStrategyConfiguration(
        public_config=OAuth2StrategyPublicConfiguration(
            server=OAuth2StrategyPublicConfiguration.Server(
                host=config.value(OAuth2AuthorizationSettingIDs.SERVER_HOST),
                authorization_endpoint=config.value(
                    OAuth2AuthorizationSettingIDs.SERVER_AUTHORIZATION_ENDPOINT
                ),
                token_endpoint=config.value(
                    OAuth2AuthorizationSettingIDs.SERVER_TOKEN_ENDPOINT
                ),
                scope=config.value(OAuth2AuthorizationSettingIDs.SERVER_SCOPE),
            ),
            client=OAuth2StrategyPublicConfiguration.Client(
                client_id=config.value(OAuth2AuthorizationSettingIDs.CLIENT_ID),
                redirect_url=config.value(
                    OAuth2AuthorizationSettingIDs.CLIENT_REDIRECT_URL
                ),
                redirect_target=RedirectionTarget.BLANK,
            ),
        ).to_dict(),
        private_config=OAuth2StrategyPrivateConfiguration(
            client=OAuth2StrategyPrivateConfiguration.Client(
                client_secret=config.value(OAuth2AuthorizationSettingIDs.CLIENT_SECRET),
            )
        ).to_dict(),
    )
