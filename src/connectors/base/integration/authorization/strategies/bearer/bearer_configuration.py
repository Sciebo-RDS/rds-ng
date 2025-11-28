from common.py.utils.config import Configuration

from .. import AuthorizationStrategyConfiguration


def get_bearer_strategy_configuration(
    config: Configuration,
) -> AuthorizationStrategyConfiguration:
    from common.py.integration.authorization.strategies.bearer import (
        BearerStrategyConfiguration,
    )

    from .....settings import BearerAuthorizationSettingIDs

    return AuthorizationStrategyConfiguration(
        public_config=BearerStrategyConfiguration(
            bearer_label=config.value(BearerAuthorizationSettingIDs.BEARER_LABEL),
            help_link=config.value(BearerAuthorizationSettingIDs.HELP_LINK),
        ).to_dict(),
        private_config={},
    )
