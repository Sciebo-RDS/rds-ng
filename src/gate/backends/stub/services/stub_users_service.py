from common.py.component import BackendComponent
from common.py.data.entities.connector import ConnectorInstance
from common.py.data.entities.user import UserSettings
from common.py.services import Service


def create_stub_users_service(comp: BackendComponent) -> Service:
    """
    Creates the stub backend users service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api.user import (
        GetUserSettingsCommand,
        GetUserSettingsReply,
        SetUserSettingsCommand,
        SetUserSettingsReply,
    )
    from common.py.data.verifiers.user import (
        UserSettingsVerifier,
    )

    from .stub_service_context import StubServiceContext

    svc = comp.create_service("Users service", context_type=StubServiceContext)

    @svc.message_handler(GetUserSettingsCommand)
    def get_user_settings(msg: GetUserSettingsCommand, ctx: StubServiceContext) -> None:
        if ctx.user_token not in StubServiceContext.user_settings:
            from ..data import get_stub_data_connector_instances

            default_settings = UserSettings()
            default_settings.connector_instances.extend(
                get_stub_data_connector_instances()
            )

            StubServiceContext.user_settings[ctx.user_token] = default_settings

        GetUserSettingsReply.build(
            ctx.message_builder,
            msg,
            settings=StubServiceContext.user_settings[ctx.user_token],
        ).emit()

    @svc.message_handler(SetUserSettingsCommand)
    def set_user_settings(msg: SetUserSettingsCommand, ctx: StubServiceContext) -> None:
        success = False
        message = ""

        user_settings = msg.settings

        # Strip string values
        for index, instance in enumerate(user_settings.connector_instances):
            user_settings.connector_instances[index] = ConnectorInstance(
                instance_id=instance.instance_id,
                connector_id=instance.connector_id,
                name=instance.name.strip(),
                description=instance.description.strip(),
            )

        try:
            UserSettingsVerifier(
                user_settings, connectors=ctx.storage_pool.connector_storage.list()
            ).verify_update()

            StubServiceContext.user_settings[ctx.user_token] = user_settings
            success = True
        except Exception as exc:  # pylint: disable=broad-exception-caught
            message = str(exc)

        SetUserSettingsReply.build(
            ctx.message_builder,
            msg,
            success=success,
            message=message,
            settings=user_settings,
        ).emit()

    return svc
