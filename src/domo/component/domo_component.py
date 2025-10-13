import typing

from common.py.component import BackendComponent, ComponentType, ComponentUnit
from common.py.component.roles import LeafRole
from common.py.utils import UnitID


class DomoComponent(BackendComponent):
    """
    The base domo component class.
    """

    def __init__(self):
        super().__init__(
            UnitID(
                ComponentType.INFRASTRUCTURE,
                ComponentUnit.DOMO,
            ),
            "Domo",
            LeafRole(),
            module_name=__name__,
        )

    def run(self) -> None:
        super().run()

    def _add_custom_routes(self) -> None:
        from ..endpoints import authorization_redirect_ep

        self.add_route_endpoint(authorization_redirect_ep())

    @staticmethod
    def instance() -> "DomoComponent":
        """
        The global ``DomoComponent`` instance.

        Raises:
            RuntimeError: If no instance has been created.
        """
        return typing.cast(DomoComponent, BackendComponent.instance())
