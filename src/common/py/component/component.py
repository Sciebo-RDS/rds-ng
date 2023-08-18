import json
import typing

from .component_data import ComponentData
from .roles import ComponentRole
from ..utils import UnitID
from ..utils.config import Configuration

if typing.TYPE_CHECKING:
    from ..service import ServiceContextType, Service


class Component:
    """
    Base class for all project components.

    Components are always based on this class. It mainly maintains an instance of the ``Core``, but also stores general information
    about the component itself and the entire project.

    When writing a component, always create a new subclass that extends ``Component``. Pass all the necessary information to its
    constructor and, after doing further setup steps, call its ``run`` method.
    """

    def __init__(
        self,
        comp_id: UnitID,
        role: ComponentRole,
        *,
        module_name: str,
        config_file: str = "./config/config.toml",
    ):
        """
        Args:
            comp_id: The identifier of this component.
            role: The role of this component.
            module_name: The component module name; simply pass ``__name__`` here.
            config_file: The configuration file to load.
        """
        config = self._create_config(config_file)
        comp_id = self._sanitize_component_id(comp_id, config)

        from .meta_information import MetaInformation

        meta_info = MetaInformation()
        comp_info = meta_info.get_component(comp_id.unit)

        self._data = ComponentData(
            comp_id=comp_id,
            role=role,
            config=config,
            title=meta_info.title,
            name=comp_info["name"],
            version=meta_info.version,
        )

        from ..core.logging import info

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
        return self._data.role.runtime_aspects.runtime_app_type(
            self._core.message_bus.network.server, self._core.flask
        )

    def run(self) -> None:
        """
        Starts the component's execution cycles.

        Notes:
            It is mandatory to call this method after creating and setting up a component.
        """
        from ..core.logging import info

        info("Running component")

        self._core.run()

    def create_service(
        self, name: str, *, context_type: type["ServiceContextType"] | None = None
    ) -> "Service":
        """
        Creates and registers a new service.

        Args:
            name: The name of the service.
            context_type: Can be used to override the default ``ServiceContext`` type. All message handlers
                associated with the new service will then receive instances of this type for their service context.

        Returns:
            The newly created service.
        """
        from ..service import Service, ServiceContext

        if context_type is None:
            context_type = ServiceContext

        svc = Service(
            self._data.comp_id,
            name,
            message_bus=self._core.message_bus,
            context_type=context_type,
        )
        self._core.register_service(svc)
        return svc

    def _create_config(self, config_file: str) -> Configuration:
        from ..settings import get_default_settings

        config = Configuration()
        config.add_defaults(get_default_settings())

        try:
            config.load(config_file)
        except Exception as exc:  # pylint: disable=broad-exception-caught
            from ..core.logging import warning

            warning(
                "Component configuration could not be loaded",
                scope="core",
                error=str(exc),
            )

        return config

    def _sanitize_component_id(self, comp_id: UnitID, config: Configuration) -> UnitID:
        if comp_id.instance is None:
            from ..settings import ComponentSettingIDs

            return UnitID(
                comp_id.type, comp_id.unit, config.value(ComponentSettingIDs.INSTANCE)
            )

        return comp_id

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
        self._core.flask.add_url_rule(
            "/",
            view_func=lambda: json.dumps(
                {
                    "id": str(self._data.comp_id),
                    "name": self._data.name,
                    "version": str(self._data.version),
                }
            ),
        )

    def __str__(self) -> str:
        return f"{self._data.title} v{self._data.version}: {self._data.name} ({self._data.comp_id})"
