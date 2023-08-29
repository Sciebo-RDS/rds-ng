from common.py.component import (
    BackendComponent,
    ComponentType,
    ComponentUnit,
)
from common.py.component.roles import NodeRole
from common.py.utils import UnitID

comp = BackendComponent(
    UnitID(ComponentType.INFRASTRUCTURE, ComponentUnit.GATE),
    NodeRole(),
    module_name=__name__,
)
app = comp.app()

svc = comp.create_service("Gate service")

comp.run()
