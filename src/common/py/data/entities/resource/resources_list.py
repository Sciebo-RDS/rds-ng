import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .resource import Resource

ResourceFolders = typing.Dict[Resource, typing.Union["ResourcesList", None]]
ResourceFiles = typing.List[Resource]


@dataclass_json
@dataclass(frozen=True, kw_only=True)
class ResourcesList:
    """
    A recursive list of resources.

    Notes:
        Resources are always given in absolute form.

    Attributes:
        resource: The current resource path.
        folders: A dictionary containing all folders and their respective sub-folder contents (can be **None**).
        files: A list of all files.
    """

    resource: Resource

    folders: ResourceFolders = field(default_factory=dict)
    files: ResourceFiles = field(default_factory=list)
