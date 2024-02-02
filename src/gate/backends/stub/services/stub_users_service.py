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
        from ..data import fill_stub_data_connector_instances

        default_settings = UserSettings()
        fill_stub_data_connector_instances(default_settings)

        settings = ctx.session_storage.get_data(
            msg.origin, "user-settings", default_settings
        )

        GetUserSettingsReply.build(ctx.message_builder, msg, settings=settings).emit()

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

            ctx.session_storage.set_data(msg.origin, "user-settings", user_settings)
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
