import typing

from requests import Response


def format_oauth2_error_response(response: Response) -> str:
    """
    Formats an OAuth2 error to a human-readable string.

    Args:
        response: The OAuth2 response.

    Returns:
        The formatted string.
    """
    resp_data = response.json()
    if "error" in resp_data:
        err_type = typing.cast(str, resp_data["error"])
        err_type = err_type.replace("_", " ")
    else:
        err_type = "unknown error"

    return f"{err_type} ({response.status_code})".title()
