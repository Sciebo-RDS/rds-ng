import typing
from dataclasses import dataclass, field

from dataclasses_json import dataclass_json

from .resource import Resource

ResourceFolders = typing.List["ResourcesList"]
ResourceFiles = typing.List[Resource]


@dataclass_json
@dataclass(kw_only=True)
class ResourcesList:
    """
    A recursive list of resources.

    Notes:
        Resources are always given in absolute form.

    Attributes:
        resource: The current resource path.
        folders: A list of all folders.
        files: A list of all files.
    """

    resource: Resource

    folders: ResourceFolders = field(default_factory=list)
    files: ResourceFiles = field(default_factory=list)
