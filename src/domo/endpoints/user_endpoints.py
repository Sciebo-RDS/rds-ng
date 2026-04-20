import typing

from flask import request

from common.py.api import DeleteUserCommand
from common.py.core.messaging.composers import MessageBuilder
from common.py.endpoints import abort_request, Endpoint, verify_request_api_header

from .utils import get_server_channel


def delete_user_ep() -> Endpoint:
    """
    Endpoint to delete a user account alongside all data (projects, etc.).

    Returns:
        The endpoint instance.
    """

    def _handler(msg_builder: MessageBuilder) -> typing.Any:
        api_key = verify_request_api_header()

        if (request_data := request.get_json(silent=True)) is not None:
            try:
                user_id = request_data["user_id"]
                if not user_id:
                    raise ValueError("Invalid user ID provided")

                host_id = request_data["host_id"]
                if not host_id:
                    raise ValueError("Invalid host ID provided")

                # Issue a command to the server, ignoring any replies
                DeleteUserCommand.build(
                    msg_builder, user_id=user_id, host_id=host_id, api_key=api_key
                ).done(lambda _, __, ___: None).failed(lambda _, __: None).emit(
                    get_server_channel()
                )

                # We can't send the actual result as a reply, so just send a generic success message
                return {"message": "Delete user call ok"}
            except Exception as exc:  # pylint: disable=broad-exception-caught
                abort_request(f"Invalid data: {exc}")
        else:
            abort_request("Missing or invalid data provided")

        return None

    return Endpoint(
        name="delete_user", path="/command/user", handler=_handler, methods=["DELETE"]
    )
