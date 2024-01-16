from common.py.component import BackendComponent
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
        GetUserSettingsReply.build(
            ctx.message_builder, msg, settings=ctx.user_settings
        ).emit()

    @svc.message_handler(SetUserSettingsCommand)
    def set_user_settings(msg: SetUserSettingsCommand, ctx: StubServiceContext) -> None:
        success = False
        message = ""

        try:
            user_settings = msg.settings

            UserSettingsVerifier(
                user_settings, connectors=ctx.storage_pool.connector_storage.list()
            ).verify_update()

            ctx.user_settings = user_settings
            success = True
        except Exception as exc:  # pylint: disable=broad-exception-caught
            message = str(exc)

        SetUserSettingsReply.build(
            ctx.message_builder, msg, success=success, message=message
        ).emit()

    return svc
