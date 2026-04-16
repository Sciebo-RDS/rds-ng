import typing

from flask import request

from common.py.core.messaging.composers import MessageBuilder
from common.py.endpoints import abort_request, Endpoint, verify_request_api_header


def delete_user_ep() -> Endpoint:
    """
    Endpoint to delete a user account alongside all data (projects, etc.).

    Returns:
        The endpoint instance.
    """

    def _handler(msg_builder: MessageBuilder) -> typing.Any:
        # from common.py.services import ClientServiceContext

        verify_request_api_header()

        # cmd = PingCommand.build(msg_builder)
        # cmd.emit(ClientServiceContext.get_remote_channel())

        if (request_data := request.get_json(silent=True)) is not None:
            try:
                user_id = request_data["user_id"]
                if not user_id:
                    raise ValueError("Invalid user id provided")

                instance_id = request_data["instance_id"]
                if not instance_id:
                    raise ValueError("Invalid instance id provided")

                # TODO: Dispatch message

                return {"message": "Delete user call ok"}
            except Exception as exc:  # pylint: disable=broad-exception-caught
                abort_request(f"Invalid data: {exc}")
        else:
            abort_request("Missing or invalid data provided")

        return None

    return Endpoint(
        name="delete_user", path="/command/user", handler=_handler, methods=["DELETE"]
    )
