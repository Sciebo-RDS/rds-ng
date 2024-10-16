import typing

from .webdav_types import WebdavResource
from .....utils import ensure_starts_with, get_mime_type


def parse_webdav_resource(
    resource: typing.Dict[str, typing.Any], webdav_endpoint: str
) -> WebdavResource | None:
    """
    Transforms a WebDAV resource into a well-formatted object.

    Args:
        resource: The WebDAV resource.
        webdav_endpoint: The endpoint that was used for resource retrieval (will be omitted from the result path).

    Returns:
        A well-formatted resource object.
    """
    try:
        resource = typing.cast(WebdavResource, WebdavResource.from_dict(resource))
        content_type = ""
        if not resource.isdir:
            content_type = (
                resource.content_type
                if resource.content_type is not None
                else get_mime_type(resource.path)
            )

        return WebdavResource(
            path=ensure_starts_with(
                ensure_starts_with(resource.path, "/").replace(webdav_endpoint, "", 1),
                "/",
            ),
            isdir=resource.isdir,
            size=resource.size if resource.size else 0,
            content_type=content_type,
        )  # Return a cleaned up and standardized resource
    except:  # pylint: disable=bare-except
        return None
