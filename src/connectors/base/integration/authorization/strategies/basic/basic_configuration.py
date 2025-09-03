from common.py.utils.config import Configuration

from .. import AuthorizationStrategyConfiguration


def get_basic_strategy_configuration(
    config: Configuration,
) -> AuthorizationStrategyConfiguration:
    from common.py.integration.authorization.strategies.basic import (
        BasicStrategyConfiguration,
    )

    from .....settings import BasicAuthorizationSettingIDs

    return AuthorizationStrategyConfiguration(
        public_config=BasicStrategyConfiguration(
            user_id_label=config.value(BasicAuthorizationSettingIDs.USER_ID_LABEL),
            user_id_optional=config.value(
                BasicAuthorizationSettingIDs.USER_ID_OPTIONAL
            ),
            user_password_label=config.value(
                BasicAuthorizationSettingIDs.USER_PASSWORD_LABEL
            ),
            user_password_optional=config.value(
                BasicAuthorizationSettingIDs.USER_PASSWORD_OPTIONAL
            ),
            help_link=config.value(BasicAuthorizationSettingIDs.HELP_LINK),
        ).to_dict(),
        private_config={},
    )
