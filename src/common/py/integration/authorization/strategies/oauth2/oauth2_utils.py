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
    err_type = (
        typing.cast(str, resp_data["error"]).replace("_", " ")
        if "error" in resp_data
        else "unknown error"
    )
    err_desc = (
        " - " + resp_data["error_description"]
        if "error_description" in resp_data
        else ""
    )
    return f"{err_type}{err_desc} ({response.status_code})".title()
