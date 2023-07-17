import typing
from semantic_version import Version


class MetaInformation:
    """
    Accesses meta information about the entire project and its various component stored in a JSON file.
    
    The JSON file needs to be structured like this::
    
        {
            "global": {
                "title": "RDS-NG",
                "version": "0.0.1"
            },
        
            "components": {
                "gate": {
                    "name": "Gate service",
                    "directory": "gate"
                },
                ...
            }
        }
    
    Args:
        info_file: The JSON file to load the meta information from.
        
    Raises:
        ValueError: If the information file couldn't be loaded.
    """
    
    """ This class is used to access the project meta information stored in a JSON file. """
    def __init__(self, info_file: str = "/config/meta-information.json"):
        import os.path
        if info_file == "" or not os.path.exists(info_file):
            raise ValueError("Invalid meta information file given")
        
        with open(info_file) as f:
            import json
            data = json.load(f)
            self._title, self._version = self._read_global_info(data)
            self._components = self._read_component_definitions(data)

    def _read_global_info(self, data: typing.Any) -> tuple[str, Version]:
        try:
            global_info = data["global"]
            title: str = global_info["title"]
            version = Version(global_info["version"])
        except Exception:
            return "<invalid>", Version("0.0.0")
        else:
            return title, version
        
    def _read_component_definitions(self, data: typing.Any) -> typing.Dict[str, typing.Dict[str, typing.Any]]:
        try:
            comps_info: typing.Dict[str, typing.Dict[str, typing.Any]] = data["components"]
        except Exception:
            return {}
        else:
            return comps_info
        
    @property
    def title(self) -> str:
        """
        The project title.
        """
        return self._title
    
    @property
    def version(self) -> Version:
        """
        The project version (see https://semver.org).
        """
        return self._version

    def get_components(self) -> typing.List[str]:
        """
        A list of all component names.
        
        Returns:
            The names of all components.
        """
        return list(self._components.keys())
    
    def get_component(self, comp: str) -> typing.Dict[str, typing.Any]:
        """
        Retrieves the meta information stored for a specific component.
        
        This meta information includes the `name` of the component, as well as its `directory` within the code structure (rooted at ``/src``).
        
        Args:
            comp: The name of the component.

        Returns:
            A dictionary containing the meta information.
        """
        if comp in self._components:
            return self._components[comp]
        else:
            return {
                "name": "<invalid>",
                "directory": "",
            }
