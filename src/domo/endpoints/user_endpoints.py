import typing

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

        abort_request("Emitted")

    return Endpoint(
        name="delete_user", path="/command/user", handler=_handler, methods=["DELETE"]
    )


# import json
# import typing
#
# from flask import request
#
# from common.py.core.messaging import Channel, unpack_message
# from common.py.endpoints.endpoint import Endpoint
#
# from ..component import ServerComponent
#
#
# def delete_user_ep() -> Endpoint:
#     """
#     Endpoint to delete a user account alongside all data (projects, etc.).
#
#     Returns:
#         The endpoint instance.
#     """
#
#     def _handler() -> typing.Any:
#         from .utils import verify_request_api_header, abort_request
#
#         comp = ServerComponent.instance()
#
#         # Using this EP always requires a valid API key passed via header, even if the message itself isn't protected
#         verify_request_api_header()
#
#         if (request_data := request.get_json(silent=True)) is not None:
#             try:
#                 # Always target the server to prevent unintended routing
#                 request_data["target"] = json.loads(
#                     Channel.direct(comp.data.comp_id).to_json()
#                 )
#
#                 # Unpack and dispatch the message
#                 msg = unpack_message(
#                     request_data["name"],
#                     json.dumps(request_data),
#                     comp_id=comp.data.comp_id,
#                 )
#                 # TODO: Dispatch message
#
#                 return {"message": "API call ok"}
#             except Exception as exc:  # pylint: disable=broad-exception-caught
#                 abort_request(f"Invalid data: {exc}")
#         else:
#             abort_request("Missing or invalid data provided")
#
#         return {"message": "Unknown error"}
#
#     return Endpoint(name="api_v1", path="/api/v1", handler=_handler, methods=["DELETE"])
