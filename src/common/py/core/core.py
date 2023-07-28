import flask

from .logging import info, debug, set_level
from .messaging import MessageBus
from .messaging.handlers import MessageService
from ..component import ComponentData


class Core:
    """
    The main *underlying basis* of any component.
    
    The ``Core`` brings together all portions and aspects that build the underlying foundation of every component,
    including the ``MessageBus``.
    
    The core can be regarded as a facade to the *inner structure* of a component. It only offers a small number of public
    methods and is accessed from the outside very rarely.

    An instance of this class is always created when creating a ``Component``; it should never be instantiated otherwise.
    """
    def __init__(self, module_name: str, comp_data: ComponentData):
        """
        Args:
            module_name: The module name used for *Flask* initialization.
            comp_data: The component data used to access common component information.
        """
        info("Initializing core...", scope="core")
        
        self._comp_data = comp_data
        
        if self.is_debug_mode:
            self._enable_debug_mode()
        
        debug(f"-- Settings file: {self._comp_data.config.settings_file}", scope="core")
        
        debug("-- Creating Flask server", scope="core", module_name=module_name)
        self._flask = self._create_flask(module_name)
        
        debug("-- Creating message bus", scope="core")
        self._message_bus = self._create_message_bus()
    
    def _create_flask(self, module_name: str) -> flask.Flask:
        from ..utils.random import generate_random_string
        
        if module_name == "":
            raise ValueError("Invalid module name given")
        
        flsk = flask.Flask(module_name)
        flsk.config["SECRET"] = generate_random_string(64)
        return flsk
    
    def _create_message_bus(self) -> MessageBus:
        return MessageBus(self._comp_data)
    
    def _enable_debug_mode(self) -> None:
        import logging as log
        set_level(log.DEBUG)
        debug("-- Debug mode enabled", scope="core")
    
    def register_service(self, svc: MessageService) -> None:
        """
        Registers a message service.
        
        Services are always created and registered using ``create_service`` (in ``Component``),
        so you should rarely (if ever) need to call this method directly.
        
        Args:
            svc: The message service to register.
        """
        if self._message_bus.add_service(svc):
            debug(f"Registered service: {svc}", scope="core")
        else:
            debug("Service already registered", scope="core", service=svc)
            
    def unregister_service(self, svc: MessageService) -> None:
        """
        Removes a message service.
        
        Args:
            svc: The message service to remove.
        """
        if self._message_bus.remove_service(svc):
            debug(f"Unregistered service: {svc}", scope="core")
        else:
            debug("Service not registered", scope="core", service=svc)
            
    def run(self) -> None:
        """
        Starts periodic background tasks.
        """
        self._message_bus.run()
        
    @property
    def message_bus(self) -> MessageBus:
        """
        The global ``MessageBus`` instance.
        """
        return self._message_bus
    
    @property
    def flask(self) -> flask.Flask:
        """
        The global ``Flask`` instance.
        """
        return self._flask
        
    @property
    def is_debug_mode(self) -> bool:
        """
        Whether we're running in Debug mode.
        """
        from ..settings import GeneralSettingIDs
        return self._comp_data.config.value(GeneralSettingIDs.DEBUG)
