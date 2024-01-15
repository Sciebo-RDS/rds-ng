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
        GetUserConfigurationCommand,
        GetUserConfigurationReply,
        SetUserConfigurationCommand,
        SetUserConfigurationReply,
    )
    from common.py.data.verifiers.user import (
        UserConfigurationVerifier,
    )

    from .stub_service_context import StubServiceContext

    svc = comp.create_service("Users service", context_type=StubServiceContext)

    @svc.message_handler(GetUserConfigurationCommand)
    def get_user_configuration(
        msg: GetUserConfigurationCommand, ctx: StubServiceContext
    ) -> None:
        GetUserConfigurationReply.build(
            ctx.message_builder, msg, configuration=ctx.user_configuration
        ).emit()

    @svc.message_handler(SetUserConfigurationCommand)
    def set_user_configuration(
        msg: SetUserConfigurationCommand, ctx: StubServiceContext
    ) -> None:
        success = False
        message = ""

        try:
            user_config = msg.configuration

            UserConfigurationVerifier(
                user_config, connectors=ctx.storage_pool.connector_storage.list()
            ).verify_update()

            ctx.user_configuration = user_config
            success = True
        except Exception as exc:  # pylint: disable=broad-exception-caught
            message = str(exc)

        SetUserConfigurationReply.build(
            ctx.message_builder, msg, success=success, message=message
        )

    return svc
