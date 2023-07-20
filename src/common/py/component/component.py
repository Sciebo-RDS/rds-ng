import json
import typing

import socketio

from .component_data import ComponentData
from .component_id import ComponentID
from .roles.component_role import ComponentRole
from ..core.logging import info, warning
from ..utils.config import Configuration

if typing.TYPE_CHECKING:
    from ..core import Core  # We can't import this regularely due to cyclic imports


class Component:
    """
    Base class for all project components.
    
    Components are always based on this class. It mainly maintains an instance of the ``Core``, but also stores general information
    about the component itself and the entire project.
    
    When writing a component, always create a new subclass that extends ``Component``. Pass all the necessary information to its
    constructor (see ``Args``) and, after doing further setup steps, call its ``run`` method.
    
    Args:
        comp_id: The identifier of this component.
        role: The role of this component.
        module_name: The component module name; simply pass ``__name__`` here.
        config_file: The configuration file to load.
    """
    def __init__(self, comp_id: ComponentID, role: ComponentRole, *, module_name: str, config_file: str = "./config.toml"):
        """
        Args:
            comp_id: The identifier of this component.
            role: The role of this component.
            module_name: The component module name; simply pass ``__name__`` here).
            config_file: The configuration file to load.
        """
        config = self._create_config(config_file)
        comp_id = self._sanitize_component_id(comp_id, config)
        
        from .meta_information import MetaInformation
        meta_info = MetaInformation()
        comp_info = meta_info.get_component(comp_id.component)
        
        self._data = ComponentData(
            comp_id=comp_id,
            role=role,
            config=config,
            title=meta_info.title,
            name=comp_info["name"],
            version=meta_info.version,
        )
        
        info(str(self), role=self._data.role.name)
        info("-- Starting component...")
        
        from ..core import Core
        self._core = Core(module_name, self._data)
        
        self._add_default_routes()
        
    def app(self) -> typing.Any:
        """
        Creates a WSGI application object that can be used to be run by a gateway service.
        
        Returns:
            The WSGI application object.
        """
        # Note: This is the only dependency on socket.io outside the network engine, as we need to use their app logic
        return socketio.WSGIApp(self._core.message_bus.network.server, self._core.flask)
   
    def run(self) -> None:
        """
        Starts the component's execution cycles.
        
        Notes:
            It is mandatory to call this method after creating and setting up a component.
        """
        self._core.run()
    
    def _create_config(self, config_file: str) -> Configuration:
        from ..settings import get_default_settings
        config = Configuration()
        config.add_defaults(get_default_settings())
        
        try:
            config.load(config_file)
        except Exception as e:
            warning("Component configuration could not be loaded", scope="core", error=str(e))
        
        return config
    
    def _sanitize_component_id(self, comp_id: ComponentID, config: Configuration) -> ComponentID:
        if comp_id.instance is None:
            from ..settings import ComponentSettingIDs
            return ComponentID(comp_id.type, comp_id.component, config.value(ComponentSettingIDs.INSTANCE))
        else:
            return comp_id
    
    @property
    def core(self) -> 'Core':
        """
        The global ``Core`` instance.
        """
        return self._core
    
    @property
    def config(self) -> Configuration:
        """
        The configuration used by the component.
        """
        return self._data.config

    @property
    def data(self) -> ComponentData:
        """
        A data helper object that stores useful component data and information.
        """
        return self._data
    
    def _add_default_routes(self) -> None:
        # The main entry point (/) returns basic component info as a JSON string
        self._core.flask.add_url_rule("/", view_func=lambda: json.dumps({
            "id": str(self._data.comp_id),
            "name": self._data.name,
            "version": str(self._data.version),
        }))

    def __str__(self) -> str:
        return f"{self._data.title} v{self._data.version}: {self._data.name} ({self._data.comp_id})"
