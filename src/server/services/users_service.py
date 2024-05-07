from common.py.component import BackendComponent
from common.py.data.entities import clone_entity
from common.py.data.entities.user import User
from common.py.services import Service

from .tools import send_projects_list


def create_users_service(comp: BackendComponent) -> Service:
    """
    Creates the users service.

    Args:
        comp: The main component instance.

    Returns:
        The newly created service.
    """

    from common.py.api.user import (
        AuthenticateUserCommand,
        AuthenticateUserReply,
        GetUserSettingsCommand,
        GetUserSettingsReply,
        SetUserSettingsCommand,
        SetUserSettingsReply,
    )
    from common.py.data.verifiers.user import (
        UserSettingsVerifier,
    )

    from .server_service_context import ServerServiceContext

    svc = comp.create_service("Users service", context_type=ServerServiceContext)

    @svc.message_handler(AuthenticateUserCommand)
    def authenticate_user(
        msg: AuthenticateUserCommand, ctx: ServerServiceContext
    ) -> None:
        success = ctx.session_manager[msg.origin].authenticate(
            msg.user_token, msg.origin
        )

        if success:
            user_id = msg.user_token.user_id
            user_name = msg.user_token.user_name

            ctx.logger.info(
                "User authenticated",
                scope="users",
                origin=msg.origin,
                user_id=user_id,
                user_name=user_name,
            )

            # Update or create the authenticated user in the storage
            if (user := ctx.storage_pool.user_storage.get(user_id)) is not None:
                user.name = user_name
            else:
                user = User(user_id=user_id, name=user_name)
                ctx.storage_pool.user_storage.add(user)
        else:
            ctx.logger.warning(
                "Unable to authenticate user",
                scope="users",
                origin=msg.origin,
                user_id=msg.user_token.user_id,
                user_name=msg.user_token.user_name,
            )

        AuthenticateUserReply.build(
            ctx.message_builder,
            msg,
            success=success,
            message="Invalid user token" if not success else "",
        ).emit()

    @svc.message_handler(GetUserSettingsCommand)
    def get_user_settings(
        msg: GetUserSettingsCommand, ctx: ServerServiceContext
    ) -> None:
        if not ctx.ensure_user(msg, GetUserSettingsReply, settings=User.Settings()):
            return

        GetUserSettingsReply.build(
            ctx.message_builder,
            msg,
            settings=ctx.user.user_settings,
        ).emit()

    @svc.message_handler(SetUserSettingsCommand)
    def set_user_settings(
        msg: SetUserSettingsCommand, ctx: ServerServiceContext
    ) -> None:
        if not ctx.ensure_user(msg, SetUserSettingsReply, settings=User.Settings()):
            return

        success = False
        message = ""

        try:
            user_settings_upd = clone_entity(msg.settings)

            # Strip string values
            for index, instance in enumerate(user_settings_upd.connector_instances):
                instance.name = instance.name.strip()
                instance.description = instance.description.strip()

            UserSettingsVerifier(
                user_settings_upd, connectors=ctx.storage_pool.connector_storage.list()
            ).verify_update()

            ctx.user.user_settings = user_settings_upd
            success = True
        except Exception as exc:  # pylint: disable=broad-exception-caught
            message = str(exc)

        SetUserSettingsReply.build(
            ctx.message_builder,
            msg,
            success=success,
            message=message,
            settings=ctx.user.user_settings,
        ).emit()

        send_projects_list(msg, ctx)

    return svc
